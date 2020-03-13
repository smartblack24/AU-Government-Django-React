from django.contrib import admin

from sitename.admin import admin as sitename_admin

from .models import Invoice, Payment, PaymentTerms


class IsPaidFilter(admin.SimpleListFilter):

    title = ('paid')
    parameter_name = 'paid'

    def lookups(self, request, model_admin):
        return (
            ("True", "True (Net Outstanding = $0.00)"),
            ("False", "False (Net Outstanding > $0.00)")
        )

    def queryset(self, request, queryset):
        if self.value() == 'True':
            return Invoice.objects.filter(is_invoice_paid=True)
        elif self.value() == 'False':
            return Invoice.objects.filter(is_invoice_paid=False)


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('number', 'created_date', 'client_name', 'matter_name')
    list_filter = ('status', (IsPaidFilter))
    readonly_fields = ('invoice_id', 'matter_id')
    fieldsets = (
        (None,
            {'fields': (
                'invoice_id', 'matter_id', 'matter', 'created_date',
                'payment_terms', 'status', 'billing_method')},
         ),
    )

    def number(self, obj):
        return obj.number

    def client_name(self, obj):
        try:
            return obj.matter.client.name
        except AttributeError:
            return None

    def matter_name(self, obj):
        return obj.matter.name

    def matter_id(self, obj):
        return obj.matter.id

    def invoice_id(self, obj):
        return obj.id


sitename_admin.register(Invoice, InvoiceAdmin)
sitename_admin.register(Payment)
sitename_admin.register(PaymentTerms)
