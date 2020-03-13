from billing.models import TIME_ENTRY, DISBURSEMENT, FIXED_PRICE_ITEM

def prepare_xero_invoice_param(invoice):
    line_items = []

    for time_entry in invoice.billing_method_entries:
        time_entry_data = {
            'Quantity': time_entry.units_to_bill if time_entry.entry_type != TIME_ENTRY else time_entry.units_to_bill / 10,
            'UnitAmount': time_entry.rate,
            'TaxType': 'OUTPUT',
            'AccountCode': time_entry.xero_account_number,
            'Tracking': [],
            'ItemCode': time_entry.xero_entry_type,
            'TaxType': time_entry.xero_gst_status
        }

        if time_entry.entry_type == TIME_ENTRY:
            time_entry_data['Description'] = '{}: {} ({}, {} {})'.format(
                    time_entry.date,
                    time_entry.description,
                    time_entry.staff_member.full_name,
                    int(time_entry.units_to_bill),
                    'units' if time_entry.units_to_bill > 1 else 'unit',
                )
        else:
            time_entry_data['Description'] = '{}: {} ({} {})'.format(
                    time_entry.date,
                    time_entry.description,
                    int(time_entry.units_to_bill),
                    'units' if time_entry.units_to_bill > 1 else 'unit',
                )

        if invoice.matter.client.office:
            time_entry_data['Tracking'].append({
                'Name': 'Location',
                'Option': invoice.matter.client.office.location.suburb,
            })

        line_items.append(time_entry_data)

    invoice_data = {
        'Type': 'ACCREC',
        'Reference': invoice.number,
        'Contact': {
            'ContactID': invoice.matter.client.xero_contact_id,
        },
        'Date': invoice.created_date,
        'DueDate': invoice.due_date,
        'Status': 'AUTHORISED',
        'LineAmountTypes': 'Exclusive',
        'LineItems': line_items,
    }


    if invoice.matter.client.office:
        invoice_office = invoice.matter.client.office

        if not invoice_office.xero_branding_theme_id and invoice_office.xero_branding_theme_name:
            invoice_office.get_branding_theme_id_from_xero()

        if invoice_office.xero_branding_theme_id:
            invoice_data['BrandingThemeID'] = invoice_office.xero_branding_theme_id

    return invoice_data

def get_payment_method(ref_str):
    methods = ['EFT', 'BPAY', 'Credit Card', 'Cheque', 'Trust Account', 'Trust Clearing Account', 'Cash', 'Write Off']

    return methods.index(ref_str) + 1 if ref_str in methods else None
