import csv

from core.models import InvoiceStatus
from django.core.management.base import BaseCommand
from core.models import Office

class Command(BaseCommand):
    help = 'Import branding theme IDs from Xero'

    def handle(self, *args, **options):
        offices = Office.objects.filter(xero_branding_theme_id__isnull=True)
    
        for office in offices:
            success = office.get_branding_theme_id_from_xero()
            if success:
                print('Imported branding theme for office {}'.format(office))

        print('Importing branding themes from xero done')
