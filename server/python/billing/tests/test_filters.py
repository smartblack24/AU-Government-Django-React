import pytest

from sitename.schema import schema
from graphene.test import Client
from accounts.models import Contact
from accounts.factories import (ClientFactory, ContactFactory, LocationFactory,
                                OrganisationFactory, UserFactory)
from ..factories import MatterFactory, NoteFactory, TimeEntryFactory


@pytest.mark.django_db
def test_matters_client_name_filter(snapshot, request):
    """ Test matters client name filter with organisations and contacts name """

    client_instance = ClientFactory(
        organisation=OrganisationFactory(name='organisation'),
        contact=ContactFactory(
            first_name='first',
            last_name='contact'
        ),
        second_contact=None
    )

    MatterFactory.create_batch(
        size=5,
        client=client_instance,
    )

    staff_member = UserFactory(id=1)
    request.user = staff_member

    client = Client(schema, context=request)
    query = client.execute("""
        query getMatters($clientName: String) {
            matters(first: 3, clientName: $clientName) {
                edges {
                    node {
                        id
                        name
                        client {
                            id
                            name
                        }
                        billableStatus
                    }
                }
            }
        }
    """, variable_values={
            'clientName': client_instance.name,
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_matters_client_name_filter_with_not_full_client_name(snapshot, request):
    """ Test matters client name filter with contacts name """

    client_instance = ClientFactory(
        organisation=None,
        contact=ContactFactory(
            first_name='first',
            last_name='contact'
        ),
        second_contact=None
    )

    MatterFactory.create_batch(
        size=5,
        client=client_instance,
    )

    staff_member = UserFactory(id=1)
    request.user = staff_member

    client = Client(schema, context=request)
    query = client.execute("""
        query getMatters($clientName: String) {
            matters(first: 3, clientName: $clientName) {
                edges {
                    node {
                        id
                        name
                        client {
                            id
                            name
                        }
                        billableStatus
                    }
                }
            }
        }
    """, variable_values={
            'clientName': client_instance.name,
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_matters_client_name_filter_with_value_error(snapshot, request):
    """ Test matters client name filter with value error """

    client_instance = ClientFactory(
        organisation=None,
        contact=ContactFactory(
            first_name='name',
            last_name='name'
        ),
        second_contact=None
    )

    MatterFactory.create_batch(
        size=5,
        client=client_instance,
    )

    staff_member = UserFactory(id=1)
    request.user = staff_member

    client = Client(schema, context=request)
    query = client.execute("""
        query getMatters($clientName: String) {
            matters(first: 3, clientName: $clientName) {
                edges {
                    node {
                        id
                        name
                        client {
                            id
                            name
                        }
                        billableStatus
                    }
                }
            }
        }
    """, variable_values={
            'clientName': 'name',
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_matters_principal_name_filter(snapshot, request):
    """ Test matters principal name filter """

    user_instance = UserFactory(
        first_name='first',
        last_name='last'
    )

    MatterFactory.create_batch(
        size=5,
        principal=user_instance,
    )

    staff_member = UserFactory(id=1)
    request.user = staff_member

    client = Client(schema, context=request)
    query = client.execute("""
        query getMatters($principalName: String) {
            matters(first: 3, principalName: $principalName) {
                edges {
                    node {
                        id
                        name
                        client {
                            id
                            name
                        }
                        billableStatus
                    }
                }
            }
        }
    """, variable_values={
            'principalName': user_instance.full_name,
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_matters_principal_name_filter_with_value_error(snapshot, request):
    """ Test matters principal name filter with value error """

    user_instance = UserFactory(
        first_name='name',
        last_name='name'
    )

    MatterFactory.create_batch(
        size=5,
        principal=user_instance,
    )

    staff_member = UserFactory(id=1)
    request.user = staff_member

    client = Client(schema, context=request)
    query = client.execute("""
        query getMatters($principalName: String) {
            matters(first: 3, principalName: $principalName) {
                edges {
                    node {
                        id
                        name
                        client {
                            id
                            name
                        }
                        billableStatus
                    }
                }
            }
        }
    """, variable_values={
            'principalName': 'name',
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_matters_manager_name_filter(snapshot, request):
    """ Test matters manager name filter """

    user_instance = UserFactory(
        first_name='first',
        last_name='last'
    )

    MatterFactory.create_batch(
        size=5,
        manager=user_instance,
    )

    staff_member = UserFactory(id=1)
    request.user = staff_member

    client = Client(schema, context=request)
    query = client.execute("""
        query getMatters($managerName: String) {
            matters(first: 3, managerName: $managerName) {
                edges {
                    node {
                        id
                        name
                        client {
                            id
                            name
                        }
                        billableStatus
                    }
                }
            }
        }
    """, variable_values={
            'managerName': user_instance.full_name,
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_matters_manager_name_filter_with_value_error(snapshot, request):
    """ Test matters manager name filter with value error """

    user_instance = UserFactory(
        first_name='name',
        last_name='name'
    )

    MatterFactory.create_batch(
        size=5,
        manager=user_instance,
    )

    staff_member = UserFactory(id=1)
    request.user = staff_member

    client = Client(schema, context=request)
    query = client.execute("""
        query getMatters($managerName: String) {
            matters(first: 3, managerName: $managerName) {
                edges {
                    node {
                        id
                        name
                        client {
                            id
                            name
                        }
                        billableStatus
                    }
                }
            }
        }
    """, variable_values={
            'managerName': 'name',
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_matters_staff_name_filter(snapshot, request):
    """ Test matters staff name filter """

    user_instance = UserFactory(
        first_name='first',
        last_name='last'
    )

    MatterFactory.create_batch(
        size=5,
        principal=user_instance,
    )

    staff_member = UserFactory(id=1)
    request.user = staff_member

    client = Client(schema, context=request)
    query = client.execute("""
        query getMatters($staffName: String) {
            matters(first: 3, staffName: $staffName) {
                edges {
                    node {
                        id
                        name
                        client {
                            id
                            name
                        }
                        billableStatus
                    }
                }
            }
        }
    """, variable_values={
            'staffName': user_instance.full_name,
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_matters_staff_name_filter_with_value_error(snapshot, request):
    """ Test matters staff name filter with value error """

    user_instance = UserFactory(
        first_name='name',
        last_name='name'
    )

    MatterFactory.create_batch(
        size=5,
        manager=user_instance,
    )

    staff_member = UserFactory(id=1)
    request.user = staff_member

    client = Client(schema, context=request)
    query = client.execute("""
        query getMatters($staffName: String) {
            matters(first: 3, staffName: $staffName) {
                edges {
                    node {
                        id
                        name
                        client {
                            id
                            name
                        }
                        billableStatus
                    }
                }
            }
        }
    """, variable_values={
            'staffName': 'name',
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_matters_assistant_name_filter(snapshot, request):
    """ Test matters assistant name filter """

    user_instance = UserFactory(
        first_name='first',
        last_name='last'
    )

    MatterFactory.create_batch(
        size=5,
        assistant=user_instance,
    )

    staff_member = UserFactory(id=1)
    request.user = staff_member

    client = Client(schema, context=request)
    query = client.execute("""
        query getMatters($assistantName: String) {
            matters(first: 3, assistantName: $assistantName) {
                edges {
                    node {
                        id
                        name
                        client {
                            id
                            name
                        }
                        billableStatus
                    }
                }
            }
        }
    """, variable_values={
            'assistantName': user_instance.full_name,
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_matters_assistant_name_filter_with_value_error(snapshot, request):
    """ Test matters assistant name filter with value error """

    user_instance = UserFactory(
        first_name='name',
        last_name='name'
    )

    MatterFactory.create_batch(
        size=5,
        assistant=user_instance,
    )

    staff_member = UserFactory(id=1)
    request.user = staff_member

    client = Client(schema, context=request)
    query = client.execute("""
        query getMatters($assistantName: String) {
            matters(first: 3, assistantName: $assistantName) {
                edges {
                    node {
                        id
                        name
                        client {
                            id
                            name
                        }
                        billableStatus
                    }
                }
            }
        }
    """, variable_values={
            'assistantName': 'name',
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_matters_is_paid_filter_with_value_false(snapshot, request):
    """ Test matters is paid filter with valur false """

    MatterFactory.create_batch(
        size=5,
    )

    staff_member = UserFactory(id=1)
    request.user = staff_member

    client = Client(schema, context=request)
    query = client.execute("""
        query getMatters($isPaid: Boolean!) {
            matters(first: 3, isPaid: $isPaid) {
                edges {
                    node {
                        id
                        name
                        client {
                            id
                            name
                        }
                        billableStatus
                    }
                }
            }
        }
    """, variable_values={
            'isPaid': False,
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_matters_is_paid_filter_with_value_true(snapshot, request):
    """ Test matters is paid filter name filter with value true """

    MatterFactory.create_batch(
        size=5,
    )

    staff_member = UserFactory(id=1)
    request.user = staff_member

    client = Client(schema, context=request)
    query = client.execute("""
        query getMatters($isPaid: Boolean!) {
            matters(first: 3, isPaid: $isPaid) {
                edges {
                    node {
                        id
                        name
                        client {
                            id
                            name
                        }
                        billableStatus
                    }
                }
            }
        }
    """, variable_values={
            'isPaid': True,
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_matters_billable_status_exclude_filter(snapshot, request):
    """ Test matters billable status exclude filter """

    MatterFactory.create_batch(
        size=5,
    )

    staff_member = UserFactory(id=1)
    request.user = staff_member

    client = Client(schema, context=request)
    query = client.execute("""
        query getMatters($billableStatusExclude: Float) {
            matters(first: 3, billableStatusExclude: $billableStatusExclude) {
                edges {
                    node {
                        id
                        name
                        client {
                            id
                            name
                        }
                        billableStatus
                    }
                }
            }
        }
    """, variable_values={
            'billableStatusExclude': 1,
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_matter_report_filter_name_filter(snapshot, request):
    """ Test matter report filter """

    user_instance = UserFactory(
        first_name='first',
        last_name='last'
    )

    MatterFactory.create_batch(
        size=5,
        assistant=user_instance,
    )

    staff_member = UserFactory(id=1)
    request.user = staff_member

    client = Client(schema, context=request)
    query = client.execute("""
        query getMatters($matterReport: String) {
            matters(first: 3, matterReport: $matterReport) {
                edges {
                    node {
                        id
                        name
                        client {
                            id
                            name
                        }
                        billableStatus
                    }
                }
            }
        }
    """, variable_values={
            'matterReport': user_instance.full_name,
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_matter_report_filter_with_value_error(snapshot, request):
    """ Test matter report filter with value error """

    user_instance = UserFactory(
        first_name='name',
        last_name='name'
    )

    MatterFactory.create_batch(
        size=5,
        assistant=user_instance,
    )

    staff_member = UserFactory(id=1)
    request.user = staff_member

    client = Client(schema, context=request)
    query = client.execute("""
        query getMatters($matterReport: String) {
            matters(first: 3, matterReport: $matterReport) {
                edges {
                    node {
                        id
                        name
                        client {
                            id
                            name
                        }
                        billableStatus
                    }
                }
            }
        }
    """, variable_values={
            'matterReport': 'name',
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_matter_status_filter(snapshot, request):
    """ Test matter status filter """

    staff_member = UserFactory(id=1)
    request.user = staff_member

    client = Client(schema, context=request)
    query = client.execute("""
        query getMatters($matterStatus: String) {
            matters(first: 3, matterStatus: $matterStatus) {
                edges {
                    node {
                        id
                        name
                        client {
                            id
                            name
                        }
                        billableStatus
                    }
                }
            }
        }
    """, variable_values={
            'matterStatus': '1',
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_time_entries_client_name_filter(snapshot, request):
    """ Test time entries client name filter """

    client_instance = ClientFactory(
        organisation=None,
        contact=ContactFactory(
            first_name='name',
            last_name='name'
        ),
        second_contact=None
    )

    TimeEntryFactory.create_batch(
        size=5,
        client=client_instance,
        date='2017-10-20'
    )

    staff_member = UserFactory(id=1)
    request.user = staff_member

    client = Client(schema, context=request)
    query = client.execute("""
          query timeEntries($clientName: String) {
            timeEntries(first: 3, clientName: $clientName) {
              totalPages
              edges {
                cursor
                node {
                  id
                  description
                  date
                  matter {
                    id
                    name
                  }
                  client {
                    id
                    name
                  }
                }
              }
              pageInfo {
                endCursor
                hasNextPage
              }
            }
          }
    """, variable_values={
            'clientName': client_instance.name,
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_time_entrie_clients_name_filter_with_value_error(snapshot, request):
    """ Test time entries clients name filter with value error """

    client_instance = ClientFactory(
        organisation=None,
        contact=ContactFactory(
            first_name='name',
            last_name='name'
        ),
        second_contact=None
    )

    TimeEntryFactory.create_batch(
        size=5,
        client=client_instance,
        date='2017-10-20'
    )

    staff_member = UserFactory(id=1)
    request.user = staff_member

    client = Client(schema, context=request)
    query = client.execute("""
          query timeEntries($clientName: String) {
            timeEntries(first: 3, clientName: $clientName) {
              totalPages
              edges {
                cursor
                node {
                  id
                  description
                  date
                  matter {
                    id
                    name
                  }
                  client {
                    id
                    name
                  }
                }
              }
              pageInfo {
                endCursor
                hasNextPage
              }
            }
          }
    """, variable_values={
            'clientName': 'name',
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_time_entries_staff_name_filter(snapshot, request):
    """ Test time entries staff name filter """

    user_instance = UserFactory(
        first_name='first',
        last_name='last'
    )

    TimeEntryFactory.create_batch(
        size=5,
        staff_member=user_instance,
        date='2017-10-20'
    )

    staff_member = UserFactory(id=1)
    request.user = staff_member

    client = Client(schema, context=request)
    query = client.execute("""
          query timeEntries($staffName: String) {
            timeEntries(first: 3, staffName: $staffName) {
              totalPages
              edges {
                cursor
                node {
                  id
                  description
                  date
                  matter {
                    id
                    name
                  }
                  client {
                    id
                    name
                  }
                }
              }
              pageInfo {
                endCursor
                hasNextPage
              }
            }
          }
    """, variable_values={
            'staffName': user_instance.full_name,
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_time_entries_staff_name_filter_with_value_error(snapshot, request):
    """ Test time entries staff name filter with value error """

    user_instance = UserFactory(
        first_name='first',
        last_name='last'
    )

    TimeEntryFactory.create_batch(
        size=5,
        staff_member=user_instance
    )

    staff_member = UserFactory(id=1)
    request.user = staff_member

    client = Client(schema, context=request)
    query = client.execute("""
          query timeEntries($staffName: String) {
            timeEntries(first: 3, staffName: $staffName) {
              totalPages
              edges {
                cursor
                node {
                  id
                  description
                  date
                  matter {
                    id
                    name
                  }
                  client {
                    id
                    name
                  }
                }
              }
              pageInfo {
                endCursor
                hasNextPage
              }
            }
          }
    """, variable_values={
            'staffName': 'name',
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_time_entries_is_billed_filter(snapshot, request):
    """ Test time entries is billed filter """

    staff_member = UserFactory(id=1)
    request.user = staff_member

    client = Client(schema, context=request)
    query = client.execute("""
          query timeEntries($isBilled: Boolean) {
            timeEntries(first: 3, isBilled: $isBilled) {
              totalPages
              edges {
                cursor
                node {
                  id
                  description
                  date
                  matter {
                    id
                    name
                  }
                  client {
                    id
                    name
                  }
                }
              }
              pageInfo {
                endCursor
                hasNextPage
              }
            }
          }
    """, variable_values={
            'isBilled': True,
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_time_entries_date_filter(snapshot, request):
    """ Test time entries date filter filter """

    time_entries = TimeEntryFactory.create_batch(
        size=5,
        date='2012-02-20'
    )

    staff_member = UserFactory(id=1)
    request.user = staff_member

    client = Client(schema, context=request)
    query = client.execute("""
          query timeEntries($date: String) {
            timeEntries(first: 3, date: $date) {
              totalPages
              edges {
                cursor
                node {
                  id
                  description
                  date
                  matter {
                    id
                    name
                  }
                  client {
                    id
                    name
                  }
                }
              }
              pageInfo {
                endCursor
                hasNextPage
              }
            }
          }
    """, variable_values={
            'date': '20/02/2012',
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_time_entries_date_filter_with_value_error(snapshot, request):
    """ Test time entries date filter filter with value error """

    TimeEntryFactory.create_batch(
        size=5,
        date='2012-02-20'
    )

    staff_member = UserFactory(id=1)
    request.user = staff_member

    client = Client(schema, context=request)
    query = client.execute("""
          query timeEntries($date: String) {
            timeEntries(first: 3, date: $date) {
              totalPages
              edges {
                cursor
                node {
                  id
                  description
                  date
                  matter {
                    id
                    name
                  }
                  client {
                    id
                    name
                  }
                }
              }
              pageInfo {
                endCursor
                hasNextPage
              }
            }
          }
    """, variable_values={
            'date': '12/20',
        })
    snapshot.assert_match(query)
