import sys

from accounts.models import User
from billing.models import Matter
from core.models import MatterStatus
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Edit matters with wrong data'

    def handle(self, *args, **options):
        matters = Matter.objects.all()
        admin_user = User.objects.get(email="admin@andreyev.com.au")
        andrew_user = User.objects.get(email="andrew@andreyev.com.au")
        for index, matter in enumerate(matters, 1):
            # Change matter status to closed if billable status is closed
            if matter.billable_status == 3:
                matter.matter_status = MatterStatus.objects.get(id=9)
            # Change manager to Admin if Principal and Matter Manager is Andrew
            if matter.principal_id == andrew_user.id and \
               matter.manager_id == andrew_user.id:
                matter.manager = admin_user
            # Principal and Matter Manager is the same person
            # change Principal to Andrew Andreyev
            if matter.manager_id == matter.principal_id:
                matter.principal = andrew_user
            # Change standard terms to date matter created
            # if matter standard terms is empty
            if not matter.is_standard_terms_sent:
                matter.is_standard_terms_sent = True
                if not matter.standard_terms_sent:
                    matter.standard_terms_sent = matter.created_date
            elif matter.is_standard_terms_sent:
                if not matter.standard_terms_sent:
                    matter.standard_terms_sent = matter.created_date
            matter.save()
            sys.stdout.write('{}/{} \r'.format(index, matters.count()))
