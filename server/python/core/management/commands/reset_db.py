from accounts.models import Client, Contact, Location, Organisation, User
from billing.models import Matter, Note, TimeEntry
from core.models import Document, InvoiceStatus, MatterType, Office, Section
from django.core.management.base import BaseCommand
from invoicing.models import Invoice, Payment, PaymentTerms


class Command(BaseCommand):
    help = 'Remove objects from db'

    def add_arguments(self, parser):
        parser.add_argument('model', type=str)

    def handle(self, *args, **options):
        model = options['model']

        if model == 'all':
            for contact in Contact.objects.all():
                contact.referrer = None
                contact.occupation = None
                contact.save()

            Location.objects.all().delete()
            Section.objects.all().delete()
            User.objects.all().delete()
            TimeEntry.objects.all().delete()
            Location.objects.all().delete()
            MatterType.objects.all().delete()
            Matter.objects.all().delete()
            Client.objects.all().delete()
            Contact.objects.all().delete()
            Organisation.objects.all().delete()
            Invoice.objects.all().delete()
            Payment.objects.all().delete()
            PaymentTerms.objects.all().delete()
            Office.objects.all().delete()
            InvoiceStatus.objects.all().delete()
            Document.objects.all().delete()

        elif model == 'users':
            User.objects.all().delete()
        elif model == 'matters':
            Matter.objects.all().delete()
            MatterType.objects.all().delete()
        elif model == 'clients':
            Client.objects.all().delete()
        elif model == 'invoices':
            Invoice.objects.all().delete()
        elif model == 'time-entries':
            TimeEntry.objects.all().delete()
        elif model == 'payments':
            Payment.objects.all().delete()
        elif model == 'matter_notes':
            Note.objects.all().delete()
        elif model == 'safe_storage':
            Document.objects.all().delete()
            Section.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS('Successfully reset the db')
        )
