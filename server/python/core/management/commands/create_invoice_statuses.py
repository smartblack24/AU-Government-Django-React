import csv

from core.models import InvoiceStatus
from django.core.management.base import BaseCommand
from invoicing.models import Invoice


class Command(BaseCommand):
    help = 'Populated invoice statuses'

    def handle(self, *args, **options):
        INVOICE_STATUSES = (
            (1, 'In Xero'), (2, 'Printed'),
            (3, 'Approved'), (4, 'Waiting approval'),
            (5, 'Draft')
        )

        def handle_invoice_status(status):
            for inv_stat in INVOICE_STATUSES:
                invoice_status, is_created = InvoiceStatus.objects.get_or_create(
                    name=inv_stat[1]
                )
                if inv_stat[1] == status:
                    return invoice_status
            return None

        with open('csv/invoices.csv', newline='', encoding="ISO-8859-1") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    invoice = Invoice.objects.get(id=row['id'])
                    invoice.status = handle_invoice_status(
                        row['Invoice Status']
                    )
                    invoice.save()
                except:
                    pass
