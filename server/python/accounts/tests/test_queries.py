import pytest

from sitename.schema import schema
from graphene.test import Client
from billing.factories import NoteFactory

from ..factories import (ClientFactory, ContactFactory, LocationFactory,
                         OrganisationFactory, UserFactory)

from graphql_relay.node.node import to_global_id


@pytest.mark.django_db
def test_users_query(snapshot, request):
    """ Test users query """

    users = UserFactory.create_batch(size=3)
    users[0].location = LocationFactory()

    staff_member = UserFactory(id=1)
    request.user = staff_member
    client = Client(schema, context=request)
    query = client.execute("""
        query getUsers {
            users(first:3) {
                edges {
                    node{
                        fullName
                        photo
                        salutation
                        location {
                             state
                             stateDisplay
                             country
                        }
                        postalLocation{
                             state
                             stateDisplay
                             country
                        }
                        rate
                        groups
                        hasGmailAccount
                        pointer
                        addressesAreEquals
                    }
                }
            }
        }
    """)
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_clients_query(snapshot, request):
    """ Test clients query """

    clients = ClientFactory.create_batch(size=3)
    clients[0].organisation = None

    client = Client(schema)
    query = client.execute("""
        query getClients {
            clients(first:3) {
                edges {
                    node{
                        name
                        organisation{
                            name
                        }
                        secondContact{
                            fullName
                        }
                        invoicingAddress
                        mattersCount
                        matters(excludeStatus:1) {
                            edges {
                                node {
                                    id
                                }
                            }
                        }
                        streetAddress
                    }
                }
            }
        }
    """)
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_clients_query_with_address_data(snapshot, request):
    """ Test clients query with address """

    clients = ClientFactory.create_batch(size=3)
    clients[0].organisation = None

    client = Client(schema)
    query = client.execute("""
        query getClients {
            clients(first:3) {
                edges {
                    node{
                        name
                        invoicingAddress
                        streetAddress
                    }
                }
            }
        }
    """)
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_get_me_query(snapshot, request):
    """ Test get me query """

    staff_member = UserFactory(id=1)
    request.user = staff_member
    client = Client(schema, context=request)
    query = client.execute("""
        query getMe {
            me {
                id
                fullName
            }
        }
    """)
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_get_contacts_query(snapshot, request):
    """ Test get contacts query """

    ContactFactory.create_batch(size=10)

    staff_member = UserFactory(id=1)
    request.user = staff_member
    client = Client(schema, context=request)
    query = client.execute("""
        query getContacts {
            contacts(first:3) {
                edges {
                    node{
                        fullName
                        salutation
                        occupation
                        notes {
                            text
                        }
                        lastNote {
                            text
                        }
                        spouse {
                            fullName
                        }
                        secondContact {
                            fullName
                        }
                        children{
                            fullName
                        }
                    }
                }
            }
        }
    """)
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_get_contacts_query_with_all_flag(snapshot, request):
    """ Test get contacts query with all flag """

    ContactFactory.create_batch(size=10)

    staff_member = UserFactory(id=1)
    request.user = staff_member
    client = Client(schema, context=request)
    query = client.execute("""
        query getContacts($all:Boolean!) {
            contacts(first:3, all:$all) {
                edges {
                    node{
                        id
                    }
                }
            }
        }
    """, variable_values={
            'all': True,
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_get_contacts_query_with_all_extra_data(snapshot, request):
    """ Test get contacts query with all extra data """

    contacts = ContactFactory.create_batch(size=10)

    staff_member = UserFactory(id=1)
    request.user = staff_member
    client = Client(schema, context=request)
    query = client.execute("""
        query getContacts($all:Boolean!, $exclude: ID!) {
            contacts(first:3, all:$all, exclude: $exclude) {
                edges {
                    node{
                        id
                    }
                }
            }
        }
    """, variable_values={
            'all': True,
            'exclude': contacts[0].id,
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_get_contacts_query_with_exclude(snapshot, request):
    """ Test get contacts query with exclude value """

    contacts = ContactFactory.create_batch(size=10)

    staff_member = UserFactory(id=1)
    request.user = staff_member
    client = Client(schema, context=request)
    query = client.execute("""
        query getContacts($exclude: ID!) {
            contacts(first:3, exclude:$exclude) {
                edges {
                    node{
                        id
                    }
                }
            }
        }
    """, variable_values={
            'exclude': contacts[0].id,
        })

    snapshot.assert_match(query)


@pytest.mark.django_db
def test_get_organisations_query(snapshot, request):
    """ Test get organisations query """

    organisation = OrganisationFactory(group_status=1)

    staff_member = UserFactory(id=1)
    request.user = staff_member
    client = Client(schema, context=request)
    query = client.execute("""
        query organisation($id: ID!) {
            organisation(id: $id) {
              id
            name
            website
            mainLine
            businessSearchWords
            industry {
              id
              name
            }
            groupStatus
            groupParent {
              id
              name
            }
            addressesAreEquals
            location {
              id
              address1
              address2
              state
              postCode
              country
              suburb
              stateDisplay
            }
            postalLocation {
              id
              postalAddress1
              postalAddress2
              postalSuburb
              postalState
              postalPostCode
              postalCountry
            }
            contacts {
              edges {
                cursor
                node {
                  id
                  fullName
                  secondContact {
                    id
                    fullName
                  }
                }
              }
            }
          }
        }
    """, variable_values={
            'id': to_global_id('OrganisationType', organisation.id),
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_get_organisation_detail_query(snapshot, request):
    """ Test get legal query """

    UserFactory.create_batch(size=2, is_legal=True)

    client = Client(schema)
    query = client.execute("""
        query getLegal {
            legal(first:3) {
                edges {
                    node{
                        id
                    }
                }
            }
        }
    """)
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_get_notes_query(snapshot, request):
    """ Test get notes query """

    contact = ContactFactory()
    NoteFactory.create_batch(size=10, contact=contact)

    client = Client(schema)
    query = client.execute("""
        query getNotes($contactId: ID!) {
            notes(contactId: $contactId) {
                id
                text
            }
        }
    """, variable_values={
            'contactId': contact.id,
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_get_legal_query(snapshot, request):
    """ Test get legal query """

    UserFactory.create_batch(size=2, is_legal=True)

    client = Client(schema)
    query = client.execute("""
        query getLegal {
            legal(first:3) {
                edges {
                    node{
                        id
                    }
                }
            }
        }
    """)
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_staff_query(snapshot):
    """Test staff query"""

    UserFactory.create_batch(size=2, is_staff=True)

    client = Client(schema)
    executed = client.execute("""
      query matterStaff($fullName: String, $skip: Boolean!) {
        users(fullName: $fullName) @skip(if: $skip) {
          edges {
            cursor
            node {
              id
              fullName
            }
          }
        }
      }
    """, variable_values={
        "fullName": "johnson",
        "skip": False,
    })
    snapshot.assert_match(executed)
