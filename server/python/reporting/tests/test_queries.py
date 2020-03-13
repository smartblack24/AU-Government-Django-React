import pytest

from datetime import date, timedelta, datetime
from decimal import Decimal
from dateutil import parser

from unittest.mock import patch
from accounts.factories import ClientFactory, UserFactory
from accounts.models import User
from sitename.schema import schema
from billing.factories import MatterFactory, TimeEntryFactory
from core.factories import InvoiceStatusFactory
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from graphene.test import Client
from graphql_relay.node.node import to_global_id
from billing.models import HistoricalMatter
from invoicing.factories import InvoiceFactory, PaymentFactory, PaymentTermsFactory


@pytest.mark.django_db
def test_average_invoice_reports(snapshot, request):
    """ Test success resolve average invoice reports """

    InvoiceFactory(created_date='2015-11-20')
    InvoiceFactory(created_date='2017-01-17')

    from_date = '20-02-2015'
    to_date = '20-12-2017'
    client = Client(schema)
    executed = client.execute("""
        query averageInvoiceReports($fromDate: String, $toDate: String) {
            averageInvoiceReports(fromDate: $fromDate, toDate: $toDate) {
                id
                month
                totalAmount
                totalOutstanding
                averageAmount
                averageOutstanding
            }
        }
    """, variable_values={
            'toDate': to_date,
            'fromDate': from_date,
        },
    )

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_average_invoice_reports_with_the_same_years(snapshot, request):
    """ Test success resolve average invoice reports with the same years """

    InvoiceFactory(created_date='2017-12-13')

    from_date = '12-02-2017'
    to_date = '20-12-2017'

    client = Client(schema)
    executed = client.execute("""
        query averageInvoiceReports($fromDate: String, $toDate: String) {
            averageInvoiceReports(fromDate: $fromDate, toDate: $toDate) {
                id
                month
                totalAmount
                totalOutstanding
                averageAmount
                averageOutstanding
            }
        }
    """, variable_values={
            'toDate': to_date,
            'fromDate': from_date,
        },
    )

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_matters_per_year_reports(snapshot, request):
    """ Test success matters per year reports """

    InvoiceFactory(created_date='2017-12-13')

    client = Client(schema)
    executed = client.execute("""
        query mattersPerYearReports {
            mattersPerYearReports {
                id
                years {
                    id
                    name
                    count
                }
                month
            }
        }
    """)

    snapshot.assert_match(executed)


# @pytest.mark.django_db
# def test_matters_per_year_reports_with_not_none_time_index(snapshot, request):
#     """ Test success matters per year reports with not none time index """
#
#     MatterFactory(created_date='2019-11-13')
#     MatterFactory(created_date='2010-05-20')
#
#     client = Client(schema)
#     executed = client.execute("""
#         query mattersPerYearReports {
#             mattersPerYearReports {
#                 id
#                 years {
#                     id
#                     name
#                     count
#                 }
#                 month
#             }
#         }
#     """)
#
#     snapshot.assert_match(executed)


@pytest.mark.django_db
def test_client_value_reports(snapshot, request):
    """ Test success client value reports """

    clients = ClientFactory.create_batch(
        size=3,
        created_date='2015-11-20'
    )
    from_date = '2015-05-20'
    to_date = '2018-02-20'

    client = Client(schema)
    executed = client.execute("""
        query clientValueReports(
            $clients:[ID],
            $fromDate:String,
            $toDate:String
        ) {
            clientValueReports(
                clients:$clients,
                fromDate:$fromDate,
                toDate:$toDate
            ) {
                id
                name
                value
            }
        }
    """, variable_values={
            'clients': [to_global_id('ClientType', client_instance.id)
                        for client_instance in clients],
            'fromDate': from_date,
            'toDate': to_date,
        },
    )

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_client_value_reports_without_clients(snapshot, request):
    """ Test success client value reports without clients """

    from_date = '2015-05-20'
    to_date = '2018-02-20'

    client = Client(schema)
    executed = client.execute("""
        query clientValueReports(
            $clients:[ID],
            $fromDate:String,
            $toDate:String
        ) {
            clientValueReports(
                clients:$clients,
                fromDate:$fromDate,
                toDate:$toDate
            ) {
                id
                name
                value
            }
        }
    """, variable_values={
            'clients': [],
            'fromDate': from_date,
            'toDate': to_date,
        },
    )

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_active_matters_reports(snapshot, request):
    """ Test success active matters reports """

    InvoiceFactory(created_date='2017-12-13')

    client = Client(schema)
    executed = client.execute("""
        query activeMattersReports {
            activeMattersReports {
                id
                date
                count
            }
        }
    """)

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_new_matters_reports(snapshot, request):
    """ Test success new matters reports """

    client = Client(schema)
    executed = client.execute("""
        query newMattersReports {
            newMattersReports {
                id
                date
                count
            }
        }
    """)

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_new_entities(snapshot, request):
    """ Test success new entities """

    ClientFactory.create_batch(
        size=1,
        created_date=date(2018, 8, 17),
    )

    client = Client(schema)
    executed = client.execute("""
        query newEntities {
            newEntities {
                id
                date
                count
            }
        }
    """)

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_new_entities2(snapshot, request):
    """ Test success new entities """

    ClientFactory.create_batch(
        size=2
        )

    client = Client(schema)
    executed = client.execute("""
        query newEntities {
            newEntities {
                id
                date
                count
            }
        }
    """)

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_billable_units(snapshot, request):
    """ Test success billable units """

    client = Client(schema)
    executed = client.execute("""
        query billableUnits {
            billableUnits {
                id
                date
                count
            }
        }
    """)

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_open_matters_reports(snapshot, request):
    """ Test success open matters reports """

    MatterFactory.create_batch(
        size=3,
        billable_status=3,
        created_date=date(2018, 8, 17)
    )

    client = Client(schema)
    executed = client.execute("""
        query openMattersReports {
            openMattersReports {
                id
                date
                count
            }
        }
    """)

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_units_by_staff_reports(snapshot, request):
    """ Test success units by staff reports """

    from_date = '2010-05-13'
    to_date = '2017-12-13'
    staff_members = UserFactory.create_batch(size=3)

    client = Client(schema)
    executed = client.execute("""
        query unitsByStaffReports(
            $staffMembers:[ID],
            $fromDate:String,
            $toDate:String
        ) {
            unitsByStaffReports(
                staffMembers:$staffMembers,
                fromDate:$fromDate,
                toDate:$toDate
            ) {
                id
                date
                staffMembers {
                    id
                }
            }
        }
    """, variable_values={
            'staffMembers': [to_global_id('UserType', staff_member.id)
                             for staff_member in staff_members],
            'fromDate': from_date,
            'toDate': to_date,
        },
    )

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_units_by_staff_reports_without_data(snapshot, request):
    """ Test success units by staff reports """

    from_date = ''
    to_date = ''
    staff_members = UserFactory.create_batch(size=3)

    client = Client(schema)
    executed = client.execute("""
        query unitsByStaffReports(
            $staffMembers:[ID],
            $fromDate:String,
            $toDate:String
        ) {
            unitsByStaffReports(
                staffMembers:$staffMembers,
                fromDate:$fromDate,
                toDate:$toDate
            ) {
                id
                date
                staffMembers {
                    id
                }
            }
        }
    """, variable_values={
            'staffMembers': [to_global_id('UserType', staff_member.id)
                             for staff_member in staff_members],
            'fromDate': from_date,
            'toDate': to_date,
        },
    )

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_open_matters_by_staff_reports(snapshot, request):
    """ Test success open matters by staff reports """

    InvoiceFactory(created_date='2017-12-13')

    client = Client(schema)
    executed = client.execute("""
        query openMattersByStaffReports {
            openMattersByStaffReports {
                id
                staffMember
                matterStatuses {
                    id
                }
            }
        }
    """)

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_total_of_matters_by_staff_reports(snapshot, request):
    """ Test success total of matters by staff reports """

    staff_members = UserFactory.create_batch(
        size=3,
    )

    MatterFactory.create_batch(
        size=3,
        created_date='2015-04-20'
    )
    MatterFactory.create_batch(
        size=3,
        created_date='2018-08-21',
    )

    client = Client(schema)
    executed = client.execute("""
        query totalOfMattersByStaffReports(
            $staffMembers: [ID],
            $matterStatus: Int
        ) {
            totalOfMattersByStaffReports(
                staffMembers: $staffMembers,
                matterStatus: $matterStatus,
            ) {
                id
                date
                staffMembers{
                    id
                }
            }
        }
    """, variable_values={
            'staffMembers': [to_global_id('UserType', staff_member.id)
                             for staff_member in staff_members],
            'matterStatus': 1,
        },
    )

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_total_of_matters_by_staff_reports_without_matter(snapshot, request):
    """ Test success total of matters by staff reports without matter """

    staff_members = UserFactory.create_batch(
        size=3,
    )

    client = Client(schema)
    executed = client.execute("""
        query totalOfMattersByStaffReports(
            $staffMembers: [ID],
            $matterStatus: Int
        ) {
            totalOfMattersByStaffReports(
                staffMembers: $staffMembers,
                matterStatus: $matterStatus,
            ) {
                id
                date
                staffMembers{
                    id
                }
            }
        }
    """, variable_values={
            'staffMembers': [to_global_id('UserType', staff_member.id)
                             for staff_member in staff_members],
            'matterStatus': 0,
        },
    )

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_effective_rate_reports_without_data(snapshot, request):
    """ Test success effective rate reports without data """

    staff_member = UserFactory(id=1)
    request.user = staff_member
    client = Client(schema, context=request)
    executed = client.execute("""
        query effectiveRateReports(
            $staffMemberId: ID,
            $fromDate: String,
            $toDate: String
        ){
            effectiveRateReports(
                staffMemberId: $staffMemberId,
                fromDate: $fromDate,
                toDate: $toDate
            ){
                id
                date
                value
            }
        }
    """, variable_values={
            'staffMemberId': '',
            'fromDate': '',
            'toDate': '',
        },
    )

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_effective_rate_reports(snapshot, request):
    """ Test success effective rate reports without data """

    to_date = '2017-11-20'
    from_date = '2015-01-20'
    staff_member = UserFactory(id=1)

    request.user = staff_member
    client = Client(schema, context=request)
    executed = client.execute("""
        query effectiveRateReports(
            $staffMemberId: ID,
            $fromDate: String,
            $toDate: String
        ){
            effectiveRateReports(
                staffMemberId: $staffMemberId,
                fromDate: $fromDate,
                toDate: $toDate
            ){
                id
                date
                value
            }
        }
    """, variable_values={
            'staffMemberId': to_global_id('UserType', staff_member.id),
            'fromDate': to_date,
            'toDate': from_date,
        },
    )

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_client_invoice_value(snapshot, request):
    """ Test success client invoice value """

    InvoiceFactory(created_date='2017-12-13')

    client = Client(schema)
    executed = client.execute("""
        query clientInvoiceValue {
            clientInvoiceValue {
                id
                count
                title
            }
        }
    """)

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_staff_matter_report(snapshot, request):
    """ Test matter report query with billable status 1 """

    manager = UserFactory(is_staff=True, is_active=True)
    MatterFactory.create_batch(size=3, manager=manager)
    request.user = manager
    client = Client(schema, context=request)
    executed = client.execute("""
    query staffMatterReportMatter(
        $after: String
        $staffName: String
        $billableStatus: String
        $billableStatusExclude: Float
      ) {
        matters(
          first: 15
          after: $after
          staffName: $staffName
          billableStatus: $billableStatus
          billableStatusExclude: $billableStatusExclude
        ) {
          edges {
            cursor
            node {
              id
              name
              totalTimeValue
              totalTimeInvoiced
              wip
              billableStatusDisplay
              daysOpen
              matterStatusDisplay
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
        'staffName': manager.full_name,
        'billableStatus': 1,
        'billableStatusExclude': 3,
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_staff_matter_report2(snapshot, request):
    """ Test matter report query with billable status 2
        must return empty data, there are no matter with this status"""

    manager = UserFactory(is_staff=True, is_active=True)
    MatterFactory.create_batch(size=3, manager=manager, billable_status=1)
    request.user = manager
    client = Client(schema, context=request)
    executed = client.execute("""
    query staffMatterReportMatter(
        $after: String
        $staffName: String
        $billableStatus: String
        $billableStatusExclude: Float
      ) {
        matters(
          first: 15
          after: $after
          staffName: $staffName
          billableStatus: $billableStatus
          billableStatusExclude: $billableStatusExclude
        ) {
          edges {
            cursor
            node {
              id
              name
              totalTimeValue
              totalTimeInvoiced
              wip
              billableStatusDisplay
              daysOpen
              matterStatusDisplay
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
        'staffName': manager.full_name,
        'billableStatus': 2,
        'billableStatusExclude': 3,
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_staff_matter_report3(snapshot, request):
    """ Test matter report query with billable status 2 """

    manager = UserFactory(is_staff=True, is_active=True)
    MatterFactory.create_batch(size=3, manager=manager, billable_status=2)
    request.user = manager
    client = Client(schema, context=request)
    executed = client.execute("""
    query staffMatterReportMatter(
        $after: String
        $staffName: String
        $billableStatus: String
        $billableStatusExclude: Float
      ) {
        matters(
          first: 15
          after: $after
          staffName: $staffName
          billableStatus: $billableStatus
          billableStatusExclude: $billableStatusExclude
        ) {
          edges {
            cursor
            node {
              id
              name
              totalTimeValue
              totalTimeInvoiced
              wip
              billableStatusDisplay
              daysOpen
              matterStatusDisplay
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
        'staffName': manager.full_name,
        'billableStatus': 2,
        'billableStatusExclude': 3,
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_staff_matter_report4(snapshot, request):
    """ Test matter report query with all billable statuses"""

    manager = UserFactory(is_staff=True, is_active=True)
    MatterFactory.create_batch(size=3, manager=manager, billable_status=2)
    MatterFactory.create_batch(size=3, manager=manager, billable_status=1)
    request.user = manager
    client = Client(schema, context=request)
    executed = client.execute("""
    query staffMatterReportMatter(
        $after: String
        $staffName: String
        $billableStatus: String
        $billableStatusExclude: Float
      ) {
        matters(
          first: 15
          after: $after
          staffName: $staffName
          billableStatus: $billableStatus
          billableStatusExclude: $billableStatusExclude
        ) {
          edges {
            cursor
            node {
              id
              name
              totalTimeValue
              totalTimeInvoiced
              wip
              billableStatusDisplay
              daysOpen
              matterStatusDisplay
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
        'staffName': manager.full_name,
        'billableStatusExclude': 3,
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_staff_principal_matter_report(snapshot, request):
    """ Test principal matter report query with all billable statuses"""

    manager = UserFactory(is_staff=True, is_active=True)
    MatterFactory.create_batch(size=3, principal=manager, billable_status=2)
    MatterFactory.create_batch(size=3, principal=manager, billable_status=1)
    request.user = manager
    client = Client(schema, context=request)
    executed = client.execute("""
    query staffMatterReportMatter(
        $after: String
        $principalName: String
        $billableStatus: String
      ) {
        matters(
          first: 15
          after: $after
          principalName: $principalName
          billableStatus: $billableStatus
        ) {
          edges {
            cursor
            node {
              id
              name
              totalTimeValue
              totalTimeInvoiced
              wip
              billableStatusDisplay
              daysOpen
              matterStatusDisplay
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
        'principalName': manager.full_name,
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_staff_principal_matter_report2(snapshot, request):
    """ Test principal matter report query with 1 billable statuse"""

    manager = UserFactory(is_staff=True, is_active=True)
    MatterFactory.create_batch(size=3, principal=manager, billable_status=2)
    MatterFactory.create_batch(size=3, principal=manager, billable_status=1)
    request.user = manager
    client = Client(schema, context=request)
    executed = client.execute("""
    query staffMatterReportMatter(
        $after: String
        $principalName: String
        $billableStatus: String
      ) {
        matters(
          first: 15
          after: $after
          principalName: $principalName
          billableStatus: $billableStatus
        ) {
          edges {
            cursor
            node {
              id
              name
              totalTimeValue
              totalTimeInvoiced
              wip
              billableStatusDisplay
              daysOpen
              matterStatusDisplay
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
        'principalName': manager.full_name,
        'billableStatus': 1,
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_staff_principal_matter_report3(snapshot, request):
    """ Test principal matter report query with 2 billable statuse"""

    manager = UserFactory(is_staff=True, is_active=True)
    MatterFactory.create_batch(size=3, principal=manager, billable_status=2)
    MatterFactory.create_batch(size=3, principal=manager, billable_status=1)
    request.user = manager
    client = Client(schema, context=request)
    executed = client.execute("""
    query staffMatterReportMatter(
        $after: String
        $principalName: String
        $billableStatus: String
      ) {
        matters(
          first: 15
          after: $after
          principalName: $principalName
          billableStatus: $billableStatus
        ) {
          edges {
            cursor
            node {
              id
              name
              totalTimeValue
              totalTimeInvoiced
              wip
              billableStatusDisplay
              daysOpen
              matterStatusDisplay
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
        'principalName': manager.full_name,
        'billableStatus': 2,
    })
    snapshot.assert_match(executed)
