import factory
import datetime


class LeadStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'core.LeadStatus'
    name = factory.Sequence(lambda n: 'Lead Status %s' % n)


class TimeEntryTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'core.TimeEntryType'

    name = factory.Sequence(lambda n: 'Time Entry Type %s' % n)


class OfficeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'core.Office'

    legal_entity = factory.Sequence(lambda n: 'John %s' % n)
    abn = factory.Sequence(lambda n: 'ABN %s' % n)
    phone = '12345'
    web = 'website'
    bank_account_name = factory.Sequence(lambda n: 'Account name %s' % n)
    bank_account_bsb = 'bsb'
    bank_account_number = '33332131'
    bpay_biller_code = '55555'


class IndustryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'core.Industry'

    name = factory.Sequence(lambda n: 'Industry %s' % n)


class MatterTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'core.MatterType'

    name = factory.Sequence(lambda n: 'Matter type %s' % n)


class MatterSubTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'core.MatterSubType'

    name = str('Matter sub type')
    matter_type = factory.SubFactory(MatterTypeFactory)


class InvoiceStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'core.InvoiceStatus'

    name = factory.Sequence(lambda n: 'Invoice status %s' % n)


class MatterStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'core.MatterStatus'

    name = factory.Sequence(lambda n: 'Matter status %s' % n)


class OccupationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'core.Occupation'

    name = factory.Sequence(lambda n: 'Invoice status %s' % n)


class SectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'core.Section'

    office = factory.SubFactory(OfficeFactory)
    number = factory.Sequence(lambda n: '%s' % n)


class DocumentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'core.Document'

    section = factory.SubFactory(SectionFactory)
    date = str(datetime.datetime.now().strftime("%Y-%m-%d"))


class DocumentTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'core.DocumentType'

    name = str('PDF')


class GeneralFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'core.General'

    gst_rate = 666.99


class PdfFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'core.PDF'

    name = 'pdf_name'
