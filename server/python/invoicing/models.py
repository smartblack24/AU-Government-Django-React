from datetime import timedelta
from decimal import Decimal
from functools import reduce

from sitename.mixins import UpdateAttributesMixin
from sitename.utils import invoice_number, get_xero_client
from billing.models import DISBURSEMENT, FIXED_PRICE_ITEM, TIME_ENTRY
from core.models import InvoiceStatus
from django.db import models
from django.db.models import Q, Sum, Value
from django.db.models.functions import Coalesce
from simple_history.models import HistoricalRecords
from .utils import prepare_xero_invoice_param, get_payment_method


class Invoice(models.Model, UpdateAttributesMixin):
    BILLING_METHODS = ((1, 'Fixed price'), (2, 'Time Entry'))

    matter = models.ForeignKey(
        'billing.Matter',
        related_name='invoices',
        on_delete=models.CASCADE
    )
    created_date = models.DateField(null=True)
    payment_terms = models.ForeignKey(
        'invoicing.PaymentTerms',
        related_name='invoices',
        default=1,
        on_delete=models.SET_DEFAULT
    )
    status = models.ForeignKey(
        'core.InvoiceStatus',
        default=1,
        on_delete=models.SET_DEFAULT
    )
    billing_method = models.IntegerField(choices=BILLING_METHODS)
    xero_invoice_id = models.CharField(max_length=256, null=True, unique=True)
    history = HistoricalRecords()
    is_invoice_paid = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created_date', )

    def __str__(self):
        return self.number

    @staticmethod
    def calculate_value(gst=False, attr="cost"):
        def calculate(total, current_value):
            if gst:
                if current_value.gst_status is 1:
                    return (total + getattr(current_value, attr) +
                            (10 * getattr(current_value, attr)) / Decimal('100.0'))
            else:
                return total + getattr(current_value, attr)

            return total + getattr(current_value, attr)

        return calculate

    @property
    def number(self):
        if self.id is 10025:
            return "100258"
        elif self.id is 10026:
            return "100266"

        return invoice_number(self.id)

    @property
    def recorded_time(self):
        return self.time_entries.all()

    @property
    def received_payments(self):
        result = self.payments.aggregate(total=Coalesce(
            Sum('amount'), Value(0))).get('total')
        if not result:
            return Decimal('0')
        return result

    @property
    def net_outstanding(self):
        return Decimal(self.value(gst=True) - self.received_payments)

    @property
    def time_entry_value(self):
        return self.time_entries.filter(
            Q(entry_type=TIME_ENTRY) | Q(entry_type=DISBURSEMENT)
        ).cost()

    @property
    def fixed_price_value(self):
        return self.time_entries.filter(
            Q(entry_type=FIXED_PRICE_ITEM) | Q(entry_type=DISBURSEMENT)
        ).cost()

    def value(self, gst=False):
        if self.billing_method is 1:
            return self.time_entries.filter(
                Q(entry_type=DISBURSEMENT) | Q(entry_type=FIXED_PRICE_ITEM)
            ).cost(gst)

        return self.time_entries.filter(
            Q(entry_type=TIME_ENTRY) | Q(entry_type=DISBURSEMENT)
        ).cost(gst)

    @property
    def billing_method_entries(self):
        if self.billing_method is 1:
            time_entries = self.time_entries.filter(
                Q(entry_type=FIXED_PRICE_ITEM) | Q(entry_type=DISBURSEMENT))
        else:
            time_entries = self.time_entries.filter(
                Q(entry_type=TIME_ENTRY) | Q(entry_type=DISBURSEMENT))

        return time_entries

    @property
    def total_fixed_price_items_value(self):
        return self.time_entries.filter(entry_type=FIXED_PRICE_ITEM).cost()

    @property
    def total_billed_value(self):
        if self.billing_method is 1:
            time_entries = self.time_entries.filter(
                Q(entry_type=TIME_ENTRY) | Q(entry_type=DISBURSEMENT))
        else:
            time_entries = self.time_entries.filter(
                Q(entry_type=DISBURSEMENT) | Q(entry_type=FIXED_PRICE_ITEM))

        return Decimal(reduce(
            Invoice.calculate_value(attr="billed_value"),
            time_entries,
            0
        ))

    @property
    def is_paid(self):
        return bool(self.net_outstanding <= Decimal(0.00))

    @property
    def due_date(self):
        days = self.payment_terms.days_offset
        return self.created_date + timedelta(days=days)

    @property
    def can_send_xero(self):
        return self.status.name == 'Printed' and self.time_entries.count() > 0

    @property
    def is_in_xero(self):
        return self.status.name == 'In Xero'

    def send_to_xero(self):
        try:
            xero = get_xero_client()

            res = self.matter.client.create_or_update_xero_contact()

            if not res.get('success'):
                return {'success': False, 'error': res.get('error')}

            invoice_data = prepare_xero_invoice_param(self)

            if self.xero_invoice_id:
                invoice_data['InvoiceID'] = self.xero_invoice_id
                xero.invoices.save(invoice_data)

            else:
                xero_invoice = xero.invoices.put(invoice_data)[0]
                self.xero_invoice_id = xero_invoice.get('InvoiceID')

            self.status = InvoiceStatus.objects.get(name='In Xero')
            self.save()

            return {'success': True}

        except Exception as e:
            print(str(e))
            return {'success': False, 'error': 'Failed to create invoice in Xero'}

    def delete_in_xero(self):
        try:
            if self.received_payments > 0:
                return {'success': False, 'error': 'This invoice already has payments'}

            if not self.is_in_xero:
                return {'success': True}

            xero = get_xero_client()
            res = xero.invoices.filter(InvoiceID=self.xero_invoice_id)

            if res:
                xero_invoice = res[0]

                if xero_invoice.get('AmountPaid') > 0:
                    return {'success': False, 'error': 'This invoice already has payments'}
                else:
                    xero_invoice['Status'] = 'VOIDED'
                    xero.invoices.save(xero_invoice)

            return {'success': True}

        except Exception as e:
            print(str(e))
            return {'success': False, 'error': 'Failed to delete invoice'}

    def can_update(self):
        try:
            if self.received_payments > 0:
                return {'success': False, 'error': 'This invoice already has payments'}

            if not self.is_in_xero:
                return {'success': True}

            xero = get_xero_client()
            res = xero.invoices.filter(InvoiceID=self.xero_invoice_id)

            if res:
                xero_invoice = res[0]

                if xero_invoice.get('AmountPaid') > 0:
                    return {'success': False, 'error': 'This invoice already has payments'}

            return {'success': True}

        except Exception as e:
            print(str(e))
            return {'success': False, 'error': 'This invoice can not be updated'}

    def fetch_payments_from_xero(self):
        try:
            if not self.xero_invoice_id:
                return {'success': True}

            xero = get_xero_client()
            xero_payments = xero.payments.filter(Invoice_InvoiceID=self.xero_invoice_id)

            if not xero_payments:
                return {'success': True}

            for xero_payment in xero_payments:
                status = xero_payment.get('Status')

                payment_data = {
                    'xero_payment_id': xero_payment.get('PaymentID'),
                    'amount': xero_payment.get('Amount'),
                    'date': xero_payment.get('Date'),
                }

                method = get_payment_method(xero_payment.get('Reference'))
                if method:
                    payment_data['method'] = method

                payment = self.payments.filter(xero_payment_id=xero_payment.get('PaymentID')).first()

                if not payment and status != 'DELETED':
                    self.payments.create(**payment_data)
                elif payment and status != 'DELETED':
                    payment.update(**payment_data)
                elif payment and status == 'DELETED':
                    payment.delete()

            return {'success': True}

        except Exception as e:
            print(str(e))
            return {'success': False, 'error': 'Failed to fetch payments from xero'}

    def save(self, *args, **kwargs):
        self.is_invoice_paid = self.is_paid
        super().save(*args, **kwargs)


class Payment(models.Model, UpdateAttributesMixin):
    METHODS = ((1, 'EFT'), (2, 'BPAY'),
               (3, 'Credit Card'), (4, 'Cheque'), (5, 'Trust Account'),
               (6, 'Trust Clearing Account'), (7, 'Cash'), (8, 'Write Off')
               )

    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.IntegerField(choices=METHODS, null=True)
    invoice = models.ForeignKey(
        Invoice, related_name='payments', on_delete=models.CASCADE)
    xero_payment_id = models.CharField(max_length=256, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return "{} - {}".format(self.date, self.amount)


class PaymentTerms(models.Model):
    days_offset = models.IntegerField(default=14)

    def __str__(self):
        return "Payment Term - {} days".format(self.days_offset)

    class Meta:
        verbose_name_plural = "payment terms"
