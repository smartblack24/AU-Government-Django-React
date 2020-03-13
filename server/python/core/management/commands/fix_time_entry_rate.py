import sys
from decimal import Decimal
from datetime import date

from billing.models import TimeEntry
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Populate rate to all time entries with empty rate'

    def handle(self, *args, **options):
        time_entries = TimeEntry.objects.filter(
            date__range=[
                date(day=18, month=6, year=2018),
                TimeEntry.objects.all().order_by('-date').first().date
            ]).filter(entry_type=1)
        for index, time_entry in enumerate(time_entries, 1):
            if time_entry.rate is None:
                user_rate = time_entry.staff_member.rate
                time_entry.rate = Decimal(user_rate)
                time_entry.save()
            sys.stdout.write('{}/{} \r'.format(
                index,
                time_entries.count())
                )
