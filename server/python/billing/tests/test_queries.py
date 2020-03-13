import pytest

from sitename.schema import schema
from graphene.test import Client
from accounts.factories import UserFactory
from ..factories import (MatterFactory, NoteFactory, TimeEntryFactory,
                         StandartDisbursementFactory)


@pytest.mark.django_db
def test_standart_disbursements_query(snapshot, request):
    """ Test get standart disbursements query"""

    StandartDisbursementFactory.create_batch(size=4)

    staff_member = UserFactory(id=1)
    request.user = staff_member

    client = Client(schema, context=request)
    query = client.execute("""
        query getStandartDisbursements {
            standartDisbursements(first: 3) {
                edges {
                    node {
                        gstStatus
                    }
                }
            }
        }
    """)
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_time_entries_query(snapshot, request):
    """ Test get time entries query"""

    staff_member = UserFactory(id=1)
    TimeEntryFactory.create_batch(
        size=1,
        rate=0,
        status=1,
        gst_status=0,
        units_to_bill=25,
        staff_member=staff_member,
    )

    TimeEntryFactory.create_batch(
        size=1,
        rate=0,
        status=1,
        gst_status=0,
        units_to_bill=25,
        staff_member=None,
    )

    TimeEntryFactory.create_batch(
        size=1,
        rate=503.40,
        status=1,
        gst_status=0,
        units_to_bill=25,
        staff_member=staff_member,
    )

    request.user = staff_member
    client = Client(schema, context=request)
    query = client.execute("""
        query getTimeEntries {
            timeEntries(first: 3) {
                edges {
                    node {
                         statusDisplay
                         gstStatus
                         gstStatusDisplay
                         cost
                         status
                         billedValue
                         rate
                         isBilled
                         entryType
                    }
                }
            }
        }
    """)
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_matters_query(snapshot, request):
    """ Test get matters query"""

    MatterFactory.create_batch(size=4)

    staff_member = UserFactory(id=1)
    request.user = staff_member
    client = Client(schema, context=request)
    query = client.execute("""
        query matters {
            matters(first: 3) {
                edges {
                    node {
                         conflictStatus
                         billableStatus
                         billableStatusDisplay
                         billingMethod
                         totalTimeValue
                         unbilledTime {
                            billedValue
                         }
                         totalTimeInvoiced
                         wip
                         amountOutstanding
                         isPaid
                         daysOpen
                         notes{
                            text
                         }
                         matterStatus
                         matterStatusDisplay
                         lastNote{
                            text
                         }
                         totalInvoicedValue
                    }
                }
            }
        }
    """)
    snapshot.assert_match(query)
