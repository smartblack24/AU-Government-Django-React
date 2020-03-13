import sys

from billing.models import Matter
from core.models import LeadStatus
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Populate lead status to existing  matters'

    def handle(self, *args, **options):
        matters = Matter.objects.all()
        all = Matter.objects.count()
        for index, matter in enumerate(matters, 1):
            if matter.entry_type_id == 1:
                matter.lead_status = LeadStatus.objects.get(name="Won")
                matter.save()
            sys.stdout.write("{}/{} \r".format(index, all))
