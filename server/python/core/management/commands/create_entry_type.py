from billing.models import EntryType
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Populated lead statuses'

    def handle(self, *args, **options):
        EntryType.objects.create(name="Matter")
        EntryType.objects.create(name="Sales")
