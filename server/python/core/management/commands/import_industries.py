import csv

from django.core.management.base import BaseCommand
from core.models import Industry


class Command(BaseCommand):
    help = 'Import branding theme IDs from Xero'

    def handle(self, *args, **options):
        with open('csv/core_industry.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    Industry.objects.create(
                        name=row.get('Name').strip(),
                        reference=row.get('Reference').strip()
                    )
                except:
                    print('Error')
                    print(row)
