import pytest

from sitename.schema import schema
from graphene.test import Client
from accounts.models import Contact
from ..factories import (ClientFactory, ContactFactory, LocationFactory,
                         OrganisationFactory, UserFactory)


@pytest.mark.django_db
def test_contacts_filters(snapshot, request):
    """ Test contact filters """

    ContactFactory.create_batch(
        size=5,
        first_name='first',
        last_name='last'
    )

    staff_member = UserFactory(id=1)
    request.user = staff_member
    client = Client(schema, context=request)
    query = client.execute("""
        query clientContacts($fullName: String) {
            contacts(first: 3, fullName: $fullName) {
                edges {
                    node {
                        id
                        fullName
                        mobile
                    }
                }
            }
        }
    """, variable_values={
            'fullName': 'first last',
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_contacts_filters_with_value_error(snapshot, request):
    """ Test contact filters with value error """

    ContactFactory.create_batch(
        size=5,
        first_name='last',
        last_name='last'
    )

    staff_member = UserFactory(id=1)
    request.user = staff_member
    client = Client(schema, context=request)
    query = client.execute("""
        query clientContacts($fullName: String) {
            contacts(first: 3, fullName: $fullName) {
                edges {
                    node {
                        id
                        fullName
                        mobile
                    }
                }
            }
        }
    """, variable_values={
            'fullName': 'last',
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_client_filters(snapshot):
    """ Test client filters """

    clients = ClientFactory.create_batch(
        size=5,
        organisation=OrganisationFactory(name='organisation'),
        contact=ContactFactory(
            first_name='first',
            last_name='contact'
        ),
        second_contact=None
    )

    client = Client(schema)
    query = client.execute("""
        query getClients($name: String) {
            clients(first: 3, name: $name) {
              totalPages
                edges {
                    node {
                    mattersCount
                    name
                    organisation {
                        id
                        name
                        mainLine
                    }
                    secondContact {
                        id
                        fullName
                        mobile
                    }
                    contact {
                        id
                        fullName
                        mobile
                    }
                }
                cursor
              }
            }
          }
    """, variable_values={
            'name': clients[0].contact.full_name,
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_client_filters_with_value_error(snapshot):
    """ Test client filters with value error """

    ClientFactory.create_batch(
        size=5,
        organisation=OrganisationFactory(name='organisation'),
        contact=ContactFactory(
            first_name='first',
            last_name='contact'
        )
    )

    client = Client(schema)
    query = client.execute("""
        query getClients($name: String) {
            clients(first: 3, name: $name) {
              totalPages
                edges {
                    node {
                        id
                        mattersCount
                        name
                        organisation {
                            id
                            name
                            mainLine
                        }
                        secondContact {
                            id
                            fullName
                            mobile
                        }
                        contact {
                            id
                            fullName
                            mobile
                        }
                    }
                cursor
             }
        }
    }
    """, variable_values={
            'name': 'name',
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_clients_matter_filter_with_true(snapshot):
    """ Test clients matter filters with true"""

    ClientFactory()
    client = Client(schema)

    query = client.execute("""
        query getClients($withMatter: Boolean!) {
            clients(first: 3, withMatter: $withMatter) {
              totalPages
                edges {
                    node {
                        id
                        mattersCount
                        name
                }
                cursor
              }
            }
          }
    """, variable_values={
            'withMatter': True,
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_clients_matter_filter_with_false(snapshot):
    """ Test clients matter filters with false"""

    ClientFactory()
    client = Client(schema)

    query = client.execute("""
        query getClients($withMatter: Boolean!) {
            clients(first: 3, withMatter: $withMatter) {
              totalPages
                edges {
                    node {
                        id
                        mattersCount
                        name
                    }
                cursor
                }
            }
        }
    """, variable_values={
            'withMatter': False,
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_user_filters(snapshot):
    """ Test user filters """

    UserFactory.create_batch(
        size=5,
        first_name='first',
        last_name='last'
    )

    client = Client(schema)
    query = client.execute("""
        query getUsers($fullName: String) {
            users(first: 3, fullName: $fullName) {
                edges {
                    node {
                        id
                        fullName
                        rate
                    }
                }
            }
        }
    """, variable_values={
            'fullName': 'first last',
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_user_filters_with_value_error(snapshot):
    """ Test user filters with value error """

    UserFactory.create_batch(
        size=5,
        first_name='first',
        last_name='last'
    )
    client = Client(schema)

    query = client.execute("""
        query getUsers($fullName: String) {
        users(first: 3, fullName: $fullName) {
            edges {
                node {
                    id
                    fullName
                    rate
                }
            }
        }
    }
    """, variable_values={
            'fullName': 'name',
        })
    snapshot.assert_match(query)
