from core.models import LeadStatus
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Populated lead statuses'

    def handle(self, *args, **options):
        LeadStatus.objects.create(name="To be contacted")
        LeadStatus.objects.create(name="Nurturing")
        LeadStatus.objects.create(name="Quoting")
        LeadStatus.objects.create(name="Waiting for response")
