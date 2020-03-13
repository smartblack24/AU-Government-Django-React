from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

from .models import Matter, TimeEntry


@receiver(pre_delete, sender=Matter)
def handle_matter_delete(sender, instance, **kwargs):
    if instance.time_entries.exists():
        raise Exception(
            'The Matter cannot be deleted because it has a recorded time'
        )


@receiver(post_save, sender=TimeEntry)
def handle_time_entry_edit(sender, instance, **kwargs):
    if instance.invoice is not None:
        instance.invoice.save()
