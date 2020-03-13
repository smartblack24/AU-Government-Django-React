import csv

from django.core.management.base import BaseCommand
from accounts.models import Organisation


class Command(BaseCommand):
    help = 'Fix main_line field'

    def handle(self, *args, **options):

        with open('csv/organisations.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                number = row['Org Main Phone']
                id = row['id']
                try:
                    organisation = Organisation.objects.get(id=id)
                    organisation.main_line = number
                    organisation.save()
                except Organisation.DoesNotExist:
                    print(id)
