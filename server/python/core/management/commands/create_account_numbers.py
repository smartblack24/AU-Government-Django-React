from core.models import (
  AccountNumber,
  TIME_ENTRY, DISBURSEMENT, FIXED_PRICE_ITEM,
  GST, GST_EXPORT, BAS_EXCLUDED,
)
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Populated account numbers'

    def handle(self, *args, **options):
        AccountNumber.objects.create(entry_type=TIME_ENTRY, gst_status=GST, account_number=200)
        AccountNumber.objects.create(entry_type=TIME_ENTRY, gst_status=GST_EXPORT, account_number=200)
        AccountNumber.objects.create(entry_type=TIME_ENTRY, gst_status=BAS_EXCLUDED, account_number=200)
        AccountNumber.objects.create(entry_type=DISBURSEMENT, gst_status=GST, account_number=261)
        AccountNumber.objects.create(entry_type=DISBURSEMENT, gst_status=GST_EXPORT, account_number=262)
        AccountNumber.objects.create(entry_type=DISBURSEMENT, gst_status=BAS_EXCLUDED, account_number=260)
        AccountNumber.objects.create(entry_type=FIXED_PRICE_ITEM, gst_status=GST, account_number=200)
        AccountNumber.objects.create(entry_type=FIXED_PRICE_ITEM, gst_status=GST_EXPORT, account_number=200)
        AccountNumber.objects.create(entry_type=FIXED_PRICE_ITEM, gst_status=BAS_EXCLUDED, account_number=200)
