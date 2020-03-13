from django.contrib import admin

from sitename.admin import admin as sitename_admin
from simple_history.admin import SimpleHistoryAdmin
from solo.admin import SingletonModelAdmin

from .forms import PdfForm
from .models import (PDF, Document, DocumentType, EmailMessage, General,
                     Industry, InvoiceStatus, Logo, MatterSubType, MatterType,
                     Office, Section, Occupation, MatterStatus, LeadStatus,
                     TimeEntryType, AccountNumber)


sitename_admin.register(Section)
sitename_admin.register(DocumentType)
sitename_admin.register(MatterType)
sitename_admin.register(MatterStatus)
sitename_admin.register(MatterSubType)
sitename_admin.register(Occupation)
sitename_admin.register(InvoiceStatus)
sitename_admin.register(LeadStatus)
sitename_admin.register(TimeEntryType)
sitename_admin.register(AccountNumber)


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'contact', 'organisation')
    list_display_links = ('id', 'contact', 'organisation')
    list_filter = ('status', 'document_type')


class DocumentType(admin.ModelAdmin):
    list_display = ('name')


class PDFAdmin(SimpleHistoryAdmin):
    form = PdfForm

    def save_model(self, request, obj, form, change):
        super(PDFAdmin, self).save_model(request, obj, form, change)

        if obj.pdf_type is 1:
            file_name = 'invoice.html'
        elif obj.pdf_type is 2:
            file_name = 'my_matter_report.html'

        path = "templates/pdf/{}".format(file_name)

        with open(path, 'w') as html:
            html.write(obj.html)


class LogoAdmin(SingletonModelAdmin):

    def save_model(self, request, obj, form, change):
        obj.logo.name = 'logo.png'
        super(LogoAdmin, self).save_model(request, obj, form, change)


class OfficeAdmin(admin.ModelAdmin):
    autocomplete_fields = ['location']

    fieldsets = (
        (None,
            {'fields': (
                'legal_entity', 'abn', 'location', 'phone',
                'web', 'bank_account_name', 'bank_account_bsb',
                'bank_account_number', 'bpay_biller_code', 'xero_branding_theme_name')},
         ),
    )


class IndustryAdmin(admin.ModelAdmin):
    list_display = ('name', 'reference')


sitename_admin.register(Industry, IndustryAdmin)
sitename_admin.register(Document, DocumentAdmin)
sitename_admin.register(PDF, PDFAdmin)
sitename_admin.register(Logo, LogoAdmin)
sitename_admin.register(Office, OfficeAdmin)
sitename_admin.register(General, SingletonModelAdmin)
sitename_admin.register(EmailMessage, SingletonModelAdmin)
