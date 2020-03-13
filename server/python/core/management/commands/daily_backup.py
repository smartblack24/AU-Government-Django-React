import datetime

import boto3
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Make daily backup and upload to S3 bucket'

    def handle(self, *args, **options):
        now = datetime.datetime.now()
        file_name = '{}.sql'.format(
            now.strftime("%d-%m-%Y")
        )
        data = open('/app/{}'.format(file_name), 'rb')
        client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ID,
            aws_secret_access_key=settings.AWS_KEY,
        )
        res = client.put_object(
            Bucket='sitename-backups',
            Key=file_name,
            Body=data
            )
        file_log = open('backup_log.log', 'a')
        file_log.write(str(res) + '\n')
        file_log.close()
