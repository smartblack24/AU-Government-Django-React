from datetime import datetime

import factory
from accounts.factories import ClientFactory, UserFactory
from core.factories import (MatterTypeFactory, MatterStatusFactory,
                            LeadStatusFactory, TimeEntryTypeFactory)


class EntryTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'billing.EntryType'

    name = factory.Sequence(lambda n: 'EntryType %s' % n)


class MatterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'billing.Matter'
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: 'Matter %s' % n)
    client = factory.SubFactory(ClientFactory)
    principal = factory.SubFactory(UserFactory)
    manager = factory.SubFactory(UserFactory)
    description = "Matter description"
    conflict_status = 1
    billing_method = 2
    billable_status = 1
    matter_type = factory.SubFactory(MatterTypeFactory)
    matter_status = factory.SubFactory(MatterStatusFactory)
    lead_status = factory.SubFactory(LeadStatusFactory)
    entry_type = factory.SubFactory(EntryTypeFactory)
    budget = factory.fuzzy.FuzzyDecimal(100, 600)
    created_date = datetime.now()


class TimeEntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'billing.TimeEntry'

    description = "Time Entry description"
    date = datetime.now()
    units = factory.fuzzy.FuzzyInteger(0, 100)
    units_to_bill = factory.fuzzy.FuzzyInteger(0, 100)
    status = factory.fuzzy.FuzzyInteger(0, 3)
    rate = factory.fuzzy.FuzzyDecimal(100, 600)
    gst_status = factory.fuzzy.FuzzyInteger(0, 3)
    staff_member = factory.SubFactory(UserFactory)
    matter = factory.SubFactory(MatterFactory)
    client = factory.SubFactory(ClientFactory)
    entry_type = 1
    time_entry_type = factory.SubFactory(TimeEntryTypeFactory)


class NoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'billing.Note'

    matter = factory.SubFactory(MatterFactory)
    date_time = datetime.now()
    text = "Note text"
    user = factory.SubFactory(UserFactory)


class StandartDisbursementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'billing.StandartDisbursement'

    name = factory.Sequence(lambda n: 'Standart Disbursement %s' % n)
    description = factory.Sequence(lambda n: 'Standart description %s' % n)
    gst_status = 1
