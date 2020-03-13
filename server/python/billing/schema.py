import graphene
from sitename.decorators import login_required, login_required_relay
from core.connection import Connection
from core.mixins import LoginRequiredRelayMixin
from core.scalars import Decimal as DecimalField
from django.db.models import Case, CharField, Q, Value, When
from django.db.models.functions import Concat
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from .filters import MatterFilter, TimeEntryFilter, InvoiceRecordsFilter
from .models import Matter, Note, StandartDisbursement, TimeEntry


class NoteType(DjangoObjectType):
    class Meta:
        model = Note


class TimeEntryType(LoginRequiredRelayMixin, DjangoObjectType):
    status_display = graphene.String()
    gst_status = graphene.Int()
    gst_status_display = graphene.String()
    cost = DecimalField()
    status = graphene.Int()
    billed_value = graphene.Float()
    rate = DecimalField()
    is_billed = graphene.Boolean()
    entry_type = graphene.Int()
    record_type = graphene.Int()

    class Meta:
        model = TimeEntry
        interfaces = (relay.Node,)
        connection_class = Connection

    def resolve_record_type(self, info):
        return self.time_entry_type.id

    def resolve_status_display(self, info):
        return self.get_status_display()

    def resolve_cost(self, info):
        return self.cost

    def resolve_status(self, info):
        return self.status

    def resolve_gst_status(self, info):
        return self.gst_status

    def resolve_gst_status_display(self, info):
        return self.get_gst_status_display()

    def resolve_billed_value(self, info):
        return self.billed_value

    def resolve_rate(self, info):
        if self.rate:
            return self.rate

        if self.staff_member:
            return self.staff_member.rate

        return 0

    def resolve_entry_type(self, info):
        return self.entry_type

    def resolve_is_billed(self, info):
        return bool(self.invoice)


class MatterType(LoginRequiredRelayMixin, DjangoObjectType):
    conflict_status = graphene.Int()
    billable_status = graphene.Int()
    billable_status_display = graphene.String()
    billing_method = graphene.Int()
    total_time_value = DecimalField()
    unbilled_time = graphene.List(TimeEntryType)
    total_time_invoiced = DecimalField()
    wip = DecimalField()
    amount_outstanding = DecimalField()
    is_paid = graphene.Boolean()
    days_open = graphene.Int()
    notes = graphene.List(NoteType)
    matter_status = graphene.Int()
    matter_status_display = graphene.String()
    last_note = graphene.Field(NoteType)
    total_invoiced_value = DecimalField()
    entry_type = graphene.Int()
    entry_type_display = graphene.String()
    matter_id = graphene.Int()
    lead_date = graphene.String()
    lead_status = graphene.Int()
    lead_status_display = graphene.String()

    class Meta:
        model = Matter
        interfaces = (relay.Node,)
        connection_class = Connection

    def resolve_lead_status_display(self, info):
        return self.lead_status.name

    def resolve_lead_status(self, info):
        return self.lead_status.id

    def resolve_lead_date(self, info):
        return self.lead_date

    def resolve_entry_type(self, info):
        return self.entry_type_id

    def resolve_entry_type_display(self, info):
        return self.entry_type.name

    def resolve_conflict_status(self, info):
        return self.conflict_status

    def resolve_billable_status(self, info):
        return self.billable_status

    def resolve_billing_method(self, info):
        return self.billing_method

    def resolve_billable_status_display(self, info):
        return self.get_billable_status_display()

    def resolve_total_time_value(self, info):
        return self.total_time_value

    def resolve_unbilled_time(self, info):
        return self.unbilled_time

    def resolve_total_time_invoiced(self, info):
        return self.total_time_invoiced(gst=False)

    def resolve_wip(self, info):
        return self.wip

    def resolve_amount_outstanding(self, info):
        return self.amount_outstanding

    def resolve_is_paid(self, info):
        return self.is_paid

    def resolve_days_open(self, info):
        return self.days_open

    def resolve_notes(self, info):
        return self.notes.all().order_by('-date_time')

    def resolve_matter_status(self, info):
        return self.matter_status_id

    def resolve_matter_status_display(self, info):
        return self.matter_status.name

    def resolve_last_note(self, info):
        return self.notes.last()

    def resolve_total_invoiced_value(self, info):
        return self.total_invoiced_value(gst=False)

    def resolve_matter_id(self, info):
        return self.id


class StandartDisbursementType(DjangoObjectType):
    gst_status = graphene.Int()

    class Meta:
        model = StandartDisbursement
        interfaces = (relay.Node,)
        filter_fields = {'name': ['icontains']}


class Query:
    matters = DjangoFilterConnectionField(
        MatterType, filterset_class=MatterFilter)
    matter = relay.Node.Field(MatterType)
    time_entries = DjangoFilterConnectionField(
        TimeEntryType, filterset_class=TimeEntryFilter)
    time_entry = relay.Node.Field(TimeEntryType)
    standart_disbursements = DjangoFilterConnectionField(
        StandartDisbursementType)
    notes = graphene.List(NoteType, matter_id=graphene.ID())
    invoice_records = DjangoFilterConnectionField(
        TimeEntryType, filterset_class=InvoiceRecordsFilter)

    @login_required
    def resolve_standart_disbursements(self, info, **args):
        return StandartDisbursement.objects.all()

    @login_required_relay
    def resolve_matters(self, info, **args):
        return Matter.objects.annotate(client_name=Case(When(
            Q(client__organisation__isnull=False) &
            Q(client__contact__isnull=False),
            then=Concat(
                'client__organisation__name',
                Value(' - '),
                'client__contact__first_name',
                Value(' '),
                'client__contact__last_name')
        ), When(
            Q(client__organisation__isnull=False) &
            Q(client__contact__isnull=True),
            then=Concat(
                'client__organisation__name',
                Value(' - '),
                Value('No Contact')
            )), When(
                Q(client__organisation__isnull=True) &
                Q(client__contact__isnull=False),
                then=Concat(
                    'client__contact__first_name',
                    Value(' '),
                    'client__contact__last_name'
                )), When(
                    Q(client__organisation__isnull=True) &
                    Q(client__contact__isnull=True),
                    then=Value(
                        'Have neither Organisation or Contact associated'
                    )),
            output_field=CharField())
        ).order_by('client_name')

    @login_required
    def resolve_time_entries(self, info, **args):
        return TimeEntry.objects.all()

    @login_required
    def resolve_notes(self, info, matter_id=None):
        return Note.objects.filter(matter_id=matter_id).order_by('-date_time')
