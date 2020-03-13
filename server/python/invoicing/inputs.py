import graphene

from .scalars import Currency


class IDFieldInput(graphene.InputObjectType):
    id = graphene.ID()


class InvoiceFixedPriceItemInput(graphene.InputObjectType):
    id = graphene.ID()
    date = graphene.String()
    units = graphene.Int()
    units_to_bill = graphene.Int()
    description = graphene.String()
    rate = Currency()
    gst_status = graphene.Int()
    status = graphene.Int()


class InvoiceMatterInput(graphene.InputObjectType):
    id = graphene.ID()
    client = graphene.InputField(IDFieldInput)
    matter = graphene.InputField(IDFieldInput)
    manager = graphene.InputField(IDFieldInput)
    description = graphene.String()
    budget = Currency()


class TimeEntryInvoiceInput(graphene.InputObjectType):
    id = graphene.ID()
    units_to_bill = graphene.Float()


class InvoiceInput(graphene.InputObjectType):
    matter = graphene.InputField(InvoiceMatterInput)
    created_date = graphene.String()
    due_date = graphene.String()
    status = graphene.Int()
    recorded_time = graphene.List(TimeEntryInvoiceInput)
    fixed_price_items = graphene.List(InvoiceFixedPriceItemInput)
    billing_method = graphene.Int()


class InvoiceInfoInput(graphene.InputObjectType):
    matter = graphene.InputField(InvoiceMatterInput)
    created_date = graphene.String()
    due_date = graphene.String()
    status = graphene.InputField(IDFieldInput)
    billing_method = graphene.Int()
