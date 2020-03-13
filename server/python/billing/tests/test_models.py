from decimal import Decimal

import pytest
from functools import reduce

from django.db.models import DecimalField, F, Sum
from ..factories import MatterFactory, TimeEntryFactory
from accounts.factories import UserFactory

TWOPLACES = Decimal(10) ** -2


@pytest.mark.django_db
def test_matter():
    """ Test Matter model """

    matter = MatterFactory(
    )
    time_entries = TimeEntryFactory.create_batch(
        10,
        rate=Decimal('200.00'),
        units=12
        )
    disbursements = TimeEntryFactory.create_batch(2, entry_type=2)
    matter.time_entries.add(*time_entries)
    matter.time_entries.add(*disbursements)

    assert list(matter.unbilled_time) == [*time_entries, *disbursements]
    assert matter.may_close is False
    assert matter.total_time_value == Decimal(sum(
        [time.units * time.rate / 10 for time in time_entries])
        ).quantize(TWOPLACES)
    assert matter.total_disbursements_value == sum(
        [disb.units_to_bill * disb.rate for disb in disbursements]
        )

    matter.entry_type_id = 1
    assert matter.days_open == 0
    assert str(matter) == matter.name

    assert matter.total_invoiced_value(gst=False) == reduce(
        (lambda x, y: x + y.value(gst=gst)),
        matter.invoices.all(),
        0
    )

    assert matter.total_time_invoiced(gst=False) == matter.time_entries.filter(
        entry_type=2, invoice__isnull=False).cost(gst=False)

    matter.billing_method = 1
    total_time_value = matter.time_entries.filter(
            entry_type=1,
            status=1
    ).cost()

    result = Decimal(total_time_value) - matter.total_time_invoiced()
    assert matter.wip == result

    assert matter.received_payments == 0

    assert matter.amount_outstanding == Decimal(
        sum([inv.net_outstanding for inv in matter.invoices.all()]))

    assert matter.is_paid is True or False


@pytest.mark.django_db
def test_time_entry():
    """ Test TimeEntry model """

    user = UserFactory(rate=Decimal('100.00'))
    time_entry = TimeEntryFactory(rate=Decimal('100.00'), staff_member=user)
    result = time_entry.staff_member.rate * \
        Decimal(time_entry.units_to_bill)
    assert time_entry.cost == Decimal(result / 10)

    assert time_entry.billable_value == time_entry.staff_member.rate * \
        Decimal(time_entry.units) / 10

    time_entry = TimeEntryFactory(
        rate=Decimal('100.00'),
        entry_type=2,
        staff_member=user
        )
    assert time_entry.cost == time_entry.staff_member.rate * \
        Decimal(time_entry.units_to_bill)

    assert time_entry.billable_value == time_entry.staff_member.rate * \
        Decimal(time_entry.units)

    time_entry = TimeEntryFactory(rate=Decimal('100.00'), staff_member=None)
    assert time_entry.cost == Decimal('100.00') * \
        Decimal(time_entry.units_to_bill) / 10

    time_entry = TimeEntryFactory(rate=Decimal('0.00'), staff_member=None)
    assert time_entry.cost == 0
