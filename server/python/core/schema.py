import graphene
from sitename.decorators import login_required, login_required_relay
from core.connection import Connection
from django.db.models import FloatField
from django.db.models.functions import Cast
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphql_relay.node.node import from_global_id

from .models import Document
from .models import DocumentType as DocumentTypeModel
from .models import (Industry, InvoiceStatus, MatterSubType, MatterType,
                     Occupation, Office, Section)


class SectionType(DjangoObjectType):
    class Meta:
        model = Section


class DocumentTypeField(DjangoObjectType):
    class Meta:
        model = DocumentTypeModel


class DocumentType(DjangoObjectType):
    status = graphene.Int()
    status_display = graphene.String()
    nominated_type = graphene.Int()
    nominated_type_display = graphene.String()
    charging_clause = graphene.Int()
    charging_clause_display = graphene.String()

    class Meta:
        model = Document
        interfaces = (relay.Node,)
        filter_fields = []
        connection_class = Connection

    def resolve_status(self, info):
        return self.status

    def resolve_status_display(self, info):
        return self.get_status_display()

    def resolve_nominated_type(self, info):
        return self.nominated_type

    def resolve_nominated_type_display(self, info):
        return self.get_nominated_type_display()

    def resolve_charging_clause(self, info):
        return self.charging_clause

    def resolve_charging_clause_display(self, info):
        return self.get_charging_clause_display()


class IndustryType(DjangoObjectType):
    class Meta:
        model = Industry


class MatterTypeType(DjangoObjectType):
    class Meta:
        model = MatterType


class MatterSubTypeType(DjangoObjectType):
    class Meta:
        model = MatterSubType


class OccupationType(DjangoObjectType):
    class Meta:
        model = Occupation


class InvoiceStatusType(DjangoObjectType):
    class Meta:
        model = InvoiceStatus


class OfficeType(DjangoObjectType):
    suburb = graphene.String()
    name = graphene.String()
    short_name = graphene.String()

    def resolve_suburb(self, info):
        return self.location.suburb

    def resolve_name(self, info):
        return self.location.suburb

    def resolve_short_name(self, info):
        if self.location.suburb == 'Adelaide':
            return 'ADL'
        elif self.location.suburb == 'Sydney':
            return 'SYD'

        return 'Unknown'

    class Meta:
        model = Office


class Query:
    industries = graphene.List(IndustryType)
    matter_types = graphene.List(MatterTypeType)
    matter_sub_types = graphene.List(
        MatterSubTypeType, matter_type_id=graphene.ID()
    )
    invoice_statuses = graphene.List(InvoiceStatusType)
    offices = graphene.List(OfficeType)
    documents = DjangoFilterConnectionField(
        DocumentType,
        contact_id=graphene.ID(),
        organisation_id=graphene.ID()
    )
    document_types = graphene.List(DocumentTypeField)
    sections = graphene.List(SectionType)
    occupations = graphene.List(OccupationType)
    occupation = graphene.Field(
        OccupationType,
        occupation_id=graphene.ID()
    )

    @login_required
    def resolve_industries(self, info):
        return Industry.objects.all()

    @login_required
    def resolve_matter_types(self, info):
        return MatterType.objects.all()

    @login_required
    def resolve_matter_sub_types(self, info, matter_type_id=None):
        if matter_type_id:
            return MatterSubType.objects.filter(matter_type__id=matter_type_id)

        return MatterSubType.objects.all()

    @login_required
    def resolve_invoice_statuses(self, info):
        return InvoiceStatus.objects.all()

    @login_required
    def resolve_offices(self, info):
        return Office.objects.all()

    @login_required_relay
    def resolve_documents(self, info, **args):
        contact_id = args.get('contact_id')
        organisation_id = args.get('organisation_id')

        if contact_id:
            contact_id = from_global_id(contact_id)[1]
            return Document.objects.filter(contact__id=contact_id)

        if organisation_id:
            organisation_id = from_global_id(organisation_id)[1]
            return Document.objects.filter(organisation__id=organisation_id)

        return Document.objects.all()

    @login_required
    def resolve_document_types(self, info):
        return DocumentTypeModel.objects.all()

    @login_required
    def resolve_sections(self, info):
        return Section.objects.annotate(
                    section_number=Cast('number', FloatField())
                ).order_by('section_number').all()

    @login_required
    def resolve_occupations(self, info):
        return Occupation.objects.all()

    @login_required
    def resolve_occupation(self, info, occupation_id):
        if Occupation.objects.filter(id=occupation_id).exists():
            return Occupation.objects.get(id=occupation_id)
        return None
