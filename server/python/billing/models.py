from datetime import datetime
from decimal import Decimal
from functools import reduce

from accounts.models import Contact
from sitename.mixins import UpdateAttributesMixin
from django.db import models
from django.db.models import DecimalField, F, Sum
from django.db.models.functions import Coalesce
from simple_history.models import HistoricalRecords

from core.models import AccountNumber

from .querysets import TimeEntryQuerySet

GST_STATUSES = ((1, 'GST (10%)'), (2, 'GST Export (0%)'),
                (3, 'BAS Excluded (0%)'))

STATUSES = ((1, 'Billable'), (2, 'Non billable'))
MATTER_STATUSES = ((1, 'Active - High (70+ units)'),
                   (2, 'Active - Moderate (30-70 units)'),
                   (3, 'Active - Low (0-30 units)'),
                   (4, 'Waiting for Internal review'),
                   (5, 'Waiting for AA review'),
                   (6, 'Waiting for external party to respond'),
                   (7, 'Ad hoc Work'),
                   (8, 'Need to be billed'), (9, 'Matter Closed'),
                   (10, 'Business Building'))
TIME_ENTRY = 1
DISBURSEMENT = 2
FIXED_PRICE_ITEM = 3
TWOPLACES = Decimal(10) ** -2


class Matter(models.Model, UpdateAttributesMixin):
    CONFLICT_STATUSES = ((1, 'Outstanding'),
                         (2, 'No other parties'), (3, 'Complete'))
    BILLING_METHODS = ((1, 'Fixed price'), (2, 'Time Entry'))
    BILLABLE_STATUSES = ((1, 'Open'), (2, 'Suspended'), (3, 'Closed'))

    name = models.CharField(max_length=150)
    client = models.ForeignKey(
        'accounts.Client',
        related_name='matters',
        null=True,
        on_delete=models.SET_NULL
    )
    description = models.TextField()
    matter_type = models.ForeignKey(
        'core.MatterType',
        related_name='matters',
        null=True,
        on_delete=models.SET_NULL
    )
    matter_sub_type = models.ForeignKey(
        'core.MatterSubType',
        related_name='matters',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    principal = models.ForeignKey(
        'accounts.User',
        related_name='principal_of_matters',
        null=True,
        on_delete=models.SET_NULL
    )
    manager = models.ForeignKey(
        'accounts.User',
        related_name='manager_of_matters',
        null=True,
        on_delete=models.SET_NULL
    )
    assistant = models.ForeignKey(
        'accounts.User',
        related_name='assistant_of_matters',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    conflict_status = models.IntegerField(choices=CONFLICT_STATUSES)
    conflict_parties = models.TextField(null=True, blank=True)
    created_date = models.DateField(auto_now=False, null=True, blank=True)
    closed_date = models.DateField(auto_now=False, null=True, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    billing_method = models.IntegerField(choices=BILLING_METHODS)
    billable_status = models.IntegerField(choices=BILLABLE_STATUSES)
    funds_in_trust = models.BooleanField(default=False)
    history = HistoricalRecords()
    matter_status = models.ForeignKey(
        'core.MatterStatus',
        default=3,
        on_delete=models.SET_DEFAULT
    )
    file_path = models.CharField(max_length=250, null=True, blank=True)
    conflict_check_sent = models.CharField(
        max_length=100, blank=True, null=True)
    is_conflict_check_sent = models.BooleanField(default=False)
    standard_terms_sent = models.CharField(
        max_length=100, blank=True, null=True)
    is_standard_terms_sent = models.BooleanField(default=False)
    referrer_thanked = models.CharField(max_length=100, blank=True, null=True)
    is_referrer_thanked = models.BooleanField(default=False)
    lead_date = models.DateField(auto_now=False, null=True, blank=True)
    lead_status = models.ForeignKey(
        'core.LeadStatus',
        default=1,
        on_delete=models.SET_DEFAULT
    )
    entry_type = models.ForeignKey(
        'billing.EntryType',
        default=1,
        on_delete=models.SET_DEFAULT
    )
    is_matter_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def total_time_invoiced(self, gst=False):
        return self.time_entries.filter(
            entry_type=TIME_ENTRY, invoice__isnull=False).cost(gst=gst)

    def total_invoiced_value(self, gst=False):
        return reduce(
            (lambda x, y: x + y.value(gst=gst)),
            self.invoices.all(),
            0
        )

    @property
    def unbilled_time(self):
        return self.time_entries.filter(invoice=None)

    @property
    def may_close(self):
        return not bool(
            reduce((lambda x, y: x + y.cost), self.unbilled_time, 0)
        )

    @property
    def total_time_value(self):
        return self.time_entries.filter(entry_type=TIME_ENTRY
                                        ).cost(gst=False, billable=True)

    @property
    def total_disbursements_value(self):
        result = self.time_entries.filter(
            entry_type=DISBURSEMENT
        ).annotate(entry_rate=Coalesce('rate', 'staff_member__rate')
                   ).aggregate(total=Sum(F('entry_rate') * F('units_to_bill'),
                                         output_field=DecimalField())
                               ).get('total')

        return result and result.quantize(TWOPLACES) or 0

    @property
    def wip(self):
        if self.billing_method is 1:
            total_time_value = self.time_entries.filter(
                entry_type=TIME_ENTRY, status=1).cost()
            result = Decimal(total_time_value) - self.total_time_invoiced()
        else:
            result = Decimal(self.total_time_value - max(
                self.total_time_value, self.total_invoiced_value()
            )) + self.unbilled_time.cost()

        if result < 0:
            return 0

        return result

    @property
    def received_payments(self):
        return self.invoices.aggregate(total=Sum('payments__amount')
                                       ).get('total') or 0

    @property
    def amount_outstanding(self):
        return Decimal(sum([inv.net_outstanding for inv in self.invoices.all()]))

    @property
    def is_paid(self):
        return False not in [inv.is_invoice_paid for inv in self.invoices.all()]

    @property
    def days_open(self):
        if self.entry_type_id == 1:
            try:
                return (datetime.now().date() - self.created_date).days
            except TypeError:
                return (datetime.now().date() - self.created_date.date()).days
        elif self.entry_type_id == 2:
            try:
                return (datetime.now().date() - self.lead_date).days
            except TypeError:
                return (datetime.now().date() - self.lead_date.date()).days
        else:
            return 0

    def matter_status_display(self):
        return [i[1] for i in MATTER_STATUSES if i[0] == self.matter_status][0]

    def save(self, *args, **kwargs):
        self.is_matter_paid = self.is_paid
        super().save(*args, **kwargs)


class TimeEntry(models.Model, UpdateAttributesMixin):
    ENTRY_TYPES = ((TIME_ENTRY, 'Time Entry'), (DISBURSEMENT, 'Disbursement'),
                   (FIXED_PRICE_ITEM, 'Fixed Price Item'))

    description = models.TextField()
    client = models.ForeignKey(
        'accounts.Client',
        related_name='time_entries',
        null=True,
        on_delete=models.SET_NULL
    )
    staff_member = models.ForeignKey(
        'accounts.User',
        related_name='time_entries',
        null=True,
        on_delete=models.SET_NULL
    )
    matter = models.ForeignKey(
        Matter,
        related_name='time_entries',
        null=True,
        on_delete=models.SET_NULL
    )
    invoice = models.ForeignKey(
        'invoicing.Invoice',
        related_name='time_entries',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    date = models.DateTimeField()
    units = models.FloatField()
    units_to_bill = models.FloatField()
    status = models.IntegerField(choices=STATUSES, null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    gst_status = models.IntegerField(choices=GST_STATUSES, null=True)
    entry_type = models.IntegerField(choices=ENTRY_TYPES)
    time_entry_type = models.ForeignKey(
        'core.TimeEntryType',
        default=1,
        on_delete=models.SET_DEFAULT
    )

    objects = TimeEntryQuerySet.as_manager()

    class Meta:
        ordering = ['date']
        verbose_name_plural = "Time Entries"

    @property
    def cost(self):
        if self.rate is not None:
            if self.entry_type == TIME_ENTRY:
                return self.rate * Decimal(self.units_to_bill) / 10
            else:
                return self.rate * Decimal(self.units_to_bill)
        elif self.staff_member:
            if self.entry_type == TIME_ENTRY:
                return self.staff_member.rate * Decimal(self.units_to_bill) / 10
            else:
                return self.staff_member.rate * Decimal(self.units_to_bill)

        return 0

    @property
    def billable_value(self):
        return self.billed_rate * Decimal(self.units) / \
            (10 if self.entry_type == TIME_ENTRY else 1)

    @property
    def units_to_pdf(self):
        units = self.units_to_bill if self.units_to_bill else self.units
        return int(units)

    @property
    def billed_value(self):
        if not self.invoice:
            return 0
        if self.invoice.time_entry_value != 0:
            return Decimal(
                self.invoice.fixed_price_value
                / self.invoice.time_entry_value * self.cost
            )
        elif self.cost != 0:
            return Decimal(self.invoice.fixed_price_value / self.cost)
        else:
            return Decimal(self.invoice.fixed_price_value)

    @property
    def xero_gst_status(self):
        XERO_GST_STATUS = ['OUTPUT', 'EXEMPTEXPORT', 'BASEXCLUDED']
        return XERO_GST_STATUS[self.gst_status - 1]

    @property
    def xero_entry_type(self):
        return self.get_entry_type_display()

    @property
    def xero_account_number(self):
        account_numbers = AccountNumber.objects.filter(entry_type=self.entry_type, gst_status=self.gst_status)
        if account_numbers.exists():
            return account_numbers.first().account_number
        else:
            return 200

    @property
    def billed_rate(self):
        if self.staff_member:
            rate = self.staff_member.rate
        elif self.rate:
            rate = self.rate
        else:
            rate = 0

        return rate

    def __str__(self):
        return self.description


class StandartDisbursement(models.Model):
    name = models.CharField(max_length=80, null=True)
    description = models.TextField()
    cost = models.FloatField(null=True)
    gst_status = models.IntegerField(choices=GST_STATUSES, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Standard Disbursement"
        verbose_name_plural = "Standard Disbursements"


class Note(models.Model):
    matter = models.ForeignKey(
        Matter,
        related_name='notes',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    contact = models.ForeignKey(
        Contact,
        related_name='notes',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    date_time = models.DateTimeField(null=True)
    text = models.TextField()
    user = models.ForeignKey(
        'accounts.User',
        related_name='notes',
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.matter.name


class EntryType(models.Model):
    name = models.CharField(max_length=80, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Entry Types"
