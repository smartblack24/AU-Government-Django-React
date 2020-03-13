from datetime import timedelta
from decimal import Decimal
from functools import reduce

import pytest
from sitename.utils import invoice_number
from billing.factories import TimeEntryFactory
from billing.models import DISBURSEMENT, FIXED_PRICE_ITEM, TIME_ENTRY
from django.db.models import Q, Sum, Value
from django.db.models.functions import Coalesce
from integration.models import Xero as XeroIntegration

from ..factories import InvoiceFactory, PaymentFactory, PaymentTermsFactory


@pytest.mark.django_db
def test_invoice():
    """ Test Invoice model """

    invoice = InvoiceFactory(id=6675)
    time_entries = TimeEntryFactory.create_batch(10)
    invoice.id = 5930

    assert str(invoice) == invoice.number

    assert invoice.number == invoice_number(invoice.id)

    invoice = InvoiceFactory()
    invoice.time_entries.add(*time_entries)

    assert list(invoice.recorded_time) == time_entries

    assert invoice.received_payments == invoice.payments.aggregate(
        total=Coalesce(Sum('amount'), Value(0))
    ).get('total')

    assert invoice.net_outstanding == Decimal(
        invoice.value(gst=True) - invoice.received_payments
    )

    assert invoice.time_entry_value == invoice.time_entries.filter(
        Q(entry_type=TIME_ENTRY) | Q(entry_type=DISBURSEMENT)
    ).cost()

    invoice.time_entries.add(*time_entries)

    assert invoice.fixed_price_value == invoice.time_entries.filter(
        Q(entry_type=FIXED_PRICE_ITEM) | Q(entry_type=DISBURSEMENT)
    ).cost()

    invoice.billing_method = 1
    invoice.time_entries.add(*time_entries)

    assert invoice.value(gst=False) == invoice.time_entries.filter(
        Q(entry_type=DISBURSEMENT) | Q(entry_type=FIXED_PRICE_ITEM)
    ).cost(False)

    invoice.time_entries.add(*time_entries)

    assert invoice.total_fixed_price_items_value == invoice.time_entries.filter(
        entry_type=FIXED_PRICE_ITEM
    ).cost()

    assert set(invoice.billing_method_entries) == set(invoice.time_entries.filter(
        Q(entry_type=FIXED_PRICE_ITEM) | Q(entry_type=DISBURSEMENT)
    ))

    invoice.billing_method = 2

    assert invoice.value(gst=False) == invoice.time_entries.filter(
        Q(entry_type=TIME_ENTRY) | Q(entry_type=DISBURSEMENT)
    ).cost(False)

    invoice.time_entries.add(*time_entries)

    assert invoice.total_fixed_price_items_value == invoice.time_entries.filter(
        entry_type=FIXED_PRICE_ITEM
    ).cost()

    assert set(invoice.billing_method_entries) == set(invoice.time_entries.filter(
        Q(entry_type=TIME_ENTRY) | Q(entry_type=DISBURSEMENT)
    ))

    assert invoice.total_billed_value == Decimal(reduce(
        invoice.calculate_value(attr="billed_value"),
        invoice.time_entries.filter(
            Q(entry_type=DISBURSEMENT) | Q(entry_type=FIXED_PRICE_ITEM)
        ),
        0
    ))

    invoice.time_entries.add(*time_entries)

    assert invoice.total_billed_value == Decimal(reduce(
        invoice.calculate_value(attr="billed_value"),
        invoice.time_entries.filter(
            Q(entry_type=TIME_ENTRY) | Q(entry_type=DISBURSEMENT)
        ),
        0
    ))

    assert invoice.is_paid == bool(invoice.net_outstanding <= 0)

    assert invoice.due_date == invoice.created_date + \
        timedelta(days=invoice.payment_terms.days_offset)

    invoice.status.name = 'Printed'
    invoice.time_entries.add(*time_entries)
    assert invoice.can_send_xero is True

    # BLOCK testing invoice models method 'send_to_xero'

    XeroIntegration.objects.create()
    invoice = InvoiceFactory()
    assert invoice.send_to_xero() == {
        'success': False,
        'error': 'Failed to create contact in Xero'
    }

    # ENDBLOCK 'send_to_xero'


@pytest.mark.django_db
def test_payment():
    """ Test Payment model """

    payment = PaymentFactory()

    assert str(payment) == "{} - {}".format(payment.date, payment.amount)


@pytest.mark.django_db
def test_payment_terms():
    """ Test Payment Terms model """

    payment_term = PaymentTermsFactory()

    assert str(payment_term) == "Payment Term - {} days".format(
        payment_term.days_offset
    )
