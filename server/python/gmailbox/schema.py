import datetime
from itertools import chain

import graphene
from sitename.decorators import login_required, login_required_relay
from core.connection import Connection
from core.mixins import LoginRequiredRelayMixin
from core.utils import get_paginator
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphql_relay.node.node import from_global_id
from billing.schema import MatterType

from .models import Mail, Attachment
from .filters import MailFilter


class AttachmentType(LoginRequiredRelayMixin, DjangoObjectType):
    class Meta:
        model = Attachment

class MailType(LoginRequiredRelayMixin, DjangoObjectType):
    sender_name = graphene.String()
    sender_address = graphene.String()
    recipient_name = graphene.String()
    recipient_address = graphene.String()
    subject = graphene.String()
    snippet = graphene.String()
    date = graphene.String()
    attachments = graphene.List(AttachmentType)
    matter = graphene.Field(MatterType)
    available_matters = graphene.List(MatterType)
    has_attachments = graphene.Boolean()

    class Meta:
        model = Mail
        interfaces = (relay.Node,)
        connection_class = Connection

    def resolve_sender_name(self, info):
        return self.sender_name

    def resolve_sender_address(self, info):
        return self.sender_address

    def resolve_recipient_name(self, info):
        return self.recipient_name

    def resolve_recipient_address(self, info):
        return self.recipient_address

    def resolve_subject(self, info):
        return self.subject

    def resolve_date(self, info):
        return self.date

    def resolve_attachments(self, info):
        return self.attachments.filter(inline=False)

    def resolve_matter(self, info):
        return self.matter

    def resolve_available_matters(self, info):
        return self.available_matters

    def resolve_has_attachments(self, info):
        return self.attachments.filter(inline=False).count() > 0


class Query:
    mails = DjangoFilterConnectionField(
        MailType, filterset_class=MailFilter
    )
    mail = relay.Node.Field(MailType)
    available_matters_of_mails = graphene.List(
        MailType,
        mails=graphene.List(graphene.ID)
    )

    @login_required_relay
    def resolve_mails(self, info, **args):
        return Mail.objects.filter(hidden=False)

    @login_required_relay
    def resolve_available_matters_of_mails(self, info, **args):
        mail_ids = [from_global_id(mail)[1] for mail in args.get('mails')]
        return Mail.objects.filter(id__in=mail_ids)
