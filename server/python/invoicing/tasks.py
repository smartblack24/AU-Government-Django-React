import os
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import boto3
import pdfkit
from sitename import capp
from billing.models import DISBURSEMENT, FIXED_PRICE_ITEM, TIME_ENTRY
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger
from core.models import EmailMessage
from django.urls import reverse
from django.conf import settings
from django.template import Context, Template
from django.template.loader import render_to_string
from invoicing.models import Invoice

logger = get_task_logger('invoicing')


@capp.task(name='send_email')
def send_email(invoice_id, staff_member_email=None):
    invoice = Invoice.objects.get(id=invoice_id)
    invoice_id = invoice.id
    subject = 'Invoice No.{} from Andreyev Lawyers'.format(invoice.number)
    from_email = EmailMessage.objects.first().from_email
    to_email = invoice.matter.client.contact.email

    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = from_email
    message['To'] = to_email

    templ = Template(EmailMessage.objects.first().body)
    html_content = templ.render(Context({'invoice': invoice}))

    part = MIMEText(html_content, 'html')
    message.attach(part)

    status = invoice.status.name
    signature = True
    if status == 'Draft'or status == 'Waiting approval':
        signature = False

    data = {
        'invoice': invoice,
        'signature': signature,
        'total_disbursements':
            invoice.time_entries.filter(entry_type=2).cost(),
        'time_entries': invoice.time_entries.filter(
            entry_type=TIME_ENTRY).order_by('date'),
        'disbursements': invoice.time_entries.filter(
            entry_type=DISBURSEMENT),
        'fixed_price_items': invoice.time_entries.filter(
            entry_type=FIXED_PRICE_ITEM),

    }
    template = render_to_string('pdf/invoice.html', data)

    # local path to bootstrap.css
    css = os.path.join(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    ), 'static/bootstrap/css/bootstrap.css')

    site = settings.SITE_URL
    if 'sitename' in site:
        site = site + '/api'

    options = {
        'margin-top': '0.2in',
        'margin-right': '0.2in',
        'margin-bottom': '1.3in',
        'margin-left': '0.2in',
        'footer-html': '{}{}'.format(
            site, reverse('invoice_footer', args=[invoice_id]),
        ),
        'encoding': "UTF-8",
    }
    pdf = pdfkit.from_string(template, False, css=css, options=options)
    part = MIMEApplication(pdf)
    part.add_header(
        'Content-Disposition', 'attachment', filename='Invoice.pdf')
    message.attach(part)

    region = 'eu-west-1'
    key_id = settings.AWS_ID
    secret_key = settings.AWS_KEY
    client = boto3.client(
        service_name='ses',
        region_name=region,
        aws_access_key_id=key_id,
        aws_secret_access_key=secret_key,
    )

    response = client.send_raw_email(
        Source=message['From'],
        Destinations=[to_email, staff_member_email],
        RawMessage={
            'Data': message.as_string()
        }
    )
    print(response)


@periodic_task(
    name="update_invoice_payments",
    run_every=(crontab(minute=0, hour='*/12'))
)
def update_invoice_payments():
    invoices = Invoice.objects.filter(xero_invoice_id__isnull=False)

    for invoice in invoices:
        res = invoice.fetch_payments_from_xero()

        if res.get('success'):
            invoice.save()
            logger.info("Fetched invoice {} payments".format(invoice.id))
        else:
            logger.warning("Failed to fetch invoice {} payments".format(invoice.id))
