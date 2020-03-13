from datetime import datetime

import pytest

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from accounts.models import User
from accounts.factories import ClientFactory, ContactFactory, UserFactory
from sitename.schema import schema
from core.factories import (MatterTypeFactory, MatterStatusFactory,
                            LeadStatusFactory, TimeEntryTypeFactory)
from graphene.test import Client
from graphql_relay.node.node import to_global_id
from invoicing.factories import InvoiceFactory

from ..factories import (MatterFactory, NoteFactory, TimeEntryFactory,
                         EntryTypeFactory, TimeEntryTypeFactory)


@pytest.mark.django_db
def test_create_matter_mutation(snapshot):
    """ Test success create matter mutation """
    LeadStatusFactory(id=1)
    LeadStatusFactory(name="Won")
    EntryTypeFactory(id=1)
    client = Client(schema)
    MatterStatusFactory(id=3)
    client_instance = ClientFactory()
    principal = UserFactory()
    manager = UserFactory()
    matter = MatterFactory.build()
    matter_type = MatterTypeFactory()

    executed = client.execute("""
        mutation createMatter ($matterData: MatterInput!) {
            createMatter (matterData: $matterData) {
                errors
                matter {
                    name
                }
            }
        }
    """, variable_values={
        'matterData': {
            'entryType': 1,
            'client': {'id': client_instance.id},
            'principal': {'id': principal.id},
            'manager': {'id': manager.id},
            'name': matter.name,
            'description': matter.description,
            'billingMethod': matter.billing_method,
            'matterType': {'id': matter_type.id},
            'conflictStatus': matter.conflict_status,
            'createdDate': "01/11/2018",
            'billableStatus': matter.billable_status,
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_create_matter_mutation2(snapshot):
    """ Test create matter without client mutation """

    client = Client(schema)

    principal = UserFactory()
    LeadStatusFactory(name="Won")
    manager = UserFactory()
    matter = MatterFactory.build()
    matter_type = MatterTypeFactory()

    executed = client.execute("""
        mutation createMatter ($matterData: MatterInput!) {
            createMatter (matterData: $matterData) {
                errors
                matter {
                    name
                }
            }
        }
    """, variable_values={
        'matterData': {
            'entryType': 1,
            'client': {'id': 0},
            'principal': {'id': principal.id},
            'manager': {'id': manager.id},
            'name': matter.name,
            'description': matter.description,
            'billingMethod': matter.billing_method,
            'matterType': {'id': matter_type.id},
            'conflictStatus': matter.conflict_status,
            'createdDate': matter.created_date,
            'billableStatus': matter.billable_status,
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_create_matter_mutation3(snapshot):
    """ Test success create matter with assistant mutation """

    client = Client(schema)

    client_instance = ClientFactory()
    EntryTypeFactory(id=1)
    LeadStatusFactory(id=1)
    LeadStatusFactory(name="Won")
    MatterStatusFactory(id=1)
    assistant = UserFactory()
    principal = UserFactory()
    manager = UserFactory()
    matter = MatterFactory.build()
    matter_type = MatterTypeFactory()

    executed = client.execute("""
        mutation createMatter ($matterData: MatterInput!) {
            createMatter (matterData: $matterData) {
                errors
                matter {
                    name
                }
            }
        }
    """, variable_values={
        'matterData': {
            'entryType': 1,
            'client': {'id': client_instance.id},
            'principal': {'id': principal.id},
            'assistant': {'id': to_global_id('UserType', assistant.id)},
            'manager': {'id': manager.id},
            'name': matter.name,
            'description': matter.description,
            'matterStatus': 1,
            'billingMethod': matter.billing_method,
            'matterType': {'id': matter_type.id},
            'conflictStatus': matter.conflict_status,
            'createdDate': matter.created_date,
            'billableStatus': matter.billable_status,
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_create_matter_mutation4(snapshot):
    """ Test create matter with wrong assistant mutation """

    client = Client(schema)
    EntryTypeFactory(id=1)
    LeadStatusFactory(id=1)
    LeadStatusFactory(name="Won")
    client_instance = ClientFactory()
    MatterStatusFactory(id=3)
    principal = UserFactory()
    manager = UserFactory()
    matter = MatterFactory.build()
    matter_type = MatterTypeFactory()

    executed = client.execute("""
        mutation createMatter ($matterData: MatterInput!) {
            createMatter (matterData: $matterData) {
                errors
                matter {
                    name
                }
            }
        }
    """, variable_values={
        'matterData': {
            'entryType': 1,
            'client': {'id': client_instance.id},
            'principal': {'id': principal.id},
            'assistant': {'id': to_global_id('UserType', 0)},
            'manager': {'id': manager.id},
            'name': matter.name,
            'description': matter.description,
            'billingMethod': matter.billing_method,
            'matterType': {'id': matter_type.id},
            'conflictStatus': matter.conflict_status,
            'createdDate': matter.created_date,
            'billableStatus': matter.billable_status,
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_create_matter_mutation5(snapshot):
    """ Test create matter with wrong assistant mutation """

    client = Client(schema)
    EntryTypeFactory(id=1)
    LeadStatusFactory(id=1)
    LeadStatusFactory(name="Won")
    client_instance = ClientFactory()
    MatterStatusFactory(id=3)
    principal = UserFactory()
    manager = UserFactory()
    matter = MatterFactory.build()
    matter_type = MatterTypeFactory()

    executed = client.execute("""
        mutation createMatter ($matterData: MatterInput!) {
            createMatter (matterData: $matterData) {
                errors
                matter {
                    name
                }
            }
        }
    """, variable_values={
        'matterData': {
            'entryType': 1,
            'client': {'id': client_instance.id},
            'principal': {'id': principal.id},
            'manager': {'id': manager.id},
            'name': matter.name,
            'description': matter.description,
            'billingMethod': matter.billing_method,
            'matterStatus': 3,
            'matterType': {'id': matter_type.id},
            'conflictStatus': matter.conflict_status,
            'createdDate': matter.created_date,
            'billableStatus': matter.billable_status,
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_create_lead_mutation(snapshot):
    """ Test create Lead mutation """

    client = Client(schema)
    EntryTypeFactory(id=2)
    LeadStatusFactory(id=1)
    LeadStatusFactory(name="Won")
    client_instance = ClientFactory()
    MatterStatusFactory(id=3)
    principal = UserFactory()
    manager = UserFactory()
    matter = MatterFactory.build()
    matter_type = MatterTypeFactory()

    executed = client.execute("""
        mutation createMatter ($matterData: MatterInput!) {
            createMatter (matterData: $matterData) {
                errors
                matter {
                    name
                }
            }
        }
    """, variable_values={
        'matterData': {
            'entryType': 2,
            'client': {'id': client_instance.id},
            'principal': {'id': principal.id},
            'manager': {'id': manager.id},
            'name': 'lead name',
            'leadStatus': 1,
            'description': matter.description,
            'billingMethod': 1,
            'matterType': {'id': matter_type.id},
            'conflictStatus': matter.conflict_status,
            'createdDate': matter.created_date,
            'billableStatus': 1,
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_create_lead_mutation2(snapshot):
    """ Test create Lead mutation """

    client = Client(schema)
    EntryTypeFactory(id=2)
    LeadStatusFactory(id=2)
    client_instance = ClientFactory()
    MatterStatusFactory(id=3)
    principal = UserFactory()
    manager = UserFactory()
    matter = MatterFactory.build()
    matter_type = MatterTypeFactory()

    executed = client.execute("""
        mutation createMatter ($matterData: MatterInput!) {
            createMatter (matterData: $matterData) {
                errors
                matter {
                    name
                }
            }
        }
    """, variable_values={
        'matterData': {
            'entryType': 2,
            'client': {'id': client_instance.id},
            'principal': {'id': principal.id},
            'manager': {'id': manager.id},
            'name': 'lead name 2',
            'leadStatus': 2,
            'description': matter.description,
            'billingMethod': 1,
            'matterType': {'id': matter_type.id},
            'conflictStatus': matter.conflict_status,
            'createdDate': matter.created_date,
            'leadDate': matter.created_date,
            'billableStatus': 1,
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_create_lead_mutation3(snapshot):
    """ Test create Lead mutation """

    client = Client(schema)
    EntryTypeFactory(id=2)
    LeadStatusFactory(id=2)
    client_instance = ClientFactory()
    MatterStatusFactory(id=3)
    principal = UserFactory()
    manager = UserFactory()
    matter = MatterFactory.build()
    matter_type = MatterTypeFactory()

    executed = client.execute("""
        mutation createMatter ($matterData: MatterInput!) {
            createMatter (matterData: $matterData) {
                errors
                matter {
                    name
                }
            }
        }
    """, variable_values={
        'matterData': {
            'entryType': 2,
            'client': {'id': client_instance.id},
            'principal': {'id': principal.id},
            'assistant': {'id': to_global_id('UserType', 21334)},
            'manager': {'id': manager.id},
            'name': 'lead name 3',
            'leadStatus': 2,
            'description': matter.description,
            'billingMethod': 1,
            'matterType': {'id': matter_type.id},
            'conflictStatus': matter.conflict_status,
            'createdDate': matter.created_date,
            'leadDate': matter.created_date,
            'billableStatus': 1,
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_create_lead_mutation4(snapshot):
    """ Test create Lead mutation """

    client = Client(schema)
    EntryTypeFactory(id=1)
    EntryTypeFactory(id=2)
    LeadStatusFactory(id=1)
    client_instance = ClientFactory()
    MatterStatusFactory(id=3)
    principal = UserFactory()
    manager = UserFactory()
    assistant = UserFactory()
    matter = MatterFactory.build()
    matter_type = MatterTypeFactory()

    executed = client.execute("""
        mutation createMatter ($matterData: MatterInput!) {
            createMatter (matterData: $matterData) {
                errors
                matter {
                    name
                }
            }
        }
    """, variable_values={
        'matterData': {
            'entryType': 2,
            'client': {'id': client_instance.id},
            'principal': {'id': principal.id},
            'manager': {'id': manager.id},
            'assistant': {'id': to_global_id('UserType', assistant.id)},
            'name': 'lead name',
            'leadStatus': 1,
            'description': matter.description,
            'billingMethod': 1,
            'matterType': {'id': matter_type.id},
            'conflictStatus': matter.conflict_status,
            'createdDate': matter.created_date,
            'leadDate': matter.created_date,
            'billableStatus': 1,
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_matter_mutation(snapshot):
    """ Test success update matter mutation """

    EntryTypeFactory(id=1)
    matter = MatterFactory(entry_type_id=1)
    matter_id = to_global_id('MatterType', matter.id)
    new_name = 'New matter name'
    new_description = 'New matter description'
    client = Client(schema)

    executed = client.execute("""
        mutation updateMatter ($matterId: ID!, $matterData: MatterInput!) {
            updateMatter (matterId: $matterId, matterData: $matterData) {
                errors
                matter {
                    name
                    description
                }
            }
        }
    """, variable_values={
        'matterId': matter_id,
        'matterData': {
            'entryType': 1,
            'client': {'id': matter.client.id},
            'principal': {'id': matter.principal.id},
            'manager': {'id': matter.manager.id},
            'name': new_name,
            'description': new_description,
            'matterType': {'id': matter.matter_type.id},
            'conflictStatus': matter.conflict_status,
            'billableStatus': matter.billable_status,
            'billingMethod': matter.billing_method,
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_matter_mutation2(snapshot):
    """ Test success update matter mutation """

    EntryTypeFactory(id=1)
    matter = MatterFactory(entry_type_id=1)
    matter_id = to_global_id('MatterType', matter.id)
    new_name = 'New matter name'
    new_description = 'New matter description'
    client = Client(schema)

    executed = client.execute("""
        mutation updateMatter ($matterId: ID!, $matterData: MatterInput!) {
            updateMatter (matterId: $matterId, matterData: $matterData) {
                errors
                matter {
                    name
                    description
                }
            }
        }
    """, variable_values={
        'matterId': matter_id,
        'matterData': {
            'entryType': 1,
            'client': {'id': matter.client.id},
            'principal': {'id': matter.principal.id},
            'manager': {'id': matter.manager.id},
            'name': new_name,
            'description': new_description,
            'matterType': {'id': matter.matter_type.id},
            'conflictStatus': matter.conflict_status,
            'billableStatus': matter.billable_status,
            'billingMethod': matter.billing_method,
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_matter_mutation3(snapshot):
    """ Test failed update matter mutation """

    EntryTypeFactory(id=1)
    matter = MatterFactory(entry_type_id=1)
    new_name = 'New matter name'
    new_description = 'New matter description'
    client = Client(schema)

    executed = client.execute("""
        mutation updateMatter ($matterId: ID!, $matterData: MatterInput!) {
            updateMatter (matterId: $matterId, matterData: $matterData) {
                errors
                matter {
                    name
                    description
                }
            }
        }
    """, variable_values={
        'matterId': 0,
        'matterData': {
            'entryType': 1,
            'client': {'id': 0},
            'principal': {'id': 0},
            'manager': {'id': 0},
            'name': new_name,
            'description': new_description,
            'matterType': {'id': matter.matter_type.id},
            'conflictStatus': matter.conflict_status,
            'billableStatus': matter.billable_status,
            'billingMethod': matter.billing_method,
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_matter_mutation4(snapshot):
    """ Test success update matter with assistant mutation """

    EntryTypeFactory(id=1)
    matter = MatterFactory(entry_type_id=1)
    assistant = UserFactory()
    matter_id = to_global_id('MatterType', matter.id)
    new_name = 'New matter name'
    new_description = 'New matter description'
    client = Client(schema)

    executed = client.execute("""
        mutation updateMatter ($matterId: ID!, $matterData: MatterInput!) {
            updateMatter (matterId: $matterId, matterData: $matterData) {
                errors
                matter {
                    name
                    description
                }
            }
        }
    """, variable_values={
        'matterId': matter_id,
        'matterData': {
            'entryType': 1,
            'client': {'id': matter.client.id},
            'principal': {'id': matter.principal.id},
            'manager': {'id': matter.manager.id},
            'assistant': {'id': to_global_id('UserType', assistant.id)},
            'name': new_name,
            'description': new_description,
            'matterType': {'id': matter.matter_type.id},
            'conflictStatus': matter.conflict_status,
            'billableStatus': matter.billable_status,
            'billingMethod': matter.billing_method,
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_matter_mutation5(snapshot):
    """ Test success close matter with assistant mutation """

    EntryTypeFactory(id=1)
    matter = MatterFactory(entry_type_id=1)
    assistant = UserFactory()
    matter_id = to_global_id('MatterType', matter.id)
    new_name = 'New matter name'
    new_description = 'New matter description'
    client = Client(schema)

    executed = client.execute("""
        mutation updateMatter ($matterId: ID!, $matterData: MatterInput!) {
            updateMatter (matterId: $matterId, matterData: $matterData) {
                errors
                matter {
                    name
                    description
                }
            }
        }
    """, variable_values={
        'matterId': matter_id,
        'matterData': {
            'entryType': 1,
            'client': {'id': matter.client.id},
            'principal': {'id': matter.principal.id},
            'manager': {'id': matter.manager.id},
            'assistant': {'id': to_global_id('UserType', assistant.id)},
            'name': new_name,
            'description': new_description,
            'matterType': {'id': matter.matter_type.id},
            'conflictStatus': matter.conflict_status,
            'billableStatus': 3,
            'billingMethod': matter.billing_method,
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_matter_mutation6(snapshot):
    """ Test success close matter with closed_date mutation """

    EntryTypeFactory(id=1)
    matter = MatterFactory(entry_type_id=1)
    assistant = UserFactory()
    matter_id = to_global_id('MatterType', matter.id)
    new_name = 'New matter name'
    new_description = 'New matter description'
    client = Client(schema)

    executed = client.execute("""
        mutation updateMatter ($matterId: ID!, $matterData: MatterInput!) {
            updateMatter (matterId: $matterId, matterData: $matterData) {
                errors
                matter {
                    name
                    description
                }
            }
        }
    """, variable_values={
        'matterId': matter_id,
        'matterData': {
            'entryType': 1,
            'client': {'id': matter.client.id},
            'principal': {'id': matter.principal.id},
            'manager': {'id': matter.manager.id},
            'assistant': {'id': to_global_id('UserType', assistant.id)},
            'name': new_name,
            'description': new_description,
            'matterType': {'id': matter.matter_type.id},
            'conflictStatus': matter.conflict_status,
            'billableStatus': 3,
            'billingMethod': matter.billing_method,
            'closedDate': str(datetime.now()),
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_matter_mutation7(snapshot):
    """ Test success close matter with wrong closed_date mutation """

    EntryTypeFactory(id=1)
    matter = MatterFactory(entry_type_id=1)
    assistant = UserFactory()
    matter_id = to_global_id('MatterType', matter.id)
    new_name = 'New matter name'
    new_description = 'New matter description'
    client = Client(schema)

    executed = client.execute("""
        mutation updateMatter ($matterId: ID!, $matterData: MatterInput!) {
            updateMatter (matterId: $matterId, matterData: $matterData) {
                errors
                matter {
                    name
                    description
                }
            }
        }
    """, variable_values={
        'matterId': matter_id,
        'matterData': {
            'entryType': 1,
            'client': {'id': matter.client.id},
            'principal': {'id': matter.principal.id},
            'manager': {'id': matter.manager.id},
            'assistant': {'id': to_global_id('UserType', assistant.id)},
            'name': new_name,
            'description': new_description,
            'matterType': {'id': matter.matter_type.id},
            'conflictStatus': matter.conflict_status,
            'billableStatus': 3,
            'billingMethod': matter.billing_method,
            'closedDate': '0',
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_matter_mutation8(snapshot):
    """ Test failde close matter mutation """

    EntryTypeFactory(id=1)
    matter = MatterFactory(entry_type_id=1)
    time_entry = TimeEntryFactory.create_batch(size=20)
    matter.time_entries.add(*time_entry)
    assistant = UserFactory()
    matter_id = to_global_id('MatterType', matter.id)
    new_name = 'New matter name'
    new_description = 'New matter description'
    client = Client(schema)

    executed = client.execute("""
        mutation updateMatter ($matterId: ID!, $matterData: MatterInput!) {
            updateMatter (matterId: $matterId, matterData: $matterData) {
                errors
                matter {
                    name
                    description
                }
            }
        }
    """, variable_values={
        'matterId': matter_id,
        'matterData': {
            'entryType': 1,
            'client': {'id': matter.client.id},
            'principal': {'id': matter.principal.id},
            'manager': {'id': matter.manager.id},
            'assistant': {'id': to_global_id('UserType', assistant.id)},
            'name': new_name,
            'description': new_description,
            'matterType': {'id': matter.matter_type.id},
            'conflictStatus': matter.conflict_status,
            'billableStatus': 3,
            'billingMethod': matter.billing_method,
            'closedDate': str(datetime.now()),
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_lead_mutation(snapshot):
    """ Test update lead mutation """

    EntryTypeFactory(id=2)
    LeadStatusFactory(id=1)
    matter = MatterFactory(entry_type_id=2)
    matter_id = to_global_id('MatterType', matter.id)
    new_name = 'New matter name'
    new_description = 'New matter description'
    client = Client(schema)

    executed = client.execute("""
        mutation updateMatter ($matterId: ID!, $matterData: MatterInput!) {
            updateMatter (matterId: $matterId, matterData: $matterData) {
                errors
                matter {
                    name
                    description
                }
            }
        }
    """, variable_values={
        'matterId': matter_id,
        'matterData': {
            'entryType': 2,
            'client': {'id': matter.client.id},
            'principal': {'id': matter.principal.id},
            'manager': {'id': matter.manager.id},
            'name': new_name,
            'description': new_description,
            'matterType': {'id': matter.matter_type.id},
            'leadStatus': 1,
            'billingMethod': 1,
            'billableStatus': 1,
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_lead_mutation2(snapshot):
    """ Test update lead mutation """

    EntryTypeFactory(id=2)
    LeadStatusFactory(id=1)
    matter = MatterFactory(entry_type_id=2)
    matter_id = to_global_id('MatterType', matter.id)
    new_name = 'New matter name'
    new_description = 'New matter description'
    assistant = UserFactory()
    client = Client(schema)

    executed = client.execute("""
        mutation updateMatter ($matterId: ID!, $matterData: MatterInput!) {
            updateMatter (matterId: $matterId, matterData: $matterData) {
                errors
                matter {
                    name
                    description
                }
            }
        }
    """, variable_values={
        'matterId': matter_id,
        'matterData': {
            'entryType': 2,
            'client': {'id': matter.client.id},
            'principal': {'id': matter.principal.id},
            'assistant': {'id': to_global_id('UserType', assistant.id)},
            'manager': {'id': matter.manager.id},
            'name': new_name,
            'description': new_description,
            'matterType': {'id': matter.matter_type.id},
            'leadStatus': 1,
            'closedDate': '20/5/2018',
            'leadDate': '20/5/2018',
            'billingMethod': 1,
            'billableStatus': 1,
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_lead_mutation3(snapshot):
    """ Test update lead mutation """

    EntryTypeFactory(id=2)
    LeadStatusFactory(id=1)
    matter = MatterFactory(entry_type_id=2)
    matter_id = to_global_id('MatterType', matter.id)
    new_name = 'New matter name'
    new_description = 'New matter description'
    assistant = UserFactory()
    client = Client(schema)

    executed = client.execute("""
        mutation updateMatter ($matterId: ID!, $matterData: MatterInput!) {
            updateMatter (matterId: $matterId, matterData: $matterData) {
                errors
                matter {
                    name
                    description
                }
            }
        }
    """, variable_values={
        'matterId': matter_id,
        'matterData': {
            'entryType': 2,
            'client': {'id': matter.client.id},
            'principal': {'id': matter.principal.id},
            'assistant': {'id': to_global_id('UserType', assistant.id)},
            'manager': {'id': matter.manager.id},
            'name': new_name,
            'description': new_description,
            'matterType': {'id': matter.matter_type.id},
            'leadStatus': 1,
            'closedDate': 'asqwe',
            'leadDate': '20/5/2018',
            'billingMethod': 1,
            'billableStatus': 1,
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_create_time_entry_mutation(snapshot):
    """ Test success create billable time entry mutation """

    time_entry = TimeEntryFactory.build()
    TimeEntryTypeFactory(id=1)
    client_instane = ClientFactory()
    staff_member = UserFactory(rate=100)
    matter = MatterFactory()
    client = Client(schema)

    executed = client.execute("""
        mutation createTimeEntry($entryType: Int!, $timeEntryData: TimeEntryInput!) {
            createTimeEntry(entryType: $entryType, timeEntryData: $timeEntryData) {
                errors
                timeEntry {
                    description
                    units
                    unitsToBill
                    rate
                    staffMember {
                        fullName
                    }
                    client {
                        name
                    }
                    matter {
                        name
                    }
                }
            }
        }
    """, variable_values={
        'entryType': 1,
        'timeEntryData': {
            'recordType': 1,
            'description': time_entry.description,
            'units': 20,
            'rate': 100,
            'status': 1,
            'time': '12:00',
            'staffMember': {'id': to_global_id('UserType', staff_member.id)},
            'matter': {'id': to_global_id('MatterType', matter.id)},
            'client': {'id': to_global_id('ClientType', client_instane.id)},
            'date': str(datetime.now()),
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_create_time_entry_mutation2(snapshot):
    """ Test success create non-billable time entry mutation """

    time_entry = TimeEntryFactory.build()
    TimeEntryTypeFactory(id=1)
    client_instane = ClientFactory()
    staff_member = UserFactory()
    matter = MatterFactory()
    client = Client(schema)

    executed = client.execute("""
        mutation createTimeEntry($entryType: Int!, $timeEntryData: TimeEntryInput!) {
            createTimeEntry(entryType: $entryType, timeEntryData: $timeEntryData) {
                errors
                timeEntry {
                    description
                    units
                    unitsToBill
                    rate
                    staffMember {
                        fullName
                    }
                    client {
                        name
                    }
                    matter {
                        name
                    }
                }
            }
        }
    """, variable_values={
        'entryType': 1,
        'timeEntryData': {
            'recordType': 1,
            'description': time_entry.description,
            'units': 20,
            'rate': 300,
            'time': '12:00',
            'status': 2,
            'staffMember': {'id': to_global_id('UserType', staff_member.id)},
            'matter': {'id': to_global_id('MatterType', matter.id)},
            'client': {'id': to_global_id('ClientType', client_instane.id)},
            'date': str(datetime.now()),
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_create_time_entry_mutation3(snapshot):
    """ Test failed create  time entry mutation """

    time_entry = TimeEntryFactory.build()
    client = Client(schema)

    executed = client.execute("""
        mutation createTimeEntry($entryType: Int!, $timeEntryData: TimeEntryInput!) {
            createTimeEntry(entryType: $entryType, timeEntryData: $timeEntryData) {
                errors
                timeEntry {
                    description
                    units
                    unitsToBill
                    rate
                    staffMember {
                        fullName
                    }
                    client {
                        name
                    }
                    matter {
                        name
                    }
                }
            }
        }
    """, variable_values={
        'entryType': 1,
        'timeEntryData': {
            'recordType': 1,
            'description': time_entry.description,
            'units': 20,
            'rate': 300,
            'time': '12:00',
            'status': 2,
            'staffMember': {'id': to_global_id('UserType', 0)},
            'matter': {'id': to_global_id('MatterType', 0)},
            'client': {'id': to_global_id('ClientType', 0)},
            'date': str(datetime.now()),
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_time_entry_mutation(snapshot):
    """ Test success update billable time entry mutation """

    client = Client(schema)
    time_entry = TimeEntryFactory.create(status=1)

    new_description = 'New Time Entry description'
    new_units = 1243
    new_rate = 125

    executed = client.execute("""
        mutation updateTimeEntry($timeEntryId: ID!, $timeEntryData: TimeEntryInput!) {
            updateTimeEntry(timeEntryId: $timeEntryId, timeEntryData: $timeEntryData) {
                errors
                timeEntry {
                    description
                    units
                    unitsToBill
                    rate
                    staffMember {
                        fullName
                    }
                    client {
                        name
                    }
                    matter {
                        name
                    }
                }
            }
        }
    """, variable_values={
        'timeEntryId': to_global_id('TimeEntryType', time_entry.id),
        'timeEntryData': {
            'recordType': 1,
            'description': new_description,
            'status': 1,
            'time': '12:00',
            'units': new_units,
            'rate': new_rate,
            'staffMember': {'id': to_global_id('UserType', time_entry.staff_member.id)},
            'matter': {'id': to_global_id('MatterType', time_entry.matter.id)},
            'client': {'id': to_global_id('ClientType', time_entry.client.id)},
            'date': str(datetime.now()),
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_time_entry_mutation2(snapshot):
    """ Test success update non-billable time entry mutation """

    client = Client(schema)
    time_entry = TimeEntryFactory.create(status=2)

    new_description = 'New Time Entry description'
    new_units = 1243
    new_rate = 125

    executed = client.execute("""
        mutation updateTimeEntry($timeEntryId: ID!, $timeEntryData: TimeEntryInput!) {
            updateTimeEntry(timeEntryId: $timeEntryId, timeEntryData: $timeEntryData) {
                errors
                timeEntry {
                    description
                    units
                    unitsToBill
                    rate
                    staffMember {
                        fullName
                    }
                    client {
                        name
                    }
                    matter {
                        name
                    }
                }
            }
        }
    """, variable_values={
        'timeEntryId': to_global_id('TimeEntryType', time_entry.id),
        'timeEntryData': {
            'recordType': 1,
            'description': new_description,
            'status': 2,
            'units': new_units,
            'time': '12:00',
            'rate': new_rate,
            'staffMember': {'id': to_global_id('UserType', time_entry.staff_member.id)},
            'matter': {'id': to_global_id('MatterType', time_entry.matter.id)},
            'client': {'id': to_global_id('ClientType', time_entry.client.id)},
            'date': str(datetime.now()),
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_time_entry_mutation3(snapshot):
    """ Test failed update time entry mutation """

    client = Client(schema)
    time_entry = TimeEntryFactory.create(status=2)

    new_description = 'New Time Entry description'
    new_units = 1243
    new_rate = 125

    executed = client.execute("""
        mutation updateTimeEntry($timeEntryId: ID!, $timeEntryData: TimeEntryInput!) {
            updateTimeEntry(timeEntryId: $timeEntryId, timeEntryData: $timeEntryData) {
                errors
                timeEntry {
                    description
                    units
                    unitsToBill
                    rate
                    staffMember {
                        fullName
                    }
                    client {
                        name
                    }
                    matter {
                        name
                    }
                }
            }
        }
    """, variable_values={
        'timeEntryId': to_global_id('TimeEntryType', time_entry.id),
        'timeEntryData': {
            'recordType': 1,
            'description': new_description,
            'status': 2,
            'time': '12:00',
            'units': new_units,
            'rate': new_rate,
            'staffMember': {'id': to_global_id('UserType', 0)},
            'matter': {'id': to_global_id('MatterType', 0)},
            'client': {'id': to_global_id('ClientType', 0)},
            'date': str(datetime.now()),
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_create_matter_note_mutation(snapshot):
    """ Test success create matter note mutation """

    client = Client(schema)

    note = NoteFactory()
    staff_member = UserFactory()
    matter = MatterFactory()

    executed = client.execute("""
        mutation createNote($id: ID!, $text: String!, $userId: ID!, $dateTime: String!) {
          createNote(id: $id, text: $text, userId: $userId, dateTime: $dateTime) {
            errors
            note {
              id
            }
          }
        }
    """, variable_values={
        'id': to_global_id('MatterType', matter.id),
        'text': note.text,
        'dateTime': str(datetime.now()),
        'userId': to_global_id('UserType', staff_member.id),
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_create_matter_note_mutation2(snapshot):
    """ Test create matter note mutation without text """

    client = Client(schema)

    staff_member = UserFactory()
    matter = MatterFactory()

    executed = client.execute("""
        mutation createNote($id: ID!, $text: String!, $userId: ID!, $dateTime: String!) {
          createNote(id: $id, text: $text, userId: $userId, dateTime: $dateTime) {
            errors
            note {
              id
            }
          }
        }
    """, variable_values={
        'id': to_global_id('MatterType', matter.id),
        'text': '',
        'dateTime': str(datetime.now()),
        'userId': to_global_id('UserType', staff_member.id),
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_create_contact_note_mutation(snapshot):
    """ Test success create contact note mutation """

    client = Client(schema)

    note = NoteFactory()
    staff_member = UserFactory()
    contact = ContactFactory()

    executed = client.execute("""
        mutation createNote($id: ID!, $text: String!, $userId: ID!, $dateTime: String!) {
          createNote(id: $id, text: $text, userId: $userId, dateTime: $dateTime) {
            errors
            note {
              id
            }
          }
        }
    """, variable_values={
        'id': to_global_id('ContactType', contact.id),
        'text': note.text,
        'dateTime': str(datetime.now()),
        'userId': to_global_id('UserType', staff_member.id),
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_create_contact_note_mutation2(snapshot):
    """ Test create contact note with wrong contact_id mutation """

    client = Client(schema)

    note = NoteFactory()
    staff_member = UserFactory()

    executed = client.execute("""
        mutation createNote($id: ID!, $text: String!, $userId: ID!, $dateTime: String!) {
          createNote(id: $id, text: $text, userId: $userId, dateTime: $dateTime) {
            errors
            note {
              id
            }
          }
        }
    """, variable_values={
        'id': to_global_id('ContactType', 0),
        'text': note.text,
        'dateTime': str(datetime.now()),
        'userId': to_global_id('UserType', staff_member.id),
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_note_mutation(snapshot):
    """ Test success update note mutation """

    client = Client(schema)

    note = NoteFactory()
    new_text = 'note'
    staff_member = UserFactory()

    executed = client.execute("""
      mutation updateNote($noteId: ID!, $text: String!, $dateTime: String!, $userId: ID!) {
        updateNote(noteId: $noteId, text: $text, dateTime: $dateTime, userId: $userId) {
          errors
          note {
            text
            user {
              id
              fullName
            }
          }
        }
      }
    """, variable_values={
        'noteId': note.id,
        'text': new_text,
        'dateTime': str(datetime.now()),
        'userId': to_global_id('UserType', staff_member.id),
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_note_mutation2(snapshot):
    """ Test success update note without user mutation """

    client = Client(schema)

    note = NoteFactory()
    new_text = 'note'

    executed = client.execute("""
      mutation updateNote($noteId: ID!, $text: String!, $dateTime: String!, $userId: ID!) {
        updateNote(noteId: $noteId, text: $text, dateTime: $dateTime, userId: $userId) {
          errors
          note {
            text
            user {
              id
              fullName
            }
          }
        }
      }
    """, variable_values={
        'noteId': note.id,
        'text': new_text,
        'dateTime': str(datetime.now()),
        'userId': to_global_id('UserType', 0),
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_note_mutation3(snapshot):
    """ Test success update note without note id mutation """

    client = Client(schema)

    new_text = 'note'
    staff_member = UserFactory()

    executed = client.execute("""
      mutation updateNote($noteId: ID!, $text: String!, $dateTime: String!, $userId: ID!) {
        updateNote(noteId: $noteId, text: $text, dateTime: $dateTime, userId: $userId) {
          errors
          note {
            text
            user {
              id
              fullName
            }
          }
        }
      }
    """, variable_values={
        'noteId': '',
        'text': new_text,
        'dateTime': str(datetime.now()),
        'userId': to_global_id('UserType', staff_member.id),
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_note_mutation4(snapshot):
    """ Test success update note with note id mutation """

    client = Client(schema)

    new_text = 'note'
    staff_member = UserFactory()

    executed = client.execute("""
      mutation updateNote($noteId: ID!, $text: String!, $dateTime: String!, $userId: ID!) {
        updateNote(noteId: $noteId, text: $text, dateTime: $dateTime, userId: $userId) {
          errors
          note {
            text
            user {
              id
              fullName
            }
          }
        }
      }
    """, variable_values={
        'noteId': 0,
        'text': new_text,
        'dateTime': str(datetime.now()),
        'userId': to_global_id('UserType', staff_member.id),
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_remove_matter_mutation(snapshot, request):
    """Test a success removing matter"""

    staff_member = UserFactory()
    request.user = staff_member
    client = Client(schema, context=request)

    matter = MatterFactory()

    executed = client.execute("""
        mutation removeMatter($instanceId: ID!, $instanceType: Int!) {
            removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
                errors
            }
        }
    """, variable_values={
        'instanceId': to_global_id('MatterType', matter.id),
        'instanceType': 4
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_remove_matter_mutation2(snapshot, request):
    """Test a failed removing matter"""

    staff_member = UserFactory()
    request.user = staff_member
    client = Client(schema, context=request)

    executed = client.execute("""
        mutation removeMatter($instanceId: ID!, $instanceType: Int!) {
            removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
                errors
            }
        }
    """, variable_values={
        'instanceId': to_global_id('MatterType', 0),
        'instanceType': 4
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_remove_matter_mutation3(snapshot, request):
    """Test a failed removing matter"""

    staff_member = UserFactory()
    request.user = staff_member
    client = Client(schema, context=request)
    matter = MatterFactory()
    time_entry = TimeEntryFactory.create_batch(size=20)
    matter.time_entries.add(*time_entry)

    executed = client.execute("""
        mutation removeMatter($instanceId: ID!, $instanceType: Int!) {
            removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
                errors
            }
        }
    """, variable_values={
        'instanceId': to_global_id('MatterType', matter.id),
        'instanceType': 4
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_remove_time_entry_mutation(snapshot, request):
    """Test a success removing time entry"""

    staff_member = UserFactory()
    request.user = staff_member
    client = Client(schema, context=request)

    time_entry = TimeEntryFactory()

    executed = client.execute("""
        mutation removeTimeEntry($instanceId: ID!, $instanceType: Int!) {
            removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
                errors
            }
        }
    """, variable_values={
        'instanceId': to_global_id('TimeEntryType', time_entry.id),
        'instanceType': 5
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_remove_time_entry_mutation2(snapshot, request):
    """Test a failed removing time entry"""

    staff_member = UserFactory()
    request.user = staff_member
    client = Client(schema, context=request)

    invoice = InvoiceFactory()
    time_entry = TimeEntryFactory(invoice=invoice)

    executed = client.execute("""
        mutation removeTimeEntry($instanceId: ID!, $instanceType: Int!) {
            removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
                errors
            }
        }
    """, variable_values={
        'instanceId': to_global_id('TimeEntryType', time_entry.id),
        'instanceType': 5
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_remove_time_entry_mutation3(snapshot, request):
    """Test a failed removing time entry"""

    staff_member = UserFactory()
    request.user = staff_member
    client = Client(schema, context=request)

    executed = client.execute("""
        mutation removeTimeEntry($instanceId: ID!, $instanceType: Int!) {
            removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
                errors
            }
        }
    """, variable_values={
        'instanceId': to_global_id('TimeEntryType', 0),
        'instanceType': 5
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_remove_disbursement_mutation(snapshot, request):
    """Test a success removing time entry"""

    staff_member = UserFactory()
    request.user = staff_member
    client = Client(schema, context=request)

    disbursement = TimeEntryFactory(entry_type=2)

    executed = client.execute("""
        mutation removeTimeEntry($instanceId: ID!, $instanceType: Int!) {
            removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
                errors
            }
        }
    """, variable_values={
        'instanceId': to_global_id('TimeEntryType', disbursement.id),
        'instanceType': 6
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_remove_disbursement_mutation2(snapshot, request):
    """Test a failed removing time entry"""

    staff_member = UserFactory()
    request.user = staff_member
    client = Client(schema, context=request)

    invoice = InvoiceFactory()
    disbursement = TimeEntryFactory(invoice=invoice, entry_type=2)

    executed = client.execute("""
        mutation removeTimeEntry($instanceId: ID!, $instanceType: Int!) {
            removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
                errors
            }
        }
    """, variable_values={
        'instanceId': to_global_id('TimeEntryType', disbursement.id),
        'instanceType': 6
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_remove_disbursement_mutation3(snapshot, request):
    """Test a failed removing time entry"""

    staff_member = UserFactory()
    request.user = staff_member
    client = Client(schema, context=request)
    LeadStatusFactory(name="Won")

    executed = client.execute("""
        mutation removeTimeEntry($instanceId: ID!, $instanceType: Int!) {
            removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
                errors
            }
        }
    """, variable_values={
        'instanceId': to_global_id('TimeEntryType', 0),
        'instanceType': 6
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_remove_note_mutation(snapshot, request):
    """Test a success removing note"""

    user_without_perms = UserFactory()

    user_ct, created = ContentType.objects.get_or_create(
        app_label='billing', model='Billing')
    permission, created = Permission.objects.get_or_create(
        content_type=user_ct,
        codename='delete_note',
        name="Can delete delete note"
    )

    user_without_perms.user_permissions.add(permission)
    staff_member = User.objects.get(id=user_without_perms.id)

    request.user = staff_member
    client = Client(schema, context=request)

    note = NoteFactory()

    executed = client.execute("""
        mutation removeInstance($instanceId: ID!, $instanceType: Int!) {
            removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
                errors
            }
        }
    """, variable_values={
        'instanceId': to_global_id('NoteType', note.id),
        'instanceType': 7
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_remove_note_mutation_without_permission(snapshot, request):
    """Test a failed removing note without permission"""
    user_without_perms = UserFactory()
    request.user = user_without_perms
    client = Client(schema, context=request)

    note = NoteFactory()

    executed = client.execute("""
        mutation removeInstance($instanceId: ID!, $instanceType: Int!) {
            removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
                errors
            }
        }
    """, variable_values={
        'instanceId': to_global_id('NoteType', note.id),
        'instanceType': 7
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_remove_note_mutation_with_incorrect_id(snapshot, request):
    """ Test a failed removing note with incorrect id """
    user_without_perms = UserFactory()

    user_ct, created = ContentType.objects.get_or_create(
        app_label='billing', model='Billing')
    permission, created = Permission.objects.get_or_create(
        content_type=user_ct,
        codename='delete_note',
        name="Can delete delete note"
    )

    user_without_perms.user_permissions.add(permission)
    staff_member = User.objects.get(id=user_without_perms.id)

    request.user = staff_member
    client = Client(schema, context=request)

    note = NoteFactory()

    executed = client.execute("""
        mutation removeInstance($instanceId: ID!, $instanceType: Int!) {
            removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
                errors
            }
        }
    """, variable_values={
        'instanceId': to_global_id('NoteType', note.id+666),
        'instanceType': 7
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_lost(snapshot, request):
    """Test lost lead"""

    client = Client(schema)
    matter = MatterFactory()
    EntryTypeFactory(id=1)
    EntryTypeFactory(id=2)
    LeadStatusFactory(name="Lost")
    MatterStatusFactory(name="Matter Closed")
    executed = client.execute("""
          mutation lostMatter($matterId: ID!) {
            lostMatter(matterId: $matterId) {
              errors
            }
          }
    """, variable_values={
        'matterId': to_global_id('MatterType', matter.id)
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_lost2(snapshot, request):
    """Test lost lead"""

    client = Client(schema)
    matter = MatterFactory()
    EntryTypeFactory(id=1)
    EntryTypeFactory(id=2)
    LeadStatusFactory(name="Lost")
    MatterStatusFactory(name="Matter Closed")
    executed = client.execute("""
          mutation lostMatter($matterId: ID!) {
            lostMatter(matterId: $matterId) {
              errors
            }
          }
    """, variable_values={
        'matterId': to_global_id('MatterType', 1231)
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_won(snapshot, request):
    """Test Won lead"""

    client = Client(schema)
    matter = MatterFactory()
    EntryTypeFactory(id=1)
    EntryTypeFactory(id=2)
    LeadStatusFactory(name="Won")
    executed = client.execute("""
          mutation winMatter($matterId: ID!) {
            winMatter(matterId: $matterId) {
              errors
            }
          }
    """, variable_values={
        'matterId': to_global_id('MatterType', matter.id)
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_won2(snapshot, request):
    """Test Won lead"""

    client = Client(schema)
    EntryTypeFactory(id=1)
    EntryTypeFactory(id=2)
    LeadStatusFactory(name="Won")
    executed = client.execute("""
          mutation winMatter($matterId: ID!) {
            winMatter(matterId: $matterId) {
              errors
            }
          }
    """, variable_values={
        'matterId': to_global_id('MatterType', 123123)
    })
    snapshot.assert_match(executed)
