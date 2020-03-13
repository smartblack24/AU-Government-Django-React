import os
from datetime import datetime

import pdfkit
from accounts.models import User
from billing.models import DISBURSEMENT, FIXED_PRICE_ITEM, TIME_ENTRY
from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import View
from graphql_relay.node.node import from_global_id
from invoicing.models import Invoice


def invoice_footer(request, invoice_id):
    invoice = Invoice.objects.get(pk=invoice_id)
    return render(request, 'pdf/invoice_footer.html', {'invoice': invoice})


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        invoice_id = from_global_id(kwargs.get('invoice_id'))[1]

        invoice = Invoice.objects.get(pk=invoice_id)

        status = invoice.status.name
        signature = True
        if status == 'Draft'or status == 'Waiting approval':
            signature = False

        data = {
            'invoice': invoice,
            'signature': signature,
            'total_disbursements': invoice.time_entries.filter(
                entry_type=2).cost(),
            'time_entries': invoice.time_entries.filter(
                entry_type=TIME_ENTRY).filter(status=1).order_by('date'),
            'disbursements': invoice.time_entries.filter(
                entry_type=DISBURSEMENT),
            'fixed_price_items': invoice.time_entries.filter(
                entry_type=FIXED_PRICE_ITEM),

        }
        template = render_to_string('pdf/invoice.html', data)
        site = settings.SITE_URL
        if 'sitename' in site:
            site = site + '/api'

        # local path to bootstrap.css
        css = os.path.join(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        ), 'static/bootstrap/css/bootstrap.css')
        options = {
            'margin-top': '0.2in',
            'margin-right': '0.2in',
            'margin-bottom': '1.3in',
            'margin-left': '0.2in',
            'footer-html': '{}{}'.format(
                site, reverse('invoice_footer', args=[invoice_id])
            ),
            # 'footer-html':
            #     '{}/pdf/invoice_footer/{}/'.format(site, invoice_id),
            'encoding': "UTF-8",
        }
        pdf = pdfkit.from_string(template, False, css=css, options=options)
        return HttpResponse(pdf, content_type='application/pdf')


class GenerateReminder(View):
    def get(self, request, *args, **kwargs):
        invoice_id = from_global_id(kwargs.get('invoice_id'))[1]
        reminder = kwargs.get('reminder')
        user_id = from_global_id(kwargs.get('user_id'))[1]
        user = get_object_or_404(User, pk=user_id)
        invoice = get_object_or_404(Invoice, pk=invoice_id)
        data = {
            'type': reminder,
            'staff': request.user,
            'invoice': invoice,
            'time_entries': invoice.time_entries.filter(
                entry_type=TIME_ENTRY),
            'disbursements': invoice.time_entries.filter(
                entry_type=DISBURSEMENT),
            'fixed_price_items': invoice.time_entries.filter(
                entry_type=FIXED_PRICE_ITEM),
            'date': datetime.now(),
            'user': user
        }
        template = None
        friendly_reminder = 'pdf/invoice_friendly_reminder.html'
        first_reminder = 'pdf/invoice_1st_reminder.html'
        second_reminder = 'pdf/invoice_2nd_reminder.html'

        # local path to bootstrap.css
        css = os.path.join(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        ), 'static/bootstrap/css/bootstrap.css')

        if reminder == 'friendly':
            template = render_to_string(friendly_reminder, data)
        elif reminder == 'first':
            template = render_to_string(first_reminder, data)
        elif reminder == 'second':
            template = render_to_string(second_reminder, data)

        options = {
            'margin-top': '0.7in',
            'margin-right': '0.2in',
            'margin-bottom': '0.5in',
            'margin-left': '0.2in',
        }

        try:
            pdf = pdfkit.from_string(template, False, css=css, options=options)
        except TypeError:
            raise Http404('Reminder type does not exist')

        return HttpResponse(pdf, content_type='application/pdf')
