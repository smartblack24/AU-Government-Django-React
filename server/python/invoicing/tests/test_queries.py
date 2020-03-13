import pytest

from datetime import datetime, date
from decimal import Decimal

from accounts.factories import ClientFactory, UserFactory, ContactFactory
from graphene.test import Client
from sitename.schema import schema
from billing.factories import MatterFactory, TimeEntryFactory
from ..factories import InvoiceFactory, PaymentFactory, PaymentTermsFactory


@pytest.mark.django_db
def test_invoices_query(snapshot, request):
    """ Test invoices query"""

    client_instance = ClientFactory()

    matter_instance = MatterFactory(
        client=client_instance,
    )

    InvoiceFactory(id=1231, matter=matter_instance)
    InvoiceFactory(id=4322, matter=matter_instance)
    InvoiceFactory(id=3233, matter=matter_instance)

    staff_member = UserFactory(id=1)
    request.user = staff_member

    client = Client(schema, context=request)
    query = client.execute("""
        query getInvoices {
            invoices(first: 3) {
                edges {
                    node {
                        statusDisplay
                        valueExGst
                        valueInclGst
                        receivedPayments
                        netOutstanding
                        history
                        totalBilledValue
                        isPaid
                        dueDate
                        number
                        friendlyReminder
                        firstReminder
                        secondReminder
                        timeEntries{
                            edges{
                                node{
                                    description
                                }
                            }
                        }
                        billingMethod
                        timeEntryValue
                        fixedPriceValue
                        canSendXero
                        isInXero
                    }
                }
            }
        }
    """)
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_invoices_query_with_incorrect_due_date(snapshot, request):
    """ Test invoices query with incorrect dueDate"""

    payment_terms = PaymentTermsFactory(days_offset=1)

    InvoiceFactory(
        payment_terms=payment_terms,
        created_date=date.today()
    )

    InvoiceFactory(
        payment_terms=payment_terms,
        created_date=datetime.now()
    )

    staff_member = UserFactory(id=1)
    request.user = staff_member

    client = Client(schema, context=request)
    query = client.execute("""
        query getInvoices {
            invoices(first: 3) {
                edges {
                    node {
                        friendlyReminder
                        firstReminder
                        secondReminder
                    }
                }
            }
        }
    """)
    snapshot.assert_match(query)
