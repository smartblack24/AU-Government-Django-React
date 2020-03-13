import re

from django.db.models import Q
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from .models import Client, Contact, Organisation

from gmailbox.models import Mail


@receiver(pre_delete, sender=Contact)
def pre_delete_contact(sender, instance, **kwargs):
    if instance.clients.count():
        raise Exception(
            "The Contact cannot be deleted because it has a relation to a \
            Client"
        )
    elif instance.referrers.count():
        raise Exception(
            "The Contact cannot be deleted because it is the referrer for \
            someone"
        )


@receiver(pre_save, sender=Contact)
def pre_save_contact(sender, instance, **kwargs):
    if instance.pk:
        try:
            pre_instance = sender.objects.get(pk=instance.pk)

            if pre_instance.email == instance.email:
                return

            if instance.email:
                pre_instance.mail_set.clear()
                mails = Mail.objects.filter(Q(sender_address=instance.email) | Q(recipient_address=instance.email))
                pre_instance.mail_set.set(mails)
        except:
            pass


@receiver(pre_delete, sender=Organisation)
def pre_delete_organisation(sender, instance, **kwargs):
    if len(instance.clients.all()):
        raise Exception(
            "The Organisation cannot be deleted because it has a relation to a Client"
        )


@receiver(pre_save, sender=Organisation)
def pre_save_organisation(sender, instance, **kwargs):
    def get_domain(website):
        domain = website
        for seg in ['^http://', '^https://', '^www.']:
            domain = re.sub(seg, '', domain)
        return domain

    if instance.pk:
        try:
            pre_instance = sender.objects.get(pk=instance.pk)

            if pre_instance.website == instance.website:
                return

            pre_instance.mail_set.clear()
            if instance.website:
                domain = get_domain(instance.website)
                mails = Mail.objects.filter(Q(sender_address__contains=domain) | Q(recipient_address__contains=domain))
                pre_instance.mail_set.set(mails)
        except:
            pass


@receiver(pre_delete, sender=Client)
def pre_delete_client(sender, instance, **kwargs):
    if instance.matters.count():
        raise Exception(
            "The Client cannot be deleted because it has a Matter assigned to")

    if instance.contact:
        instance.contact.organisations.remove(instance.organisation)
