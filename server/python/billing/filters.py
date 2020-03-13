from datetime import date, timedelta

from django.db.models import Q
from django_filters import BooleanFilter, CharFilter, FilterSet, NumberFilter
from graphql_relay.node.node import from_global_id
from .models import Matter, TimeEntry


class MatterFilter(FilterSet):
    client_name = CharFilter(name='client_name', method='client_name_filter')
    matter_report = CharFilter(
        name='matter_report', method='matter_report_filter')
    principal_name = CharFilter(
        name='principal_name', method='principal_name_filter')
    manager_name = CharFilter(
        name='manager_name', method='manager_name_filter')
    assistant_name = CharFilter(
        name='assistant_name', method='assistant_name_filter')
    is_paid = BooleanFilter(name='is_paid', method="is_paid_filter")
    staff_name = CharFilter(name='staff_name', method='staff_name_filter')
    billable_status_exclude = NumberFilter(
        name="billable_status_exclude",
        method="billable_status_exclude_filter"
    )
    matter_status = CharFilter(
        name='matter_status', method='matter_status_filter')
    lead_type = BooleanFilter(name='lead_type', method='lead_type_filter')
    lead_status = CharFilter(name='lead_status', method='lead_status_filter')
    active_leads = BooleanFilter(
        name="active_leads",
        method="active_leads_filter"
        )

    class Meta:
        model = Matter
        fields = {
            'name': ['icontains'],
            'client__id': ['exact'],
            'billable_status': ['exact']
        }

    def active_leads_filter(self, queryset, name, value):
        if value:
            return queryset.exclude(lead_status_id=6)
        return queryset

    def lead_status_filter(self, queryset, name, value):
            return queryset.filter(
                lead_status_id=int(value)
                )

    def lead_type_filter(self, queryset, name, value):
        if value:
            return queryset.filter(entry_type_id=2).filter(billable_status=1)
        return queryset.filter(entry_type=1)

    def client_name_filter(self, queryset, name, value):
        result = value.split(' - ')
        try:
            if len(result) == 2:
                first_name, last_name = result[-1].split()
            else:
                first_name, last_name = value.split()

            return queryset.filter(
                Q(client__organisation__name__icontains=value) |
                (Q(client__contact__first_name__icontains=first_name) &
                 Q(client__contact__last_name__icontains=last_name))
            ).order_by('matter_status', 'client_name')
        except ValueError:
            first_name = value
            last_name = value

            return queryset.filter(
                Q(client__organisation__name__icontains=value) |
                Q(client__contact__first_name__icontains=value) |
                Q(client__contact__last_name__icontains=value)
            ).order_by('matter_status', 'client_name')

    def principal_name_filter(self, queryset, name, value):
        try:
            first_name, last_name = value.split()

            return queryset.filter(
                (Q(principal__first_name__icontains=first_name) &
                 Q(principal__last_name__icontains=last_name))
            ).order_by('matter_status', 'client_name')
        except ValueError:
            first_name = value
            last_name = value

            return queryset.filter(
                Q(principal__first_name__icontains=value) |
                Q(principal__last_name__icontains=value)
            ).order_by('matter_status', 'client_name')

    def manager_name_filter(self, queryset, name, value):
        try:
            first_name, last_name = value.split()

            return queryset.filter(
                (Q(manager__first_name__icontains=first_name) &
                 Q(manager__last_name__icontains=last_name))
            ).order_by('matter_status', 'client_name')
        except ValueError:
            first_name = value
            last_name = value

            return queryset.filter(
                Q(manager__first_name__icontains=value) |
                Q(manager__last_name__icontains=value)
            ).order_by('matter_status', 'client_name')

    def assistant_name_filter(self, queryset, name, value):
        try:
            first_name, last_name = value.split()

            return queryset.filter(
                (Q(assistant__first_name__icontains=first_name) &
                 Q(assistant__last_name__icontains=last_name))
            ).order_by('matter_status', 'client_name')
        except ValueError:
            first_name = value
            last_name = value

            return queryset.filter(
                Q(assistant__first_name__icontains=value) |
                Q(manager__last_name__icontains=value)
            ).order_by('matter_status', 'client_name')

    def staff_name_filter(self, queryset, name, value):
        try:
            first_name, last_name = value.split()

            return queryset.filter(
                (Q(principal__first_name__icontains=first_name) &
                 Q(principal__last_name__icontains=last_name)) |
                (Q(manager__first_name__icontains=first_name) &
                 Q(manager__last_name__icontains=last_name)) |
                (Q(assistant__first_name__icontains=first_name) &
                 Q(assistant__last_name__icontains=last_name))
            ).order_by('matter_status', 'client_name')
        except ValueError:
            first_name = value
            last_name = value

            return queryset.filter(
                (Q(principal__first_name__icontains=value) |
                 Q(principal__last_name__icontains=value)) |
                (Q(manager__first_name__icontains=first_name) |
                 Q(manager__last_name__icontains=last_name)) |
                (Q(assistant__first_name__icontains=first_name) |
                 Q(assistant__last_name__icontains=last_name))
            ).order_by('matter_status', 'client_name')

    def is_paid_filter(self, queryset, name, value):
        # matters = queryset.raw('''
        #     SELECT
        #         matters.id
        #     FROM billing_matter matters
        #     LEFT JOIN (
        #     SELECT
        #         i.id,
        #         i.matter_id,
        #         (COALESCE(t.totalInvoice, 0) + COALESCE(t.totalInvoice, 0) / 10) - COALESCE(p.totalPyments, 0) <= 0 AS isPaid
        #     FROM invoicing_invoice i
        #     LEFT JOIN (
        #     SELECT
        #         ti.invoice_id,
        #         SUM(ti.units) AS totalUnits,
        #         SUM(COALESCE(ti.rate, COALESCE(s.rate, 0), 0) * ti.units / 10) AS totalInvoice
        #     FROM billing_timeentry ti
        #     LEFT JOIN accounts_user s ON ti.staff_member_id = s.id
        #     LEFT JOIN (
        #         SELECT
        #         id,
        #         billing_method AS matter_billing_method
        #         FROM billing_matter
        #         GROUP BY id, billing_method
        #     ) m ON ti.matter_id=m.id
        #     WHERE (
        #         CASE
        #         WHEN m.matter_billing_method = 1 THEN (ti.entry_type = 2 OR ti.entry_type = 3)
        #         WHEN m.matter_billing_method = 2 THEN (ti.entry_type = 1 OR ti.entry_type = 2)
        #         END
        #     )
        #     GROUP BY ti.invoice_id
        #     ) t ON t.invoice_id = i.id
        #     LEFT JOIN (
        #     SELECT
        #         invoice_id,
        #         SUM(COALESCE(amount, 0)) AS totalPyments
        #     FROM invoicing_payment
        #     GROUP BY invoice_id
        #     ) p ON p.invoice_id = i.id
        #     GROUP BY i.id, t.totalInvoice, p.totalPyments, i.matter_id
        #     ) invoices ON invoices.matter_id = matters.id
        #     GROUP BY matters.id
        #     HAVING bool_and(COALESCE(invoices.isPaid, true))
        # ''')
        # matter_ids = [m.id for m in matters]

        if value is True:
            return queryset.filter(is_matter_paid=True).order_by(
                'matter_status', 'client_name')

        elif value is False:
            return queryset.filter(is_matter_paid=False).order_by(
                'matter_status', 'client_name')

    def billable_status_exclude_filter(self, queryset, name, value):
        return queryset.exclude(billable_status=value).order_by(
            'matter_status', 'client_name')

    def matter_report_filter(self, queryset, name, value):
        try:
            first_name, last_name = value.split()

            return queryset.filter(
                (Q(manager__first_name__icontains=first_name) &
                 Q(manager__last_name__icontains=last_name)) |
                (Q(assistant__first_name__icontains=first_name) &
                 Q(assistant__last_name__icontains=last_name))
            ).order_by('matter_status', 'client_name')
        except ValueError:
            first_name = value
            last_name = value

            return queryset.filter(
                (Q(principal__first_name__icontains=value) |
                 Q(principal__last_name__icontains=value)) |
                (Q(assistant__first_name__icontains=first_name) |
                 Q(assistant__last_name__icontains=last_name))
            ).order_by('matter_status', 'client_name')

    def matter_status_filter(self, queryset, name, value):
        return queryset.filter(matter_status_id=int(value)).order_by(
            'matter_status', 'client_name')


class TimeEntryFilter(FilterSet):
    client_name = CharFilter(name='client_name', method='client_name_filter')
    client_id = CharFilter(name='client_id', method='client_id_filter')
    is_billed = BooleanFilter(name='is_billed', method='is_billed_filter')
    staff_name = CharFilter(name='staff_name', method='staff_name_filter')
    date = CharFilter(name="date", method='date_filter')
    to_date = CharFilter(name="to_date", method='to_date_filter')
    from_date = CharFilter(name="from_date", method='from_date_filter')
    entry_type = CharFilter(name="entry_type", method="entry_type_filter")
    time_entry_type = CharFilter(
        name="time_entry_type",
        method="time_entry_type_filter"
        )

    class Meta:
        model = TimeEntry
        fields = {
            'matter__name': ['icontains'],
            'rate': ['exact'],
        }

    def time_entry_type_filter(self, queryset, name, value):
        if value:
            return queryset.filter(time_entry_type_id=int(value))
        return queryset

    def client_id_filter(self, queryset, name, value):
        if value:
            return queryset.filter(client_id=from_global_id(value)[1])
        else:
            return queryset

    def entry_type_filter(self, queryset, name, value):
        return queryset.filter(entry_type=int(value)).order_by('-date')

    def client_name_filter(self, queryset, name, value):
        try:
            first_name, last_name = value.split()

            return queryset.filter(
                Q(client__organisation__name__icontains=value) |
                (Q(client__contact__first_name__icontains=first_name) &
                 Q(client__contact__last_name__icontains=last_name))
            ).order_by('-date')
        except ValueError:
            first_name = value
            last_name = value

            return queryset.filter(
                Q(client__organisation__name__icontains=value) |
                Q(client__contact__first_name__icontains=value) |
                Q(client__contact__last_name__icontains=value)
            ).order_by('-date')

    def is_billed_filter(self, queryset, name, value):
        return queryset.filter(invoice__isnull=not value).order_by('-date')

    def staff_name_filter(self, queryset, name, value):
        try:
            first_name, last_name = value.split()

            return queryset.filter(
                (Q(staff_member__first_name__icontains=first_name) &
                 Q(staff_member__last_name__icontains=last_name))
            ).order_by('-date')
        except ValueError:
            first_name = value
            last_name = value

            return queryset.filter(
                (Q(staff_member__first_name__icontains=first_name) |
                 Q(staff_member__last_name__icontains=last_name))
            ).order_by('-date')

    def date_filter(self, queryset, name, value):
        try:
            day, month, year = value.split('/')
            time_entry_date = date(
                day=int(day), month=int(month), year=int(year))
        except Exception as e:
            return queryset.none()
        return queryset.filter(
            date__day=time_entry_date.day,
            date__month=time_entry_date.month,
            date__year=time_entry_date.year,
            ).order_by('-date')

    def from_date_filter(self, queryset, name, value):
        first_date = queryset.order_by('date').last()
        try:
            day, month, year = value.split('/')
            time_entry_date = date(
                day=int(day), month=int(month), year=int(year))
            first_date = date(
                day=first_date.date.day,
                month=first_date.date.month,
                year=first_date.date.year
                ) + timedelta(days=1)
        except Exception as e:
            return queryset.none()
        return queryset.filter(
            date__range=(time_entry_date, first_date)).order_by('-date')

    def to_date_filter(self, queryset, name, value):
        last_date = queryset.order_by('date').first()
        try:
            day, month, year = value.split('/')
            time_entry_date = date(
                day=int(day), month=int(month), year=int(year)) + timedelta(days=1)
            end_date = date(
                day=last_date.date.day,
                month=last_date.date.month,
                year=last_date.date.year
                ) + timedelta(days=1)
        except Exception as e:
            return queryset.none()
        return queryset.filter(
            date__range=(end_date, time_entry_date)).order_by('-date')


class InvoiceRecordsFilter(FilterSet):
    invoice_id = CharFilter(name='invoice_id', method='invoice_id_filter')
    entry_type = CharFilter(name='entry_type', method='entry_type_filter')
    time_records = BooleanFilter(
        name='time_records',
        method='time_records_filter'
        )

    class Meta:
        model = TimeEntry
        fields = []

    def time_records_filter(self, queryset, name, value):
        if value:
            return queryset.filter(entry_type=1)
        return queryset

    def invoice_id_filter(self, queryset, name, value):
        id = from_global_id(value)[1]
        return queryset.filter(invoice_id=id)

    def entry_type_filter(self, queryset, name, value):
        if int(value) == 1:
            return queryset.exclude(entry_type=1)
        elif int(value) == 2:
            return queryset.exclude(entry_type=3)
