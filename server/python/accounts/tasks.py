import boto3
from accounts.models import User, Client, Contact, Organisation
from sitename import capp
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from celery.utils.log import get_task_logger
from gmailbox.models import Mail
from gmailbox.utils import get_user_mails, get_domain
# from django.core.mail import send_mail

logger = get_task_logger('accounts')

@capp.task(name='reset_password_email')
def reset_password_email(email):
    subject = "sitename: reset password"
    from_email = "accounts@andreyev.com.au"
    to = [email]
    # get user by email
    user = User.objects.get(email=email)
    # generate token
    token = default_token_generator.make_token(user)

    body = "Click here to reset your password: {site_url}/reset-password/{user_id}/{token}".format(
        site_url=settings.SITE_URL, user_id=user.id, token=token)
    print(body)
    # send_mail(subject, body, from_email, to)
    region = 'eu-west-1'
    key_id = settings.AWS_ID
    secret_key = settings.AWS_KEY
    client = boto3.client(
        service_name='ses',
        region_name=region,
        aws_access_key_id=key_id,
        aws_secret_access_key=secret_key,
        )
    response = client.send_email(
        Source=from_email,
        Destination={
            'ToAddresses': to,
        },
        Message={
            'Body': {
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': body,
                }
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': subject
            }
        }
    )
    print(response)


@capp.task(name='update_xero_contact')
def update_xero_contact(client_id):
    client = Client.objects.filter(id=client_id).first()

    if client:
        res = client.create_or_update_xero_contact(force_update=True)

        if res.get('success'):
            logger.info("Updated contact for client {}".format(client_id))
        else:
            logger.warning("Failed to update contact for client {}".format(client_id))

@capp.task(name='create_all_contacts_in_xero')
def create_all_contacts_in_xero():
    clients = Client.objects.filter(xero_contact_id__isnull=True)

    for client in clients:
        res = client.create_or_update_xero_contact()

        if res.get('success'):
            logger.info("Created contact for client {}".format(client.id))
        else:
            logger.warning("Failed to create contact for client {}".format(client.id))

@capp.task(name='get_user_mails_task')
def get_user_mails_task(user_id):
    user = User.objects.get(id=user_id)
    get_user_mails(user)
