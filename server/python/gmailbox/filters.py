from django.db.models import Q
from django_filters import CharFilter, FilterSet

from graphql_relay.node.node import from_global_id

from sitename.utils import get_date_from_str

from .models import Mail


class MailFilter(FilterSet):
    sender = CharFilter(name='sender', method='filter_sender')
    recipient = CharFilter(name='sender', method='filter_recipient')
    subject = CharFilter(name='sender', method='filter_subject')
    date_from = CharFilter(name='sender', method='filter_date_from')
    date_to = CharFilter(name='date_to', method='filter_date_to')
    order_by = CharFilter(name='order_by', method='filter_order_by')
    contact_id = CharFilter(name='contact', method='filter_contact')
    organisation_id = CharFilter(name='organisation', method='filter_organisation')
    matter_id = CharFilter(name='matter', method='filter_matter')

    class Meta:
        model = Mail
        fields = []

    def filter_sender(self, queryset, name, value):
        return queryset.filter(
            Q(sender_name__icontains=value) | Q(sender_address__icontains=value)
        )

    def filter_recipient(self, queryset, name, value):
        return queryset.filter(
            Q(recipient_name__icontains=value) | Q(recipient_address__icontains=value)
        )

    def filter_subject(self, queryset, name, value):
        return queryset.filter(subject__icontains=value)

    def filter_date_from(self, queryset, name, value):
        date = get_date_from_str(value, 'start')
        return queryset.filter(date__gte=date) if date else queryset.none()

    def filter_date_to(self, queryset, name, value):
        date = get_date_from_str(value, 'end')
        return queryset.filter(date__lte=date) if date else queryset.none()

    def filter_order_by(self, queryset, name, value):
        if 'sender' in value or 'recipient' in value:
            name = value + '_name'
            address = value + '_address'

            return queryset.order_by(name, address)

        return queryset.order_by(value)

    def filter_contact(self, queryset, name, value):
        contact_id = from_global_id(value)[1]
        return queryset.filter(contacts__in=[contact_id])

    def filter_organisation(self, queryset, name, value):
        organisation_id = from_global_id(value)[1]
        return queryset.filter(organisations__in=[organisation_id])

    def filter_matter(self, queryset, name, value):
        matter_id = from_global_id(value)[1]
        return queryset.filter(matter_id=matter_id)
