import base64
import json
import os
import shutil
import uuid
import pdfkit
import zipfile

from django.http import HttpResponse, FileResponse
from django.template.loader import render_to_string
from django.views.generic import View
from graphql_relay.node.node import from_global_id
from html import unescape, escape

from .models import Mail
from .utils import zip_folder, get_mail_filename, get_mail_data


class MailView(View):
    def get(self, request, *args, **kwargs):
        try:
            mail_id = from_global_id(kwargs.get('mail_id'))[1]
            mail = Mail.objects.get(pk=mail_id)

            html = mail.content

            return HttpResponse(html)
        except Exception as e:
            return HttpResponse('')


class MailExportView(View):
    def get(self, request, *args, **kwargs):
        options = {
            'encoding': 'utf-8',
        }
        try:
            mail_ids = kwargs.get('mail_ids')

            mails = []
            for m_id in mail_ids.split(','):
                m_id = from_global_id(m_id)[1]
                mails.append(Mail.objects.get(pk=m_id))

            mail_count = len(mails)

            if mail_count == 0:
                return HttpResponse('')
            elif mail_count == 1:
                mail = mails[0]
                data = get_mail_data(mail)
                mail_content = render_to_string('pdf/mail.html', data)

                tmp_filename = 'media/{}.pdf'.format(uuid.uuid4().hex)
                pdfkit.from_string(unescape(mail_content), tmp_filename, options=options)

                file_data = None
                with open(tmp_filename, 'rb') as f:
                    file_data = f.read()

                filename = get_mail_filename(data, single=True)
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
                response.write(file_data)

                os.remove(tmp_filename)

                return response
            else:
                tmp_folder = uuid.uuid4().hex
                os.makedirs('/mails/{}'.format(tmp_folder), exist_ok=True)

                for mail in mails:
                    data = get_mail_data(mail)
                    mail_content = render_to_string('pdf/mail.html', data)
                    filename = '/mails/{}/{}'.format(tmp_folder, get_mail_filename(data))
                    pdfkit.from_string(unescape(mail_content), filename, options=options)

                zip_filename = '/mails/mails.zip'

                zip_folder('/mails/{}/'.format(tmp_folder), zip_filename)

                zip_data = None

                with open(zip_filename, 'rb') as f:
                    zip_data = f.read()

                response = HttpResponse(content_type='application/zip')
                response['Content-Disposition'] = 'attachment; filename="mails.zip"'
                response.write(zip_data)

                shutil.rmtree('/mails')

                return response
        except Exception as e:
            print(str(e))
            return HttpResponse('')
