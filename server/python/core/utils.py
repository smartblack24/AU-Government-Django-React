from base64 import b64decode, b64encode

from django.conf import settings


def decode_cursor(cursor):
    if cursor:
        try:
            querystring = b64decode(cursor).decode()
            offset_start, offset_end = querystring.split(':')
            offset_start, offset_end = int(offset_start), int(offset_end)
        except Exception:
            raise ValueError("Invalid Cursor".split())
    else:
        offset_start, offset_end = 0, settings.EMAILS_PER_PAGE
    return offset_start, offset_end


def encode_cursor(offset_start, offset_end):
    querystring = '{}:{}'.format(offset_start, offset_end)
    return b64encode(querystring.encode()).decode()


def get_paginator(queryset, cursor, paginated_type, **kwargs):
    offset_start, offset_end = decode_cursor(cursor)
    objects = queryset[offset_start:offset_end]
    prev_cursor = next_cursor = first_cursor = last_cursor = None

    if queryset[:offset_start]:
        prev_offset_start = offset_start - settings.EMAILS_PER_PAGE
        prev_offset_end = offset_start
        if prev_offset_start < 0:
            prev_offset_start, prev_offset_end = 0, settings.EMAILS_PER_PAGE
        prev_cursor = encode_cursor(prev_offset_start, prev_offset_end)

    if queryset[offset_end:]:
        next_offset_start = offset_end
        next_offset_end = offset_end + settings.EMAILS_PER_PAGE
        next_cursor = encode_cursor(next_offset_start, next_offset_end)

    len_queryset = len(queryset)
    if len_queryset > settings.EMAILS_PER_PAGE:
        first_cursor = encode_cursor(0, settings.EMAILS_PER_PAGE)
        last_offset_start = len_queryset - len_queryset % settings.EMAILS_PER_PAGE
        last_offset_end = len_queryset
        last_cursor = encode_cursor(last_offset_start, last_offset_end)

    try:
        email_id = objects.first().id
    except AttributeError:
        email_id = 1

    return paginated_type(
        id=email_id,  # keep unique for normalizing by Apollo Client
        prev_cursor=prev_cursor,
        next_cursor=next_cursor,
        first_cursor=first_cursor,
        last_cursor=last_cursor,
        objects=objects,
        **kwargs
    )
