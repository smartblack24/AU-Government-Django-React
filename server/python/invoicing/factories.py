from datetime import datetime

import factory
from billing.factories import MatterFactory
from core.factories import InvoiceStatusFactory


class PaymentTermsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'invoicing.PaymentTerms'
    days_offset = 14


class InvoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'invoicing.Invoice'
    billing_method = 1
    matter = factory.SubFactory(MatterFactory)
    payment_terms = factory.SubFactory(PaymentTermsFactory)
    created_date = datetime.now()
    status = factory.SubFactory(InvoiceStatusFactory)


class PaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'invoicing.Payment'
    date = datetime.now()
    amount = factory.fuzzy.FuzzyDecimal(100, 600)
    method = factory.fuzzy.FuzzyInteger(0, 7)
    invoice = factory.SubFactory(InvoiceFactory)
