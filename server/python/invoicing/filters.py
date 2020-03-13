import re

from django.db.models import Case, CharField, F, IntegerField, Q, When
from django.db.models.functions import Cast, Concat, Substr
from django_filters import BooleanFilter, CharFilter, FilterSet, NumberFilter

from .models import Invoice


class InvoiceFilter(FilterSet):
    number_or_client_name = CharFilter(
        name='number_or_client_name', method='number_or_client_name_filter')
    is_paid = BooleanFilter(name="is_paid", method="is_paid_filter")
    status = NumberFilter(name="status", method="status_filter")

    class Meta:
        model = Invoice
        fields = []

    def number_or_client_name_filter(self, queryset, name, value):
        if re.search('\d+', value):
            return queryset.annotate(
                a=Cast(
                    Substr(Cast('id', CharField(max_length=30)), 1, 1),
                    IntegerField()
                )).annotate(second_digit=Cast(
                    Substr(Cast('id', CharField(max_length=30)), 2, 1),
                    IntegerField()) * 2
            ).annotate(
                b=F('second_digit') / 10 + F('second_digit') % 10
            ).annotate(c=Cast(
                Substr(Cast('id', CharField(max_length=30)), 3, 1),
                IntegerField())
            ).annotate(fourth_digit=Cast(
                Substr(Cast('id', CharField(max_length=30)), 4, 1),
                IntegerField()) * 2
            ).annotate(
                d=F('fourth_digit') / 10 + F('fourth_digit') % 10
            ).annotate(step1=F('a') + F('b') + F('c') + F('d')
                       ).annotate(step2=F('step1') % 10
                                  ).annotate(step3=Cast(
                                      Case(
                                          When(step2=0, then=0),
                                          default=10 - F('step2')
                                      ),
                                      CharField(max_length=5))
            ).annotate(invoice_number=Concat(
                Substr(Cast('id', CharField(max_length=30)), 1, 4),
                F('step3')
            )).filter(invoice_number__icontains=value)

        try:
            first_name, last_name = value.split(" ")
            return queryset.filter(
                (Q(matter__client__contact__first_name__icontains=first_name) &
                 Q(matter__client__contact__last_name__icontains=last_name)) |
                (Q(matter__client__second_contact__first_name__icontains=first_name) &
                 Q(matter__client__second_contact__last_name__icontains=last_name)
                 ) |
                Q(matter__client__organisation__name__icontains=value)
            )
        except ValueError:
            first_name = value
            last_name = value

            return queryset.filter(
                Q(matter__client__contact__first_name__icontains=value) |
                Q(matter__client__contact__last_name__icontains=value) |
                Q(matter__client__second_contact__first_name__icontains=value) |
                Q(matter__client__second_contact__last_name__icontains=value) |
                Q(matter__client__organisation__name__icontains=value)

            )

    def is_paid_filter(self, queryset, name, value):
        if value is True:
            return queryset.filter(is_invoice_paid=True)

        elif value is False:
            return queryset.filter(is_invoice_paid=False)
        # invoices = Invoice.objects.raw("""
        #     SELECT
        #         i.id
        #     FROM invoicing_invoice i
        #     LEFT JOIN (
        #     SELECT
        #         ti.invoice_id,
        #         SUM(
        #             COALESCE(ti.rate, COALESCE(s.rate, 0), 0) * ti.units
        #         ) AS totalInvoice
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
        #     HAVING (
        #         COALESCE(t.totalInvoice, 0)
        #      - COALESCE(p.totalPyments, 0) <= 0);
        # """)
        #
        # invoice_ids = [inv.id for inv in invoices]
        #
        # if value is True:
        #     return queryset.filter(id__in=invoice_ids)
        #
        # elif value is False:
        #     return queryset.exclude(id__in=invoice_ids)

    def status_filter(self, queryset, name, value):
        if value == 0:
            return queryset
        else:
            return queryset.filter(status_id=value)
