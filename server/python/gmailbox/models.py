import re

from django.db import models
from django.db.models import Q

from billing.models import Matter


class GmailAccount(models.Model):
    user = models.OneToOneField(
        'accounts.User',
        related_name='gmail_account',
        on_delete=models.CASCADE
    )
    address = models.EmailField(max_length=256, null=True, blank=True)
    token = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return self.user.full_name

    @property
    def latest_mail_date(self):
        queryset = Mail.objects.filter(
            Q(sender_address=self.address) | Q(recipient_address=self.address)
        )
        return queryset.latest('date').date if queryset.exists() else None


class Mail(models.Model):
    contacts = models.ManyToManyField(
        'accounts.Contact',
        blank=True,
    )
    organisations = models.ManyToManyField(
        'accounts.Organisation',
        blank=True,
    )
    matter = models.ForeignKey(
        'billing.Matter',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    sender_name = models.CharField(max_length=256, null=True, blank=True)
    sender_address = models.EmailField(null=True, blank=True)
    recipient_name = models.CharField(max_length=256, null=True, blank=True)
    recipient_address = models.EmailField(null=True, blank=True)
    subject = models.CharField(max_length=512, null=True, blank=True)
    snippet = models.CharField(max_length=512, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    date = models.DateTimeField()
    gmail_message_id = models.CharField(max_length=256, null=True, blank=True)
    hidden = models.BooleanField(default=False)

    class Meta:
        ordering = ('-date', )

    def __str__(self):
        return "{} ({} - {})".format(
            self.subject,
            self.sender_address,
            self.recipient_address,
        )

    @property
    def available_matters(self):
        matter_filter = Q(client__contact__in=self.contacts.all()) | Q(client__organisation__in=self.organisations.all())

        search = re.search('\[(\d+)\]$', self.subject)

        if search:
            matter_id = search.group(1)
            matter_filter = matter_filter | Q(id=int(matter_id))

        return Matter.objects.filter(matter_filter)

class Attachment(models.Model):
    mail = models.ForeignKey(
        'gmailbox.Mail',
        related_name='attachments',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    data = models.ImageField(upload_to="attachments/", null=True, blank=True)
    name = models.CharField(max_length=512, null=True, blank=True)
    size = models.IntegerField()
    content_type = models.CharField(max_length=128, null=True, blank=True)
    inline = models.BooleanField(default=False)
