from sitename.mixins import UpdateAttributesMixin
from sitename.utils import get_xero_client
from django.db import models
from simple_history.models import HistoricalRecords
from solo.models import SingletonModel

from .storage import OverwriteStorage

TIME_ENTRY = 1
DISBURSEMENT = 2
FIXED_PRICE_ITEM = 3

GST = 1
GST_EXPORT = 2
BAS_EXCLUDED = 3

GST_STATUSES = ((GST, 'GST (10%)'), (GST_EXPORT, 'GST Export (0%)'),
                (BAS_EXCLUDED, 'BAS Excluded (0%)'))

ENTRY_TYPES = ((TIME_ENTRY, 'Time Entry'), (DISBURSEMENT, 'Disbursement'),
               (FIXED_PRICE_ITEM, 'Fixed Price Item'))


class LeadStatus(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Lead statuses'

    def __str__(self):
        return self.name


class TimeEntryType(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Time Entry Type'

    def __str__(self):
        return self.name


class Industry(models.Model):
    name = models.CharField(max_length=200)
    reference = models.CharField(max_length=5, null=True, blank=True)

    class Meta:
        verbose_name_plural = "industries"
        ordering = ('name',)

    def __str__(self):
        return self.name


class Occupation(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Office(models.Model):
    legal_entity = models.CharField(max_length=30)
    abn = models.CharField(max_length=30)
    location = models.ForeignKey(
        'accounts.Location', null=True, on_delete=models.SET_NULL)
    phone = models.CharField(max_length=30)
    web = models.CharField(max_length=30)
    bank_account_name = models.CharField(max_length=30)
    bank_account_bsb = models.CharField(max_length=30)
    bank_account_number = models.CharField(max_length=30)
    bpay_biller_code = models.CharField(max_length=30)
    xero_branding_theme_name = models.CharField(max_length=30, null=True, blank=True, unique=True)
    xero_branding_theme_id = models.CharField(max_length=256, null=True, unique=True)

    def __str__(self):
        if self.location:
            return self.location.suburb or self.location.address1

        return 'No location'

    def get_branding_theme_id_from_xero(self):
        if not self.xero_branding_theme_name:
            return False

        xero = get_xero_client()

        try:
            res = xero.brandingthemes.filter(Name=self.xero_branding_theme_name)

            if res:
                self.xero_branding_theme_id = res[0].get('BrandingThemeID')
                self.save()
                return True

            return False
        except Exception as e:
            print(str(e))
            return False


class General(SingletonModel):
    gst_rate = models.FloatField()
    logo = models.ImageField()
    email_from_name = models.CharField(max_length=30)
    email_from_address = models.EmailField()
    smtp_server = models.CharField(max_length=30)
    smtp_username = models.CharField(max_length=30)
    smtp_password = models.CharField(max_length=30)
    smtp_port = models.CharField(max_length=30)

    def __str__(self):
        return "General Configuration"


class MatterType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class MatterSubType(models.Model):
    name = models.CharField(max_length=100)
    matter_type = models.ForeignKey(
        MatterType,
        related_name="subtypes",
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class InvoiceStatus(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Invoice statuses'

    def __str__(self):
        return self.name


class MatterStatus(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Matter statuses"

    def __str__(self):
        return self.name

class AccountNumber(models.Model):
    entry_type = models.IntegerField(choices=ENTRY_TYPES)
    gst_status = models.IntegerField(choices=GST_STATUSES)
    account_number = models.IntegerField(default=200)

    class Meta:
        verbose_name_plural = "Account numbers"
        ordering = ('entry_type', 'gst_status')
        unique_together = ('entry_type', 'gst_status')

    def __str__(self):
        return '{}, {} - {}'.format(self.get_entry_type_display(), self.get_gst_status_display(), self.account_number)


class PDF(models.Model):
    PDF_TYPES = ((1, 'Invoice'), (2, 'My Matter report'))
    name = models.CharField(max_length=30)
    pdf_type = models.IntegerField(
        choices=PDF_TYPES,
        verbose_name="PDF type",
        unique=True,
        null=True,
    )
    html = models.TextField()
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    def get_full_name(self):
        return self.name


class DocumentType(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class Section(models.Model):
    office = models.ForeignKey(
        'core.Office', null=True, blank=True, on_delete=models.SET_NULL)
    number = models.CharField(max_length=256)

    def __str__(self):
        return self.number


class Document(models.Model, UpdateAttributesMixin):
    DOCUMENT_STATUSES = (
        (1, 'Original held by Andreyev Lawyers'), (2, 'Removed'),
        (3, 'Not Returned'), (4, 'Transit Money held by Andreyev Lawyers'),
        (5, 'Scanned')
    )
    NOMINATED_TYPES = ((1, 'Executor'), (2, 'Attorney'),
                       (3, 'Guardian'), (4, 'Donee'),
                       (5, 'Substitute Decision Maker'), (6, 'Beneficiary'),
                       (7, 'Other'), (8, 'No Selection'))
    CHARGING_CLAUSE = ((1, 'Yes - Signed'), (2, 'n/a'), (3, 'Not returned'))

    contact = models.ForeignKey(
        'accounts.Contact',
        related_name="documents",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    organisation = models.ForeignKey(
        'accounts.Organisation',
        related_name="documents",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    owner = models.ForeignKey(
        'accounts.User',
        related_name="documents",
        null=True,
        on_delete=models.SET_NULL
    )
    date = models.DateField(null=True)
    date_removed = models.DateField(null=True, blank=True)
    status = models.IntegerField(choices=DOCUMENT_STATUSES, null=True)
    notes = models.TextField(null=True, blank=True)
    document_type = models.ForeignKey(
        DocumentType, null=True, on_delete=models.SET_NULL)
    nominated_type = models.IntegerField(choices=NOMINATED_TYPES, null=True)
    nominated_names = models.TextField(null=True, blank=True)
    andrew_executor = models.BooleanField(default=True)
    charging_clause = models.IntegerField(choices=CHARGING_CLAUSE, null=True)
    section = models.ForeignKey(
        Section,
        related_name="documents",
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.pk)


class EmailMessage(SingletonModel):
    body = models.TextField()
    from_email = models.EmailField(null=True)


class Logo(SingletonModel):
    logo = models.ImageField(
        upload_to="logo/", storage=OverwriteStorage(), null=True, blank=True)
