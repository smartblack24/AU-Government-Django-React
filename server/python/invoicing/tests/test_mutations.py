from datetime import date
from decimal import Decimal
from unittest.mock import patch

import pytest
from accounts.factories import ClientFactory, LocationFactory, UserFactory
from accounts.models import User
from sitename.schema import schema
from billing.factories import (MatterFactory, TimeEntryFactory,
                               TimeEntryTypeFactory)
from core.factories import InvoiceStatusFactory
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from graphene.test import Client
from graphql_relay.node.node import to_global_id
from integration.models import Xero as XeroIntegration

from ..factories import InvoiceFactory, PaymentFactory, PaymentTermsFactory


@pytest.mark.django_db
def test_create_invoice_mutation(snapshot, request):
    """ Test success create invoice mutation """

    PaymentTermsFactory(id=1)
    InvoiceStatusFactory(id=1)
    TimeEntryTypeFactory(id=1)

    staff_member = UserFactory()
    matter = MatterFactory()
    client_instance = ClientFactory()
    time_entry = TimeEntryFactory()

    request.user = staff_member

    client = Client(schema, context_value=request)

    fixed_price_items = [{
        'id': to_global_id('TimeEntryType', time_entry.id),
        'units': time_entry.units,
        'date': date.today(),
        'unitsToBill': time_entry.units_to_bill,
        'description': time_entry.description,
        'rate': time_entry.rate, 'status': time_entry.status
    }]

    recorded_time = [{
        'id': to_global_id('TimeEntryType', time_entry.id),
        'unitsToBill': time_entry.units_to_bill,
    }]

    executed = client.execute("""
        mutation createInvoice($invoiceData: InvoiceInput!) {
        createInvoice(invoiceData: $invoiceData) {
          errors
          invoice {
              number
          }
        }
      }
    """, variable_values={
        'invoiceData': {
            'billingMethod': 1,
            'matter': {
                'id': to_global_id('MatterType', matter.id),
                'description': matter.description,
                'budget': Decimal(matter.budget),
                'client': {
                    'id': client_instance.id
                },
            },
            'fixedPriceItems': fixed_price_items,
            'recordedTime': recorded_time,
        },
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_invoice_mutation(snapshot, request):
    """ Test success update invoice mutation """

    invoice = InvoiceFactory(id=1238)
    time_entries = TimeEntryFactory.create_batch(size=1)

    staff_member = UserFactory()
    request.user = staff_member

    time_entries_list = [time_entry.id for time_entry in time_entries]

    client = Client(schema, context_value=request)
    executed = client.execute("""
        mutation updateInvoice($invoiceId: ID!, $recordedTime: [ID]!) {
        updateInvoice(invoiceId: $invoiceId, recordedTime: $recordedTime) {
          errors
        }
      }
    """, variable_values={
            'invoiceId': to_global_id('InvoiceType', invoice.id),
            'recordedTime': time_entries_list,
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_invoice_mutation_with_incorrect_data(snapshot, request):
    """ Test failed update invoice mutation with incorrect data """

    invoice = InvoiceFactory(id=6532)

    staff_member = UserFactory()
    request.user = staff_member

    client = Client(schema, context_value=request)
    executed = client.execute("""
        mutation updateInvoice($invoiceId: ID!, $recordedTime: [ID]!) {
        updateInvoice(invoiceId: $invoiceId, recordedTime: $recordedTime) {
          errors
        }
      }
    """, variable_values={
            'invoiceId': to_global_id('InvoiceType', invoice.id),
            'recordedTime': [None],
        })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_invoice_mutation_with_incorrect_invoice(snapshot, request):
    """Test failed update invoice mutation with incorrect invoice data"""

    payment = PaymentFactory()
    time_entries = TimeEntryFactory.create_batch(size=1)

    staff_member = UserFactory()
    request.user = staff_member

    time_entries = [time_entry.id for time_entry in time_entries]

    client = Client(schema, context_value=request)
    executed = client.execute("""
        mutation updateInvoice($invoiceId: ID!, $recordedTime: [ID]!) {
        updateInvoice(invoiceId: $invoiceId, recordedTime: $recordedTime) {
          errors
        }
      }
    """, variable_values={
            'invoiceId': to_global_id('InvoiceType', payment.invoice.id),
            'recordedTime': time_entries,
        })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_check_for_existence_create_invoice_mutation(snapshot, request):
    """ Test create invoice with check for existence mutation """

    staff_member = UserFactory()
    client_instance = ClientFactory()

    request.user = staff_member

    client = Client(schema, context_value=request)

    fixed_price_items = []

    recorded_time = []

    executed = client.execute("""
        mutation createInvoice($invoiceData: InvoiceInput!) {
        createInvoice(invoiceData: $invoiceData) {
          errors
          invoice {
              number
          }
        }
      }
    """, variable_values={
        'invoiceData': {
            'billingMethod': 1,
            'matter': {
                'id': 1,
                'description': 'qwe',
                'budget': 1.23,
                'client': {
                    'id':  client_instance.id
                },
            },
            'fixedPriceItems': fixed_price_items,
            'recordedTime': recorded_time,
        },
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_invoice_info_mutation(snapshot):
    """ Test success update invoice info mutation """

    PaymentTermsFactory(id=1)

    status = InvoiceStatusFactory(id=1)
    matter = MatterFactory()
    manager = UserFactory()
    invoice = InvoiceFactory(id=1998)
    client_instance = ClientFactory()

    client = Client(schema)

    executed = client.execute("""
        mutation updateInfo($invoiceId: ID!, $invoiceData: InvoiceInfoInput) {
          updateInvoiceInfo(invoiceId: $invoiceId, invoiceData: $invoiceData) {
              errors
              invoice {
                  number
              }
          }
      }
    """, variable_values={
        'invoiceId': to_global_id('InvoiceType', invoice.id),
        'invoiceData': {
            'billingMethod': invoice.billing_method,
            'createdDate': date.today(),
            'dueDate': date.today(),
            'status': {
                'id': status.id
            },
            'matter': {
                'id': to_global_id('MatterType', matter.id),
                'description': matter.description,
                'client': {
                    'id': client_instance.id
                },
                'manager': {
                    'id':  manager.id
                },
            },
        },
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_invoice_info_mutation_with_invalid_invoice(snapshot):
    """ Test failed update invoice info mutation with invalid invoice data """

    PaymentTermsFactory(id=1)

    status = InvoiceStatusFactory(id=1)
    matter = MatterFactory()
    manager = UserFactory()
    invoice = PaymentFactory().invoice
    client_instance = ClientFactory()

    client = Client(schema)

    executed = client.execute("""
        mutation updateInfo($invoiceId: ID!, $invoiceData: InvoiceInfoInput) {
          updateInvoiceInfo(invoiceId: $invoiceId, invoiceData: $invoiceData) {
              errors
              invoice {
                  number
              }
          }
      }
    """, variable_values={
        'invoiceId': to_global_id('InvoiceType', invoice.id),
        'invoiceData': {
            'billingMethod': invoice.billing_method,
            'createdDate': date.today(),
            'dueDate': date.today(),
            'status': {
                'id': status.id
            },
            'matter': {
                'id': to_global_id('MatterType', matter.id),
                'description': matter.description,
                'client': {
                    'id': client_instance.id
                },
                'manager': {
                    'id':  manager.id
                },
            },
        },
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_check_for_existence_update_invoice_info_mutation(snapshot):
    """ Test update invoice info with check for existence mutation """

    client = Client(schema)

    executed = client.execute("""
        mutation updateInfo($invoiceId: ID!, $invoiceData: InvoiceInfoInput) {
          updateInvoiceInfo(invoiceId: $invoiceId, invoiceData: $invoiceData) {
              errors
              invoice {
                  number
              }
          }
      }
    """, variable_values={
        'invoiceId': 1,
        'invoiceData': {
            'billingMethod': 1,
            'createdDate': date.today(),
            'dueDate': date.today(),
            'status': {
                'id': 1
            },
            'matter': {
                'id': 1,
                'description': 'qwe',
                'client': {
                    'id': 1
                },
                'manager': {
                    'id': 1
                },
            },
        },
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_remove_time_record_mutation(snapshot):
    """ Test remove time record mutation """

    client = Client(schema)

    time_record = TimeEntryFactory()

    executed = client.execute("""
      mutation removeTimeRecord($timeRecordId: ID!, $timeRecordType: Int!) {
        removeTimeRecord(timeRecordId: $timeRecordId, timeRecordType: $timeRecordType) {
          errors
        }
      }
    """, variable_values={
        'timeRecordId': to_global_id('TimeEntryType', time_record.id),
        'timeRecordType': time_record.entry_type
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_check_for_existence_remove_time_record_mutation(snapshot):
    """ Test check for existence remove time record mutation """

    client = Client(schema)

    time_record = TimeEntryFactory()

    executed = client.execute("""
      mutation removeTimeRecord($timeRecordId: ID!, $timeRecordType: Int!) {
        removeTimeRecord(timeRecordId: $timeRecordId, timeRecordType: $timeRecordType) {
          errors
        }
      }
    """, variable_values={
        'timeRecordId': to_global_id('TimeEntryType', time_record.id),
        'timeRecordType': 2
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_add_payment_mutation(snapshot, request):
    """ Test success add payment mutation """
    staff_member = UserFactory()
    request.user = staff_member
    client = Client(schema, context_value=request)

    payment = PaymentFactory()
    # xero_put_patch = patch('invoicing.mutations.xero.payments.put')
    # with xero_put_patch as mock_xero_put:
    executed = client.execute("""
        mutation addPayment($invoiceId: ID!, $method: Int!, $amount: Float!, $date: String!) {
            addPayment(invoiceId: $invoiceId, method: $method, amount: $amount, date: $date) {
                errors
                payment {
                    id
                }
            }
        }
    """, variable_values={
        'invoiceId': to_global_id('InvoiceType', payment.invoice.id),
        'method': payment.method,
        'amount': payment.amount,
        'date': date.today()
    })
    # mock_xero_put.assert_called_once_with(payment_data)
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_check_for_existence_add_payment_mutation(snapshot, request):
    """ Test check for existence success add payment mutation """

    staff_member = UserFactory()
    request.user = staff_member
    client = Client(schema, context_value=request)

    executed = client.execute("""
        mutation addPayment($invoiceId: ID!, $method: Int!, $amount: Float!, $date: String!) {
            addPayment(invoiceId: $invoiceId, method: $method, amount: $amount, date: $date) {
                errors
                payment {
                    id
                }
            }
        }
    """, variable_values={
        'invoiceId': 1,
        'method': 1,
        'amount': 1,
        'date': date.today()
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_remove_fixed_price_item_mutation(snapshot):
    """ Test remove fixed price item mutation """

    client = Client(schema)
    invoice = InvoiceFactory(id=7436)
    fixed_price_item = TimeEntryFactory(entry_type=3, invoice=invoice)

    executed = client.execute("""
        mutation removeFixedPriceItem($id: ID!) {
            removeFixedPriceItem(id: $id) {
            errors
            invoice {
                number
                }
            }
        }
        """, variable_values={
        'id': to_global_id('TimeEntryType', fixed_price_item.id),
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_remove_fixed_price_item_mutation2(snapshot):
    """ Test remove fixed price item mutation with wrong id """

    client = Client(schema)

    executed = client.execute("""
        mutation removeFixedPriceItem($id: ID!) {
            removeFixedPriceItem(id: $id) {
            errors
            invoice {
                number
                }
            }
        }
        """, variable_values={
        'id': to_global_id('TimeEntryType', 0),
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_create_fixed_price_item_mutation(snapshot, request):
    """ Test create fixed price item mutation """

    staff_member = UserFactory()

    request.user = staff_member

    client = Client(schema, context_value=request)
    TimeEntryTypeFactory(id=1)
    time_entry = TimeEntryFactory.build(entry_type=3)

    fixed_price_item = {
        'id': time_entry.id,
        'units': time_entry.units,
        'date': date.today(),
        'unitsToBill': time_entry.units_to_bill,
        'description': time_entry.description,
        'rate': 1, 'status': time_entry.status
    }
    invoice = InvoiceFactory()

    executed = client.execute("""
        mutation createFixedPriceItem($invoiceId: ID!, $fixedPriceItem: InvoiceFixedPriceItemInput!) {
            createFixedPriceItem(invoiceId: $invoiceId, fixedPriceItem: $fixedPriceItem) {
                invoice {
                    id
                }
            }
        }
        """, variable_values={
        'invoiceId': to_global_id('InvoiceType', invoice.id),
        'fixedPriceItem': fixed_price_item
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_create_fixed_price_item_mutation2(snapshot, request):
    """ Test create fixed price item without invoice mutation """

    staff_member = UserFactory()

    request.user = staff_member

    client = Client(schema, context_value=request)

    time_entry = TimeEntryFactory.build(entry_type=3)

    fixed_price_item = {
        'id': time_entry.id,
        'units': time_entry.units,
        'date': date.today(),
        'unitsToBill': time_entry.units_to_bill,
        'description': time_entry.description,
        'rate': 1, 'status': time_entry.status
    }

    executed = client.execute("""
        mutation createFixedPriceItem($invoiceId: ID!, $fixedPriceItem: InvoiceFixedPriceItemInput!) {
            createFixedPriceItem(invoiceId: $invoiceId, fixedPriceItem: $fixedPriceItem) {
                invoice {
                    id
                }
            }
        }
        """, variable_values={
        'invoiceId': to_global_id('InvoiceType', 9),
        'fixedPriceItem': fixed_price_item
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_create_fixed_price_item_mutation_with_error(snapshot, request):
    """ Test failed create fixed price item mutation without update invoice """

    staff_member = UserFactory()

    request.user = staff_member

    client = Client(schema, context_value=request)

    time_entry = TimeEntryFactory.build(entry_type=3)

    payment = PaymentFactory()

    fixed_price_item = {
        'id': time_entry.id,
        'units': time_entry.units,
        'date': date.today(),
        'unitsToBill': time_entry.units_to_bill,
        'description': time_entry.description,
        'rate': 1, 'status': time_entry.status
    }

    executed = client.execute("""
        mutation createFixedPriceItem($invoiceId: ID!, $fixedPriceItem: InvoiceFixedPriceItemInput!) {
            createFixedPriceItem(invoiceId: $invoiceId, fixedPriceItem: $fixedPriceItem) {
                invoice {
                    id
                }
            }
        }
        """, variable_values={
        'invoiceId': to_global_id('InvoiceType', payment.invoice.id),
        'fixedPriceItem': fixed_price_item
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_fixed_price_item_mutation(snapshot, request):
    """ Test update fixed price item mutation """

    staff_member = UserFactory()

    request.user = staff_member

    client = Client(schema, context_value=request)

    time_entry = TimeEntryFactory(entry_type=3, invoice=InvoiceFactory(id=6734))

    fixed_price_item = {
        'id': to_global_id('TimeEntryType', time_entry.id),
        'units': time_entry.units,
        'date': date.today(),
        'unitsToBill': 12,
        'description': time_entry.description,
        'rate': 1, 'status': time_entry.status
    }

    executed = client.execute("""
        mutation updateFixedPriceItem($fixedPriceItem: InvoiceFixedPriceItemInput!) {
            updateFixedPriceItem(fixedPriceItem: $fixedPriceItem) {
                invoice {
                    id
                }
            }
        }
        """, variable_values={
        'fixedPriceItem': fixed_price_item
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_fixed_price_item_mutation2(snapshot, request):
    """ Test update fixed price item with missing item mutation """

    staff_member = UserFactory()

    request.user = staff_member

    client = Client(schema, context_value=request)

    fixed_price_item = {
        'id': to_global_id('TimeEntryType', 0),
        'units': 1,
        'date': date.today(),
        'unitsToBill': 1,
        'description': "test",
        'rate': 1, 'status': 1
    }

    executed = client.execute("""
        mutation updateFixedPriceItem($fixedPriceItem: InvoiceFixedPriceItemInput!) {
            updateFixedPriceItem(fixedPriceItem: $fixedPriceItem) {
                invoice {
                    id
                }
            }
        }
        """, variable_values={
        'fixedPriceItem': fixed_price_item
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_remove_invoice_mutation(snapshot, request):
    """Test a success removing invoice"""

    user_without_perms = UserFactory()

    user_ct, created = ContentType.objects.get_or_create(
        app_label='invoicing', model='Invoicing')
    permission, created = Permission.objects.get_or_create(
        content_type=user_ct,
        codename='delete_invoice',
        name="Can delete delete_invoice"
    )

    user_without_perms.user_permissions.add(permission)
    staff_member = User.objects.get(id=user_without_perms.id)

    request.user = staff_member
    client = Client(schema, context=request)

    invoice = InvoiceFactory()

    executed = client.execute("""
        mutation removeInstance($instanceId: ID!, $instanceType: Int!) {
            removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
                errors
            }
        }
    """, variable_values={
        'instanceId': to_global_id('InvoiceType', invoice.id),
        'instanceType': 8
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_remove_invoice_mutation2(snapshot, request):
    """Test remove invoice with missing id"""

    user_without_perms = UserFactory()

    user_ct, created = ContentType.objects.get_or_create(
        app_label='invoicing', model='Invoicing')
    permission, created = Permission.objects.get_or_create(
        content_type=user_ct,
        codename='delete_invoice',
        name="Can delete delete_invoice"
    )

    user_without_perms.user_permissions.add(permission)
    staff_member = User.objects.get(id=user_without_perms.id)

    request.user = staff_member
    client = Client(schema, context=request)

    executed = client.execute("""
        mutation removeInstance($instanceId: ID!, $instanceType: Int!) {
            removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
                errors
            }
        }
    """, variable_values={
        'instanceId': 1,
        'instanceType': 8
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_remove_invoice_mutation3(snapshot, request):
    """Test remove invoice without permissions"""

    user_without_perms = UserFactory()

    request.user = user_without_perms
    client = Client(schema, context=request)

    invoice = InvoiceFactory()

    executed = client.execute("""
        mutation removeInstance($instanceId: ID!, $instanceType: Int!) {
            removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
                errors
            }
        }
    """, variable_values={
        'instanceId': to_global_id('InvoiceType', invoice.id),
        'instanceType': 8
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_remove_invoice_mutation4(snapshot, request):
    """Test remove invoice with payment"""

    user_without_perms = UserFactory()

    user_ct, created = ContentType.objects.get_or_create(
        app_label='invoicing', model='Invoicing')
    permission, created = Permission.objects.get_or_create(
        content_type=user_ct,
        codename='delete_invoice',
        name="Can delete delete_invoice"
    )

    user_without_perms.user_permissions.add(permission)
    staff_member = User.objects.get(id=user_without_perms.id)

    request.user = staff_member
    client = Client(schema, context=request)
    payments = PaymentFactory.create_batch(size=5)
    invoice = InvoiceFactory()
    invoice.payments.add(*payments)

    executed = client.execute("""
        mutation removeInstance($instanceId: ID!, $instanceType: Int!) {
            removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
                errors
            }
        }
    """, variable_values={
        'instanceId': to_global_id('InvoiceType', invoice.id),
        'instanceType': 8
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_remove_invoice_mutation_with_no_success_delete_in_xero(snapshot, request):
    """Test remove invoice mutation with no success delete in xero """

    user_without_perms = UserFactory()

    user_ct, created = ContentType.objects.get_or_create(
        app_label='invoicing', model='Invoicing')
    permission, created = Permission.objects.get_or_create(
        content_type=user_ct,
        codename='delete_invoice',
        name="Can delete delete_invoice"
    )

    user_without_perms.user_permissions.add(permission)
    staff_member = User.objects.get(id=user_without_perms.id)

    payment = PaymentFactory()
    payment.invoice.status.name = 'In Xero'
    payment.invoice.xero_invoice_id = to_global_id('InvoiceType',
                                                   payment.invoice.id)[0],
    payment.save()
    payment.invoice.save()
    payment.invoice.status.save()

    request.user = staff_member
    client = Client(schema, context=request)
    executed = client.execute("""
        mutation removeInstance($instanceId: ID!, $instanceType: Int!) {
            removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
                errors
            }
        }
    """, variable_values={
        'instanceId': to_global_id('InvoiceType',  payment.invoice.id),
        'instanceType': 8
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_remove_payment_mutation(snapshot, request):
    """Test a success removing payment"""

    user_without_perms = UserFactory()

    user_ct, created = ContentType.objects.get_or_create(
        app_label='invoicing', model='Invoicing')
    permission, created = Permission.objects.get_or_create(
        content_type=user_ct,
        codename='delete_payment',
        name="Can delete delete payment"
    )

    user_without_perms.user_permissions.add(permission)
    staff_member = User.objects.get(id=user_without_perms.id)

    request.user = staff_member
    client = Client(schema, context=request)

    payment = PaymentFactory()

    executed = client.execute("""
        mutation removeInstance($instanceId: ID!, $instanceType: Int!) {
            removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
                errors
            }
        }
    """, variable_values={
        'instanceId': to_global_id('PaymentType', payment.id),
        'instanceType': 9
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_remove_payment_mutation2(snapshot, request):
    """Test remove payment with missing id"""

    user_without_perms = UserFactory()

    user_ct, created = ContentType.objects.get_or_create(
        app_label='invoicing', model='Invoicing')
    permission, created = Permission.objects.get_or_create(
        content_type=user_ct,
        codename='delete_payment',
        name="Can delete delete payment"
    )

    user_without_perms.user_permissions.add(permission)
    staff_member = User.objects.get(id=user_without_perms.id)

    request.user = staff_member
    client = Client(schema, context=request)

    executed = client.execute("""
        mutation removeInstance($instanceId: ID!, $instanceType: Int!) {
            removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
                errors
            }
        }
    """, variable_values={
        'instanceId': to_global_id('PaymentType', 0),
        'instanceType': 9
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_remove_payment_mutation3(snapshot, request):
    """Test remove payment without permissions"""

    user_without_perms = UserFactory()

    request.user = user_without_perms
    client = Client(schema, context=request)

    payment = PaymentFactory()

    executed = client.execute("""
        mutation removeInstance($instanceId: ID!, $instanceType: Int!) {
            removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
                errors
            }
        }
    """, variable_values={
        'instanceId': to_global_id('PaymentType', payment.id),
        'instanceType': 9
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_send_invoice_email_mutation_with(snapshot, request):
    """ Test success send invoice email mutation """

    invoice = InvoiceFactory()
    staff_member = UserFactory()
    request.user = staff_member

    client = Client(schema, context=request)
    with patch('invoicing.mutations.send_email.delay') as mock_send_email:
        executed = client.execute("""
            mutation sendInvoiceEmail($invoiceId: ID!) {
                sendInvoiceEmail(invoiceId: $invoiceId) {
                    errors
                    success
                }
            }
            """, variable_values={
              'invoiceId': to_global_id('InvoiceType', invoice.id)
        })

        mock_send_email.assert_called_once_with(
            str(invoice.id), staff_member_email=staff_member.email
        )

        snapshot.assert_match(executed)


@pytest.mark.django_db
def test_send_invoice_email_mutation_with_incorrect_id(snapshot, request):
    """ Test a fuiled send invoice email mutation """

    client = Client(schema)

    invoice = InvoiceFactory()

    with patch('invoicing.mutations.send_email') as mock_send_email:
        executed = client.execute("""
            mutation sendInvoiceEmail($invoiceId: ID!) {
                sendInvoiceEmail(invoiceId: $invoiceId) {
                    errors
                    success
                }
            }
            """, variable_values={
              'invoiceId': to_global_id('InvoiceType', invoice.id+666)
        })

        snapshot.assert_match(executed)


@pytest.mark.django_db
def test_send_invoice_in_xero_mutation_with_failed_create_invoice(snapshot, request):
    """ Test a send invoice in xero mutation with failed create invoice """

    client = ClientFactory()
    invoice = InvoiceFactory()
    invoice.matter.client = client
    invoice.matter.save()
    XeroIntegration.objects.create()
    invoice.matter.client.contact.postal_location = LocationFactory()
    invoice.matter.client.xero_contact_id = invoice.matter.client.contact.id
    invoice.matter.client.save()

    client = Client(schema)
    with patch('invoicing.mutations.send_email'):
        executed = client.execute("""
            mutation sendInvoiceToXero($invoiceId: ID!) {
                sendInvoiceToXero(invoiceId: $invoiceId) {
                    errors
                    success
                }
            }
            """, variable_values={
              'invoiceId': to_global_id('InvoiceType', invoice.id)
        })

        snapshot.assert_match(executed)


@pytest.mark.django_db
def test_send_invoice_in_xero_mutation_with_failed_create_contact(snapshot, request):
    """ Test a send invoice in xero mutation with failed create contact """

    invoice = InvoiceFactory()

    client = Client(schema)
    with patch('invoicing.mutations.send_email'):
        executed = client.execute("""
            mutation sendInvoiceToXero($invoiceId: ID!) {
                sendInvoiceToXero(invoiceId: $invoiceId) {
                    errors
                    success
                }
            }
            """, variable_values={
              'invoiceId': to_global_id('InvoiceType', invoice.id)
        })

        snapshot.assert_match(executed)
