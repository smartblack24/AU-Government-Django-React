from datetime import datetime
from io import BytesIO

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template

import jwt
from dateutil.parser import parse
from graphql_relay.node.node import from_global_id
from xhtml2pdf import pisa

from xero.auth import PrivateCredentials
from xero import Xero

from integration.models import Xero as XeroIntegration

def obtain_jwt(user_id, forever=False):
    if forever:
        token = jwt.encode(
            {
                'user_id': user_id
            },
            settings.SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
    else:
        token = jwt.encode(
            {
                'exp': datetime.utcnow() + settings.JWT_EXPIRATION_DELTA,
                'user_id': user_id
            },
            settings.SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )

    return token.decode('utf-8')


def check_for_existence(*args):
    for arg in args:
        pk, model = arg

        try:
            # try to convert from global Relay id to Django model id
            pk = from_global_id(pk)[1]
        except Exception:
            pass

        try:
            model.objects.get(pk=pk)
        except model.DoesNotExist:
            raise Exception(
                "{} with the provided id does not exist".format(
                    model.__name__
                )
            )


def is_date(string):
    if len(str(string)) > 4:
        try:
            parse(string)
            return True
        except (ValueError, TypeError):
            return False

    return False


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def invoice_number(id):
    step1 = str(id)
    first_one = (int(step1[0])
                 + int(step1[2])
                 + 2 * int(step1[1]) // 10 + 2 * int(step1[1]) % 10
                 + 2 * int(step1[3]) // 10 + 2 * int(step1[3]) % 10)
    first_one %= 10
    if first_one == 0:
        return str(step1) + str(first_one)
    return str(step1) + str(10 - first_one)

def get_date_from_str(datestr, mode):
    try:
        day, month, year = datestr.split('/')
        if mode == 'start':
            return datetime(second=0, minute=0, hour=0, day=int(day), month=int(month), year=int(year))
        else:
            return datetime(second=59, minute=59, hour=23, day=int(day), month=int(month), year=int(year))
    except:
        return None

def get_xero_client():
    xeroIntegration = XeroIntegration.objects.first()
    consumer_key = xeroIntegration.consumer_key
    rsa_key = xeroIntegration.rsa_key

    credentials = PrivateCredentials(consumer_key, rsa_key)
    xero = Xero(credentials)
    return xero
