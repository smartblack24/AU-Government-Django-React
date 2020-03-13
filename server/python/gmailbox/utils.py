import base64
import email
import httplib2
import json
import oauth2client
import os
import pprint
import pytz
import re
import uuid
import zipfile

from accounts.models import Contact, Organisation
from apiclient import errors
from apiclient.discovery import build
from billing.models import Matter
from datetime import datetime
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.db.models import Q
from email.header import decode_header
from email.utils import getaddresses, mktime_tz, parseaddr, parsedate_tz
from integration.models import Gmail

from .models import Mail, Attachment, GmailAccount


def paragraphs(value):
    """
    Turns paragraphs delineated with newline characters into
    paragraphs wrapped in <div> and </div> HTML tags.
    """
    paras = re.split(r'[\r\n]+', value)
    paras = ['<div>%s</div>' % p.strip() for p in paras]
    return ''.join(paras)

def get_subject(msg):
    try:
        subject = None
        if msg.get('subject') is not None:
            decode_fragments = decode_header(msg.get('subject'))

            subject_fragments = []
            for sub, encoding in decode_fragments:
                if encoding:
                    sub = sub.decode(encoding)
                subject_fragments.append(sub)
            subject = ''.join(subject_fragments)

        return subject.replace('\r', '').replace('\n', '')
    except Exception as e:
        print('parse_subject: {}'.format(str(e)))
        return None

def get_content(msg):
    text_body = None
    html_body = None
    content = None

    for part in msg.walk():
        try:
            content_type = part.get_content_type()
            content_disposition = part.get('Content-Disposition', None)

            if not content_disposition:
                if content_type == "text/plain":
                    if text_body is None:
                        text_body = ""
                    text_body += part.get_payload(decode=True).decode('utf-8')
                    text_body = text_body.replace('\r\n', '<br/>')
                elif content_type == "text/html":
                    if html_body is None:
                        html_body = ""
                    html_body += part.get_payload(decode=True).decode('utf-8')
        except Exception as e:
            print('parse_message: {}'.format(str(e)))
            pass

    content = html_body if html_body else text_body
    return content


def get_attachments(msg):
    origins = []
    inlines = []

    for part in msg.walk():
        try:
            name = part.get_filename()
            cid = part.get('Content-ID')
            ctype = part.get_content_type()
            data = part.get_payload(decode=True)
            cdis = part.get('Content-Disposition')

            if data:                
                if cdis and 'attachment' in cdis:
                    origins.append({
                        'name': name,
                        'ctype': ctype,
                        'data': data,
                        'size': len(data),
                    })
                elif cid and 'image' in ctype:
                    inlines.append({
                        'name': name,
                        'cid': re.sub('[<>]', '', cid),
                        'ctype': ctype,
                        'data': data,
                        'size': len(data),
                    })

        except Exception as e:
            print('get_attachments: {}'.format(str(e)))
            pass

    return {
        'origins': origins,
        'inlines': inlines,
    }

def get_gmail_service(token_data):
    gmail_config = Gmail.objects.first()

    if not gmail_config:
        return None

    try:
        client_id = gmail_config.client_id
        client_secret = gmail_config.client_secret
        token_uri = 'https://www.googleapis.com/oauth2/v4/token'

        data = json.loads(token_data)

        cred = oauth2client.client.GoogleCredentials(data['access_token'], client_id, client_secret, data['refresh_token'], 3600, token_uri, '')
        service = build(serviceName='gmail', version='v1', http=cred.authorize(httplib2.Http()))

        return service
    except Exception as e:
        print('get_gmail_service: {}'.format(str(e)))
        return None


def get_domain(address):
    search = re.search('@(.+)', address)
    return search.group(1) if search else None


def get_contacts(sender, recipient):
    sender_name, sender_address = sender
    recipient_name, recipient_address = recipient

    filter_param = None

    if sender_address and sender_address != '':
        filter_param = Q(email=sender_address) | Q(secondary_email=sender_address)

    if recipient_address and recipient_address != '':
        filter_param |= Q(email=recipient_address) | Q(secondary_email=recipient_address)

    contacts = Contact.objects.filter(filter_param)

    return contacts


def get_matter(subject):
    search = re.search('\[(\d+)\]$', subject)
    if not search:
        return None

    matter_id = search.group(1)

    try:
        matter = Matter.objects.get(pk=int(matter_id))
        return matter
    except ObjectDoesNotExist:
        return None

def is_hidden_mail(subject):
    search = re.search('\[(\d+)\]$', subject)
    if not search:
        return False

    matter_id = search.group(1)
    return matter_id == '0000'


def get_organisations(sender, recipient):
    sender_name, sender_address = sender
    recipient_name, recipient_address = recipient
    sender_domain = get_domain(sender_address)
    recipient_domain = get_domain(recipient_address)

    filter_param = None

    if sender_domain:
        filter_param = Q(website__endswith=sender_domain)

    if recipient_domain:
        filter_param |= Q(website__endswith=recipient_domain)

    organisations = Organisation.objects.filter(filter_param)

    return organisations


def get_user_mails(user):
    if not hasattr(user, 'gmail_account') or not user.gmail_account.token:
        return {'success': False, 'error': "User gmail is not activated"}

    service = get_gmail_service(user.gmail_account.token)

    if not service:
        return {'success': False, 'error': "User gmail is not valid"}

    try:
        latest_mail_date = user.gmail_account.latest_mail_date
        query = '-label:SPAM -label:DRAFT'

        if latest_mail_date:
            query += ' after: {}'.format(latest_mail_date.strftime("%Y/%m/%d"))

        response = service.users().messages().list(userId='me', q=query).execute()

        if 'messages' in response:
            handle_messages(response['messages'], service)

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = service.users().messages().list(userId='me', pageToken=page_token).execute()
                if 'messages' in response:
                    handle_messages(response['messages'], service)

        return {'success': True}
    except Exception as e:
        print('Failed to get_user_mails for {}: {}'.format(user.full_name, str(e)))
        return {'success': False}

def handle_messages(messages, service):
    try:
        for message in messages[::-1]:
            res = service.users().messages().get(userId='me', id=message['id'], format='raw').execute()
            msg = email.message_from_bytes(base64.urlsafe_b64decode(res['raw'].encode('ASCII')))

            subject = get_subject(msg)
            snippet = res.get('snippet')
            sender = parse_special_addr(msg)
            tos = msg.get_all('to', [])
            ccs = msg.get_all('cc', [])
            recipients = getaddresses(tos + ccs)
            date = datetime.fromtimestamp(mktime_tz(parsedate_tz(msg.get('date'))), pytz.timezone(settings.TIME_ZONE))
            content = get_content(msg)
            attachments = get_attachments(msg)

            if content:
                for recipient in recipients:
                    insert_mail(sender, recipient, date, subject, snippet, content, message['id'], attachments)
    except Exception as e:
        print('handle_messages: {}'.format(str(e)))
        pass

def parse_special_addr(msg):
    sender = parseaddr(msg.get('from'))
    sender_name, sender_addr = sender
    sender_name = decode_header(sender_name)
    name, encoding = sender_name[0]

    if encoding:
        name = name.decode(encoding)

    return name, sender_addr


def insert_mail(sender, recipient, date, subject, snippet, content, message_id, attachments):
    try:
        sender_name, sender_address = sender
        recipient_name, recipient_address = recipient
        sender_domain = get_domain(sender_address)
        recipient_domain = get_domain(recipient_address)

        if not sender_address or sender_address == '' or not recipient_address or recipient_address == '' or not sender_domain or not recipient_domain:
            return

        contacts = get_contacts(sender, recipient)
        organisations = get_organisations(sender, recipient)
        matter = get_matter(subject)
        hidden = is_hidden_mail(subject)

        mail_data = {
            'sender_name': sender_name,
            'sender_address': sender_address,
            'recipient_name': recipient_name,
            'recipient_address': recipient_address,
            'subject': subject,
            'snippet': snippet,
            'content': content,
            'date': date,
            'matter': matter,
            'gmail_message_id': message_id,
            'hidden': hidden,
        }

        exists = Mail.objects.filter(gmail_message_id=message_id, recipient_address=recipient_address).exists()

        if not exists:
            mail = Mail.objects.create(**mail_data)

            if contacts.exists():
                mail.contacts.set(contacts)

            if organisations.exists():
                mail.organisations.set(organisations)

            if attachments:
                origins = attachments.get('origins')
                inlines = attachments.get('inlines')

                if origins:                
                    for origin in origins:
                        ext = origin.get('name').split('.')[-1]
                        filename = '%s.%s' % (uuid.uuid4(), ext)
                        data = ContentFile(origin.get('data'), name=filename)
                        Attachment.objects.create(
                            mail=mail,
                            name=origin.get('name'),
                            size=origin.get('size'),
                            content_type=origin.get('content_type'),
                            data=data,
                        )

                if inlines:
                    content = mail.content

                    for inline in inlines:
                        content_id = inline.get('content_id')
                        ext = inline.get('name').split('.')[-1]
                        filename = '{}.{}'.format(uuid.uuid4(), ext)
                        data = ContentFile(inline.get('data'), name=filename)
                        attachment = Attachment.objects.create(
                            mail=mail,
                            name=inline.get('name'),
                            size=inline.get('size'),
                            content_type=inline.get('content_type'),
                            data=data,
                            inline=True,
                        )

                        cid = 'cid:%s' % content_id
                        abs_url = '%s%s' % (settings.API_URL, attachment.data.url)
                        content = content.replace(cid, abs_url)

                    mail.content = content
                    mail.save()
                    

    except Exception as e:
        print('insert_mail: {}'.format(str(e)))
        pass

def zip_folder(folder_path, output_path):
    parent_folder = os.path.dirname(folder_path)
    contents = os.walk(folder_path)

    try:
        zip_file = zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED)
        for root, folders, files in contents:
            for folder_name in folders:
                absolute_path = os.path.join(root, folder_name)
                relative_path = absolute_path.replace(parent_folder + '\\','')
                zip_file.write(absolute_path, relative_path)
            for file_name in files:
                absolute_path = os.path.join(root, file_name)
                relative_path = absolute_path.replace(parent_folder + '\\','')
                zip_file.write(absolute_path, relative_path)
        zip_file.close()
    except:
        zip_file.close()
        pass

def get_mail_filename(data, single=False):
    subject = data.get('subject')
    sender = data.get('sender')
    date = data.get('date').strftime('%Y%d%m')
    matter = data.get('matter')
    id = data.get('id')

    filename = None

    if matter:
        filename = '{}_Email from {}_{}_{}_(ID {}).pdf'.format(date, sender, subject, matter, id)
    else:
        filename = '{}_Email from {}_{}_(ID {}).pdf'.format(date, sender, subject, id)

    if single:
        return filename

    return filename.replace('/', '\u2215')


def get_mail_data(mail):
    attachments = mail.attachments.filter(inline=False)
    content = re.sub('src=[\"\']cid:.+[\"\']', 'src=""', mail.content)

    return {
        'id': mail.id,
        'subject': mail.subject,
        'date': mail.date,
        'sender': mail.sender_name if mail.sender_name else mail.sender_address,
        'recipient': mail.recipient_name if mail.recipient_name else mail.recipient_address,
        'matter': mail.matter.name if mail.matter else None,
        'content': content,
        'attachments': [attachment.name for attachment in attachments] if attachments.count() > 0 else None,
    }
