from datetime import datetime
from django.core.management.base import BaseCommand
from billing.models import TimeEntry


class Command(BaseCommand):
    help = 'Fix main_line field'

    def handle(self, *args, **options):
        for time_entry in TimeEntry.objects.all():
            time_entry.date = datetime.combine(
                time_entry.date,
                datetime.strptime('10:00', '%H:%M').time()
                )
            time_entry.save()
