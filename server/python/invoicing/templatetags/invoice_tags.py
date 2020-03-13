from decimal import Decimal

from django import template

register = template.Library()


@register.filter(name='value_incl_gst')
def value_incl_gst(invoice):
    return invoice.value(gst=True)


@register.filter(name='gst_amount')
def gst_amount(invoice):
    return invoice.value(gst=True) - invoice.value(gst=False)


@register.filter(name='two_places')
def two_places(number):
    TWOPLACES = Decimal(10) ** -2
    if type(number) is Decimal:
        return number.quantize(TWOPLACES)

    return number
