from core.models import MatterStatus
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Populated invoice statuses'

    def handle(self, *args, **options):
        MATTER_STATUSES = ((1, 'Active - High (70+ units)'),
                           (2, 'Active - Moderate (30-70 units)'),
                           (3, 'Active - Low (0-30 units)'),
                           (4, 'Waiting for Internal review'),
                           (5, 'Waiting for AA review'),
                           (6, 'Waiting for external party to respond'),
                           (7, 'Ad hoc Work'),
                           (8, 'Need to be billed'), (9, 'Matter Closed'),
                           (10, 'Business Building'))

        for status in MATTER_STATUSES:
            MatterStatus.objects.create(name=status[1])
            print(status[1])
