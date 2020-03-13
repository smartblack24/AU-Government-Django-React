from datetime import date, datetime
from itertools import chain

import graphene
from sitename.decorators import login_required_relay
from billing.filters import TimeEntryFilter
from billing.schema import TimeEntryType
from core.connection import Connection
from core.mixins import LoginRequiredRelayMixin
from core.scalars import Decimal
from graphene import relay
from graphene_django.converter import convert_django_field
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from simple_history.models import HistoricalRecords

from .filters import InvoiceFilter
from .models import Invoice, Payment
from .scalars import HistoricalRecord


@convert_django_field.register(HistoricalRecords)
def convert_location_field(field, registry=None):
    return HistoricalRecord()


class PaymentType(DjangoObjectType):
    method_display = graphene.String()
    amount = Decimal()

    def resolve_method_display(self, info):
        return self.get_method_display()

    def resolve_amount(self, info):
        return self.amount

    class Meta:
        model = Payment


class InvoiceType(LoginRequiredRelayMixin, DjangoObjectType):
    status_display = graphene.String()
    value_ex_GST = Decimal()
    value_incl_GST = Decimal()
    received_payments = Decimal()
    net_outstanding = Decimal()
    history = graphene.List(HistoricalRecord)
    total_billed_value = Decimal()
    is_paid = graphene.Boolean()
    due_date = graphene.String()
    number = graphene.ID()
    friendly_reminder = graphene.Boolean()
    first_reminder = graphene.Boolean()
    second_reminder = graphene.Boolean()
    time_entries = DjangoFilterConnectionField(
        TimeEntryType, filterset_class=TimeEntryFilter)
    billing_method = graphene.Int()
    time_entry_value = Decimal()
    fixed_price_value = Decimal()
    can_send_xero = graphene.Boolean()
    is_in_xero = graphene.Boolean()

    class Meta:
        model = Invoice
        interfaces = (relay.Node,)
        connection_class = Connection

    def resolve_time_entry_value(self, info):
        return self.time_entry_value

    def resolve_fixed_price_value(self, info):
        return self.fixed_price_value

    def resolve_status_display(self, info):
        return self.status.name

    def resolve_value_ex_GST(self, info):
        return self.value()

    def resolve_value_incl_GST(self, info):
        return self.value(gst=True)

    def resolve_received_payments(self, info):
        return self.received_payments

    def resolve_net_outstanding(self, info):
        return self.net_outstanding

    def resolve_history(self, info):
        return sorted(chain(
            self.history.exclude(history_change_reason__isnull=True),
            *[payment.history.exclude(history_change_reason__isnull=True)
              for payment in self.payments.all()]
        ), key=lambda x: x.history_date, reverse=True)

    def resolve_total_billed_value(self, info):
        return self.total_billed_value

    def resolve_is_paid(self, info):
        return self.is_paid

    def resolve_due_date(self, info):
        return self.due_date

    def resolve_number(self, info):
        return self.number

    def resolve_friendly_reminder(self, info):
        try:
            return not self.is_paid and \
                (date.today() - self.due_date).days >= 14
        except TypeError:
            return not self.is_paid and \
                (datetime.now() - self.due_date).days >= 14

    def resolve_first_reminder(self, info):
        try:
            return not self.is_paid and \
                (date.today() - self.due_date).days >= 28
        except TypeError:
            return not self.is_paid and \
                (datetime.now() - self.due_date).days >= 28

    def resolve_second_reminder(self, info):
        try:
            return not self.is_paid and \
                (date.today() - self.due_date).days >= 42
        except TypeError:
            return not self.is_paid and \
                (datetime.now() - self.due_date).days >= 42

    def resolve_time_entries(self, info, **args):
        return self.time_entries.all()

    def resolve_billing_method(self, info):
        return self.billing_method

    def resolve_can_send_xero(self, info):
        return self.can_send_xero

    def resolve_is_in_xero(self, info):
        return self.is_in_xero


class Query:
    invoices = DjangoFilterConnectionField(
        InvoiceType, filterset_class=InvoiceFilter)
    invoice = relay.Node.Field(InvoiceType)

    @login_required_relay
    def resolve_invoices(self, info, **args):
        return Invoice.objects.all()
