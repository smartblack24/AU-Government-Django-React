from sitename.utils import get_xero_client

def format_address(location):
    print('ad1 ', location.address1, 'ad2 ', location.address2, 'suburb ', location.suburb, 'state ', location.get_state_display(), 'co_post ', location.post_code, location.country)
    if location.country == 'Australia':
        if location.post_code is None:
            country_and_post_code = ''
        if location.post_code == '0':
            country_and_post_code = ''
        else:
            if location.post_code == '':
                country_and_post_code = ''
            else:
                country_and_post_code = '{}'.format(
                    location.post_code or '')
    else:
        country = location.country
        post_code = location.post_code
        if location.country == '0':
            country = ''
        if location.country is None:
            country = ''
        if location.post_code == '0':
            post_code = ''
        if location.post_code is None:
            post_code = ''
        country_and_post_code = '{} {}'.format(
            country,
            post_code
        )
    if location.get_state_display() == 0:
        state_display = ''
    elif location.get_state_display() is None:
        state_display = ''
    else:
        state_display = location.get_state_display()
    if location.address2 == '':
        address2 = ''
    elif location.address2 is None:
        address2 = ''
    else:
        address2 = '{}\n'.format(location.address2)
    suburb = location.suburb
    if location.suburb is None:
        suburb = ''
    if location.suburb == '0':
        suburb = ''
    print('ad1 ', location.address1, 'ad2 ', address2, 'suburb ', suburb, 'state ', state_display, 'co_post ', country_and_post_code)
    return "{}\n{}{} {} {}".format(
        location.address1 or '',
        address2,
        suburb or '',
        state_display or '',
        country_and_post_code
    )

    return None

def prepare_xero_contact_param(client):
    postal_location = client.organisation.postal_location if client.organisation else client.contact.postal_location
    contact = client.contact

    if not postal_location:
        return {'valid': False, 'error': 'Contact: Empty postal location'}

    if not postal_location.address1:
        return {'valid': False, 'error': 'Contact: Empty primary address in postal location'}

    xero_contact_data = {
        'FirstName': contact.first_name,
        'LastName': contact.last_name,
        'Name': client.name,
        'EmailAddress': contact.email,
        'Addresses': [
            {
                'AddressType': 'POBOX',
                'AddressLine1': postal_location.address1,
                'AddressLine2': postal_location.address2 or '',
                'City': postal_location.suburb or '',
                'Region': postal_location.get_state_display() if postal_location.state else '',
                'PostalCode': postal_location.post_code or '',
                'Country': postal_location.country or '',
            }
        ]
    }

    return {'valid': True, 'data': xero_contact_data}

def check_contact_in_xero(client):
    xero = get_xero_client()
    res = xero.contacts.filter(Name=client.name)

    if res:
        client.xero_contact_id = res[0].get('ContactID')
        client.save()
        return False

    return True
