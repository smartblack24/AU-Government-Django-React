from core.models import TimeEntryType
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Populated lead statuses'

    def handle(self, *args, **options):
        TimeEntryType.objects.create(name="Matter")
        TimeEntryType.objects.create(name="Sales")
