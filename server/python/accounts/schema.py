from datetime import datetime, timedelta

import graphene
from sitename.decorators import login_required, login_required_relay
from billing.filters import MatterFilter
from billing.models import Matter, Note, TimeEntry
from billing.schema import MatterType, NoteType
from core.connection import Connection
from core.mixins import LoginRequiredRelayMixin
from core.scalars import Decimal as DecimalScalar
from django.conf import settings
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from .filters import ClientFilter, ContactFilter, UserFilter
from .models import Client, Contact, Location, Organisation, User


class LocationType(DjangoObjectType):
    state = graphene.Int()
    state_display = graphene.String()
    country = graphene.String()

    def resolve_state(self, info):
        return self.state

    def resolve_state_display(self, info):
        return self.get_state_display()

    def resolve_country(self, info):
        if self.country == '0':
            return ''
        else:
            return self.country

    class Meta:
        model = Location


class PostalLocationType(graphene.ObjectType):
    id = graphene.ID()
    postal_address1 = graphene.String()
    postal_address2 = graphene.String()
    postal_suburb = graphene.String()
    postal_state = graphene.Int()
    postal_post_code = graphene.String()
    postal_country = graphene.String()


class LocationInterface(graphene.Interface):
    addresses_are_equals = graphene.Boolean()
    postal_location = graphene.Field(PostalLocationType)

    def resolve_addresses_are_equals(self, info):
        return self.location == self.postal_location

    def resolve_postal_location(self, info):
        if self.postal_location:
            return PostalLocationType(
                id=self.postal_location.id,
                postal_address1=self.postal_location.address1,
                postal_address2=self.postal_location.address2,
                postal_suburb=self.postal_location.suburb,
                postal_state=self.postal_location.state,
                postal_post_code=self.postal_location.post_code,
                postal_country=self.postal_location.country,

            )

        return None


class OrganisationType(LoginRequiredRelayMixin, DjangoObjectType):
    group_status = graphene.Int()
    link_mails = graphene.Boolean()

    def resolve_group_status(self, info):
        return self.group_status
    
    def resolve_link_mails(self, info):
        return self.link_mails

    class Meta:
        model = Organisation
        interfaces = (relay.Node, LocationInterface)
        connection_class = Connection
        filter_fields = {
            'name': ['icontains']
        }


class UserType(LoginRequiredRelayMixin, DjangoObjectType):
    full_name = graphene.String()
    photo = graphene.String()
    salutation = graphene.Int()
    access = graphene.Int()
    location = graphene.Field(lambda: LocationType)
    rate = DecimalScalar()
    groups = graphene.List(graphene.String)
    has_gmail_account = graphene.Boolean()
    pointer = graphene.Int()
    addresses_are_equals = graphene.Boolean()
    can_use_xero = graphene.Boolean()
    can_link_mails = graphene.Boolean()
    can_delete_mails = graphene.Boolean()
    gmail = graphene.String()
    units_today = graphene.Int()
    units_week = graphene.Int()
    units_month = graphene.Int()
    mail_enabled = graphene.Boolean()

    class Meta:
        model = User
        interfaces = (relay.Node,)
        connection_class = Connection

    def resolve_full_name(self, info):
        return self.full_name

    def resolve_photo(self, info):
        if self.photo.name:
            return str(self.photo.url)

    def resolve_pointer(self, info):
        user = self

        matters = list(
            user.manager_of_matters.filter(
                billable_status=1).values_list('matter_status', flat=True)
        ) + list(user.assistant_of_matters.filter(
            billable_status=1).values_list('matter_status', flat=True))

        all_open_matters = (list(
            user.manager_of_matters.values_list('billable_status', flat=True))
            + list(user.assistant_of_matters.values_list(
                'billable_status', flat=True))).count(1)
        if all_open_matters == 0:
            all_open_matters = 1
        active_high = matters.count(1)
        active_moderate = matters.count(2)
        active_low = matters.count(3)
        waiting_for_internal_review = matters.count(4)
        waiting_for_AA_review = matters.count(5)
        waiting_for_external = matters.count(6)
        ad_hoc_work = matters.count(7)
        need_to_be_build = matters.count(8)
        pointer = ((active_high * 10
                   + active_moderate * 7
                   + active_low * 5
                   + waiting_for_internal_review * 2
                   + waiting_for_AA_review * 2
                   + waiting_for_external * 1.5
                   + ad_hoc_work * 4
                   + need_to_be_build * 1) / all_open_matters) * 2
        return pointer

    def resolve_salutation(self, info):
        return self.salutation

    def resolve_access(self, info):
        return self.access

    def resolve_location(self, info):
        # If no location -> return empty Location instance with fake id
        return self.location or Location(id=-1)

    def resolve_rate(self, info):
        return self.rate

    def resolve_groups(self, info):
        return [group['name'] for group in self.groups.values('name')]

    def resolve_has_gmail_account(self, info):
        return hasattr(self, 'gmail_account')

    def resolve_addresses_are_equals(self, info):
        return self.location == self.postal_location

    def resolve_can_use_xero(self, info):
        return self.can_use_xero

    def resolve_can_link_mails(self, info):
        return self.can_link_mails

    def resolve_can_delete_mails(self, info):
        return self.can_delete_mails

    def resolve_gmail(self, info):
        return self.gmail

    def resolve_units_today(self, info):
        today = self.time_entries.filter(
            date__day=datetime.now().date().day,
            date__month=datetime.now().date().month,
            date__year=datetime.now().date().year
            ).filter(
            entry_type=1)
        units = today.aggregate(Sum('units'))['units__sum']
        print(today)
        print(units)
        return int(units) if units else 0

    def resolve_units_month(self, info):
        month = self.time_entries.filter(entry_type=1).filter(
            date__month=datetime.now().month,
            date__year=datetime.now().year
            )
        units = month.aggregate(Sum('units'))['units__sum']
        return int(units) if units else 0

    def resolve_units_week(self, info):
        date = datetime.today()
        start_week = date - timedelta(date.weekday()) - timedelta(1)
        end_week = start_week + timedelta(7)
        week = self.time_entries.filter(entry_type=1).filter(
            date__range=(start_week, end_week)
            )
        units = week.aggregate(Sum('units'))['units__sum']
        return int(units) if units else 0

    def resolve_mail_enabled(self, info):
        return self.mail_enabled


class ContactType(LoginRequiredRelayMixin, DjangoObjectType):
    full_name = graphene.String()
    photo = graphene.String()
    salutation = graphene.Int()
    occupation = graphene.Int()
    notes = graphene.List(NoteType)
    last_note = graphene.Field(NoteType)
    spouse = graphene.Field(lambda: ContactType)
    second_contact = graphene.Field(lambda: ContactType)
    children = graphene.List(lambda: ContactType)
    link_mails = graphene.Boolean()

    class Meta:
        model = Contact
        interfaces = (relay.Node, LocationInterface)
        connection_class = Connection

    def resolve_full_name(self, info):
        return self.full_name

    def resolve_photo(self, info):
        if self.photo.name:
            return "{}{}".format(settings.SITE_URL, self.photo.url)

        return None

    def resolve_salutation(self, info):
        return self.salutation

    def resolve_occupation(self, info):
        return self.occupation.id

    def resolve_spouse(self, info):
        return self.get_spouse()

    def resolve_children(self, info):
        return self.children

    def resolve_notes(self, info):
        return self.notes.all().order_by('-date_time')

    def resolve_last_note(self, info):
        return self.notes.last()

    def resolve_link_mails(self, info):
        return self.link_mails


class ClientType(LoginRequiredRelayMixin, DjangoObjectType):
    name = graphene.String()
    organisation = graphene.Field(OrganisationType)
    second_contact = graphene.Field(ContactType)
    invoicing_address = graphene.String()
    street_address = graphene.String()
    matters_count = graphene.Int()
    matters = DjangoFilterConnectionField(
        MatterType, exclude_status=graphene.Int(),
        filterset_class=MatterFilter)

    class Meta:
        model = Client
        interfaces = (relay.Node, )
        connection_class = Connection

    def resolve_name(self, info):
        return self.__str__()

    def resolve_organisation(self, info):
        if self.organisation:
            return self.organisation

        return Organisation(id=-1)

    def resolve_invoicing_address(self, info):
        if self.organisation:
            return self.organisation.formatted_postal_address

        return self.contact.formatted_postal_address

    def resolve_street_address(self, info):
        if self.organisation:
            return self.organisation.formatted_street_address

        return self.contact.formatted_street_address

    def resolve_matters_count(self, info):
        return self.matters.count()

    def resolve_second_contact(self, info):
        return self.second_contact

    def resolve_matters(self, info, exclude_status=None):
        if exclude_status:
            return self.matters.exclude(billable_status=exclude_status)

        return self.matters.all()


class Query:
    me = graphene.Field(UserType)
    user = relay.Node.Field(UserType)
    legal = DjangoFilterConnectionField(UserType, filterset_class=UserFilter)
    users = DjangoFilterConnectionField(UserType, filterset_class=UserFilter)
    contact = relay.Node.Field(ContactType)
    contacts = DjangoFilterConnectionField(
        ContactType,
        all=graphene.Boolean(),
        exclude=graphene.ID(),
        filterset_class=ContactFilter,
    )
    organisations = DjangoFilterConnectionField(OrganisationType)
    organisation = relay.Node.Field(OrganisationType)
    clients = DjangoFilterConnectionField(
        ClientType,
        filterset_class=ClientFilter
    )
    client = relay.Node.Field(ClientType)
    notes = graphene.List(NoteType, contact_id=graphene.ID())

    @login_required
    def resolve_users(self, info, **args):
        return User.objects.all()

    @login_required
    def resolve_clients(self, info, **args):
        return Client.objects.all()

    @login_required
    def resolve_me(self, info):
        return info.context.user

    @login_required_relay
    def resolve_contacts(self, info, exclude=None, all=False, **args):
        if all:
            if exclude:
                return Contact.objects.exclude(pk=exclude)
            return Contact.objects.all()
        else:
            if exclude:
                return Contact.objects.filter(is_general=False
                                              ).exclude(pk=exclude)

            return Contact.objects.filter(is_general=False)

        return Contact.objects.none()

    @login_required
    def resolve_organisations(self, info, **args):
        return Organisation.objects.all()

    @login_required
    def resolve_notes(self, info, contact_id=None):
        return Note.objects.filter(contact_id=contact_id).order_by('-date_time')

    @login_required
    def resolve_legal(self, info, **args):
        return User.objects.filter(is_legal=True)
