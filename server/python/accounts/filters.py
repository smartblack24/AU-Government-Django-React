from django.db.models import Q
from django_filters import BooleanFilter, CharFilter, FilterSet

from .models import Client, Contact


class ContactFilter(FilterSet):
    full_name = CharFilter(name='full_name', method='full_name_filter')

    class Meta:
        model = Contact
        fields = ['first_name', 'email', 'mobile']

    def full_name_filter(self, queryset, name, value):
        try:
            first_name, last_name = value.split()

            return queryset.filter(
                Q(mobile__icontains=value) |
                Q(email__icontains=value) |
                Q(first_name__icontains=first_name) &
                Q(last_name__icontains=last_name)
            )
        except ValueError:
            first_name = value
            last_name = value

            return queryset.filter(
                Q(mobile__icontains=value) |
                Q(email__icontains=value) |
                Q(first_name__icontains=first_name) |
                Q(last_name__icontains=last_name)
            )


class ClientFilter(FilterSet):
    name = CharFilter(name='name', method='name_filter')
    with_matter = BooleanFilter(
        name='with_matter', method="with_matter_filter")
    with_open_matter = BooleanFilter(
        name='with_open_matter', method="with_open_matter_filter")

    class Meta:
        model = Client
        fields = ['contact__first_name', 'matters__id']

    def name_filter(self, queryset, name, value):
        try:
            first_name, last_name = value.split()

            return queryset.filter(
                Q(organisation__name__icontains=value) |
                (Q(contact__first_name__icontains=first_name) &
                 Q(contact__last_name__icontains=last_name))
            )
        except ValueError:
            first_name = value
            last_name = value

            return queryset.filter(
                Q(organisation__name__icontains=value) |
                Q(contact__first_name__icontains=value) |
                Q(contact__last_name__icontains=value)
            )

    def with_matter_filter(self, queryset, name, value):
        if value is True:
            return queryset.exclude(matters=None)
        else:
            return queryset.all()

    def with_open_matter_filter(self, queryset, name, value):
        if value is True:
            clients = queryset.filter(matters__billable_status=1)
            return clients.distinct()
        else:
            return queryset.all()


class UserFilter(FilterSet):
    fullName = CharFilter(name='full_name', method='full_name_filter')

    class Meta:
        model = Client
        fields = ['is_active']

    def full_name_filter(self, queryset, name, value):
        try:
            first_name, last_name = value.split()

            return queryset.filter(
                (Q(first_name__icontains=first_name) &
                 Q(last_name__icontains=last_name))
            ).filter(is_active=True)
        except ValueError:
            first_name = value
            last_name = value

            return queryset.filter(
                Q(first_name__icontains=value) |
                Q(last_name__icontains=value)
            ).filter(is_active=True)
