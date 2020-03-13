import pytest

from datetime import date
from decimal import Decimal

from accounts.factories import ClientFactory, UserFactory
from accounts.models import User
from graphene.test import Client
from sitename.schema import schema
from accounts.factories import (ClientFactory, ContactFactory, LocationFactory,
                                OrganisationFactory, UserFactory)
from core.factories import InvoiceStatusFactory
from billing.factories import MatterFactory, TimeEntryFactory
from ..factories import InvoiceFactory, PaymentFactory, PaymentTermsFactory


@pytest.mark.django_db
def test_invoices_number_or_client_name_filter_with_str(snapshot, request):
    """ Test invoices number or client name filter with string value"""

    client_instance = ClientFactory(
        organisation=None,
        contact=ContactFactory(
            first_name='first',
            last_name='last'
        ),
        second_contact=None
    )

    matter_instance = MatterFactory(
        client=client_instance,
    )

    InvoiceFactory(
        id=6735,
        matter=matter_instance
    )
    InvoiceFactory(
        id=7845,
        matter=matter_instance
    )
    InvoiceFactory(
        id=9965,
        matter=matter_instance
    )

    staff_member = UserFactory(id=1)
    request.user = staff_member

    client = Client(schema, context=request)
    query = client.execute("""
        query getInvoices($numberOrClientName: String) {
            invoices(first: 3, numberOrClientName: $numberOrClientName) {
                edges {
                    node {
                        id
                        matter{
                            id
                            name
                            client {
                                id
                                name
                            }
                        }
                    }
                }
            }
        }
    """, variable_values={
            'numberOrClientName': client_instance.name,
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_invoices_number_or_client_name_filter_with_value_error(snapshot, request):
    """ Test invoices number or client name filter with value error """

    client_instance = ClientFactory(
        organisation=None,
        contact=ContactFactory(
            first_name='name',
            last_name='name'
        ),
        second_contact=None
    )

    matter_instance = MatterFactory(
        client=client_instance,
    )

    InvoiceFactory.create_batch(
        size=1,
        matter=matter_instance
    )

    staff_member = UserFactory(id=1)
    request.user = staff_member

    client = Client(schema, context=request)
    query = client.execute("""
        query getInvoices($numberOrClientName: String) {
            invoices(first: 3, numberOrClientName: $numberOrClientName) {
                edges {
                    node {
                        id
                        matter{
                            id
                            name
                            client {
                                id
                                name
                            }
                        }
                    }
                }
            }
        }
    """, variable_values={
            'numberOrClientName': 'name',
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_invoices_number_or_client_name_filter_with_int(snapshot, request):
    """ Test invoices number or client name filter with integer value"""

    client_instance = ClientFactory(
        organisation=OrganisationFactory(name='organisation'),
        contact=ContactFactory(
            first_name='first',
            last_name='contact'
        ),
        second_contact=None
    )

    matter_instance = MatterFactory(
        client=client_instance,
    )

    InvoiceFactory.create_batch(
        size=3,
        matter=matter_instance
    )

    staff_member = UserFactory(id=1)
    request.user = staff_member

    client = Client(schema, context=request)
    query = client.execute("""
        query getInvoices($numberOrClientName: String) {
            invoices(first: 3, numberOrClientName: $numberOrClientName) {
                edges {
                    node {
                        id
                        matter{
                            id
                            name
                            client {
                                id
                                name
                            }
                        }
                    }
                }
            }
        }
    """, variable_values={
            'numberOrClientName': str(client_instance.id),
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_invoices_is_paid_filter_with_true(snapshot, request):
    """ Test invoices is_paid with true """

    staff_member = UserFactory(id=1)
    request.user = staff_member
    InvoiceFactory.create_batch(
        size=3,
        is_invoice_paid=True
    )

    client = Client(schema, context=request)
    query = client.execute("""
        query getInvoices($isPaid: Boolean) {
            invoices(first: 3, isPaid: $isPaid) {
                edges {
                    node {
                        id
                        matter{
                            id
                            name
                            client {
                                id
                                name
                            }
                        }
                    }
                }
            }
        }
    """, variable_values={
            'isPaid': True,
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_invoices_is_paid_filter_with_false(snapshot, request):
    """ Test invoices is_paid filter with false """

    staff_member = UserFactory(id=1)
    request.user = staff_member
    InvoiceFactory.create_batch(
        size=3,
        is_invoice_paid=False
    )
    client = Client(schema, context=request)
    query = client.execute("""
        query getInvoices($isPaid: Boolean) {
            invoices(first: 3, isPaid: $isPaid) {
                edges {
                    node {
                        id
                        matter{
                            id
                            name
                            client {
                                id
                                name
                            }
                        }
                    }
                }
            }
        }
    """, variable_values={
            'isPaid': False,
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_invoices_status_filter(snapshot, request):
    """ Test invoices status filter """

    staff_member = UserFactory(id=1)
    request.user = staff_member

    invoice_status = InvoiceStatusFactory()
    invoice_instances = InvoiceFactory.create_batch(
        size=3,
        status=invoice_status
    )

    client = Client(schema, context=request)
    query = client.execute("""
        query getInvoices($status: Float) {
            invoices(first: 3, status: $status) {
                edges {
                    node {
                        id
                        matter{
                            id
                            name
                            client {
                                id
                                name
                            }
                        }
                    }
                }
            }
        }
    """, variable_values={
            'status': invoice_instances[0].status.id,
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_invoices_status_filter_with_null_value(snapshot, request):
    """ Test invoices status filter with null value """

    staff_member = UserFactory(id=1)
    request.user = staff_member

    client = Client(schema, context=request)
    query = client.execute("""
        query getInvoices($status: Float) {
            invoices(first: 3, status: $status) {
                edges {
                    node {
                        id
                        matter{
                            id
                            name
                            client {
                                id
                                name
                            }
                        }
                    }
                }
            }
        }
    """, variable_values={
            'status': 0,
        })
    snapshot.assert_match(query)
