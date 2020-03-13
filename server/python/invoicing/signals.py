from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from simple_history.utils import update_change_reason

from .models import Invoice, Payment


@receiver(post_save, sender=Payment)
def change_payment_handler(sender, instance, **kwargs):
    created = kwargs.get('created')
    instance.invoice.is_invoice_paid = instance.invoice.is_paid
    instance.invoice.save()
    instance.invoice.matter.save()

    if created:
        update_change_reason(instance, 'Payment was made')


@receiver(post_delete, sender=Payment)
def delete_payment_handler(sender, instance, **kwargs):
    instance.invoice.save()
    instance.invoice.is_invoice_paid = instance.invoice.is_paid
    instance.invoice.save()
    instance.invoice.matter.save()
    update_change_reason(instance.invoice, 'Payment was removed')


@receiver(post_save, sender=Payment)
def update_payments_handler(sender, instance, **kwargs):
    instance.invoice.save()
    instance.invoice.is_invoice_paid = instance.invoice.is_paid
    instance.invoice.save()
    instance.invoice.matter.save()


@receiver(post_save, sender=Invoice)
def change_invoice_handler(sender, instance, **kwargs):
    created = kwargs.get('created')
    last_history = instance.history.first()

    if created:
        update_change_reason(instance, 'Invoice was created')
    else:
        prev_history = last_history.get_previous_by_history_date()

        if (prev_history.history_object.status is not
                last_history.history_object.status):

            update_change_reason(
                instance,
                'Invoice changed status to {}'.format(
                    instance.status.name,
                )
            )
        else:
            update_change_reason(instance, 'Invoice edit')
