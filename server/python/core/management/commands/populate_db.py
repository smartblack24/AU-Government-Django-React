import csv
from decimal import Decimal

import psycopg2

from accounts.models import (SALUTATIONS, Client, Contact, Location,
                             Organisation, User)
from billing.models import Matter, Note, StandartDisbursement, TimeEntry
from core.models import (Document, DocumentType, Industry, InvoiceStatus,
                         MatterType, Occupation, Office, Section)
from dateutil import parser
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db.models import Max
from django.db.utils import IntegrityError
from invoicing.models import Invoice, Payment, PaymentTerms


class Command(BaseCommand):
    help = 'Populated db from csv files'

    def add_arguments(self, parser):
        parser.add_argument('model', type=str)

    def handle(self, *args, **options):
        model = options['model']

        if model == 'contacts':
            self.populate_contacts()
        elif model == 'organisations':
            self.populate_organisations()
        elif model == 'clients':
            self.populate_clients()
        elif model == 'users':
            self.populate_users()
        elif model == 'matters':
            self.populate_matters()
        elif model == 'invoices':
            self.populate_invoices()
        elif model == 'time-entries':
            self.populate_time_entries()
        elif model == 'payments':
            self.populate_payments()
        elif model == 'matter_notes':
            self.populate_matter_notes()
        elif model == 'safe_storage':
            self.populate_safe_storage()
        elif model == 'standard_disbursements':
            self.populate_standard_disbursements()
        elif model == 'admin_group':
            self.create_admin_group()
        elif model == 'xero_group':
            self.create_xero_group()
        elif model == 'mail_group':
            self.create_mail_group()
        elif model == 'all':
            office1_location = Location.objects.create(
                address1="Level 15",
                address2="45 Clarence Street",
                suburb="Sydney",
                state=2,
                post_code="2000",
                country="Australia"
            )

            office2_location = Location.objects.create(
                address1="Level 4",
                address2="29 King William Street",
                suburb="Adelaide",
                state=1,
                post_code="5000",
                country="Australia"
            )

            Office.objects.create(
                id=1,
                legal_entity="Andreyev (Sydney) Pty Ltd",
                abn="29 697 640 228",
                location=office1_location,
                phone="1300 654 590",
                web="www.andreyev.com.au",
                bank_account_name="Andreyev Lawyers",
                bank_account_bsb="115 879",
                bank_account_number="02884031",
                bpay_biller_code="208447"
            )

            Office.objects.create(
                id=2,
                legal_entity="Andreyev (Sydney) Pty Ltd",
                abn="16 994 767 151",
                location=office2_location,
                phone="1300 654 590",
                web="www.andreyev.com.au",
                bank_account_name="Andreyev Lawyers",
                bank_account_bsb="115 879",
                bank_account_number="028840351",
                bpay_biller_code="208447"
            )

            InvoiceStatus.objects.create(id=1, name="Draft")
            InvoiceStatus.objects.create(id=2, name="Waiting approval")
            InvoiceStatus.objects.create(id=3, name="Approved")
            InvoiceStatus.objects.create(id=4, name="Printed")
            InvoiceStatus.objects.create(id=5, name="In Xero")
            PaymentTerms.objects.create(id=1)
            self.populate_users()
            print('populate_users done')
            self.populate_organisations()
            print('populate_organisations done')
            self.populate_contacts()
            print('populate_contacts done')
            self.populate_clients()
            print('populate_clients done')
            self.populate_matters()
            print('populate_matters done')
            self.populate_invoices()
            print('populate_invoices done')
            self.populate_time_entries()
            print('populate_time_entries done')
            self.populate_payments()
            print('populate_payments done')
            self.populate_matter_notes()
            print('populate_matter_notes done')
            self.populate_safe_storage()
            print('populate_safe_storage done')
            self.populate_standard_disbursements()
            print('populate_standard_disbursements done')
            self.create_admin_group()
            print('Admin group is created')
            self.create_xero_group()
            print('Xero group is created')
            self.create_mail_group()
            print('Mail group is created')

        conn = psycopg2.connect(
            "host='db' dbname='sitename' user='sitename' password='sitename123'")
        cur = conn.cursor()

        contact_max_id = Contact.objects.aggregate(
            max=Max('id')).get('max') + 1
        organisation_max_id = Organisation.objects.aggregate(
            max=Max('id')).get('max') + 1
        client_max_id = Client.objects.aggregate(max=Max('id')).get('max') + 1
        user_max_id = User.objects.aggregate(max=Max('id')).get('max') + 1
        matter_max_id = Matter.objects.aggregate(max=Max('id')).get('max') + 1
        invoice_max_id = Invoice.objects.aggregate(
            max=Max('id')).get('max') + 1
        time_entry_max_id = TimeEntry.objects.aggregate(
            max=Max('id')).get('max') + 1
        payment_max_id = Payment.objects.aggregate(
            max=Max('id')).get('max') + 1

        cur.execute(
            "ALTER SEQUENCE accounts_contact_id_seq RESTART WITH %s;" % contact_max_id)
        cur.execute(
            "ALTER SEQUENCE accounts_organisation_id_seq RESTART WITH %s;" % organisation_max_id)
        cur.execute(
            "ALTER SEQUENCE accounts_client_id_seq RESTART WITH %s;" % client_max_id)
        cur.execute(
            "ALTER SEQUENCE accounts_user_id_seq RESTART WITH %s;" % user_max_id)
        cur.execute(
            "ALTER SEQUENCE billing_matter_id_seq RESTART WITH %s;" % matter_max_id)
        cur.execute(
            "ALTER SEQUENCE invoicing_invoice_id_seq RESTART WITH %s;" % invoice_max_id)
        cur.execute(
            "ALTER SEQUENCE billing_timeentry_id_seq RESTART WITH %s;" % time_entry_max_id)
        cur.execute(
            "ALTER SEQUENCE invoicing_payment_id_seq RESTART WITH %s;" % payment_max_id)

        conn.commit()
        cur.close()
        conn.close()

        self.stdout.write(
            self.style.SUCCESS('Successfully populate "%s" table' % model)
        )

    def handle_state(self, state):
        for row in Location.STATES:
            if row[1] == state:
                return row[0]

        return None

    def handle_active_status(self, active_status):
        return active_status == 'Active'

    def populate_contacts(self):
        def handle_occupation(new_occupation):
            blank_occupation, is_created = Occupation.objects.get_or_create(
                name="-------"
            )

            for row in Contact.OCCUPATIONS:
                if row[1] == new_occupation:
                    occupation, is_created = Occupation.objects.get_or_create(
                        name=row[1]
                    )
                    return occupation

            return blank_occupation

        def handle_salutations(salutation):
            for row in SALUTATIONS:
                if row[1] == salutation:
                    return row[0]

            return None

        def handle_email(email):
            if email == '':
                return None

            return email

        with open('csv/contacts.csv', newline='', encoding="ISO-8859-1") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                location = None
                postal_location = None
                if row['Ctact Addr Home Street 1']:
                    location = Location.objects.create(
                        address1=row['Ctact Addr Home Street 1'],
                        address2=row['Ctact Addr Home Street 2'],
                        suburb=row['Ctact Addr Home Suburb'],
                        state=self.handle_state(row['Ctact Addr Home State']),
                        post_code=row['Ctact Addr Home PC'],
                        country=row['Ctact Addr Home Country'],
                    )
                if row['Ctact Addr Postal Street 1']:
                    postal_location = Location.objects.create(
                        address1=row['Ctact Addr Postal Street 1'],
                        address2=row['Ctact Addr Postal Street 2'],
                        suburb=row['Ctact Addr Postal Suburb'],
                        state=self.handle_state(
                            row['Ctact Addr Postal State']),
                        post_code=row['Ctact Addr Postal PC'],
                        country=row['Ctact Addr Postal Country'],
                    )

                organisation = None
                if row['c_Ctact Client Org Name'] != '1' and row['c_Ctact Client Org Name']:
                    try:
                        organisation = Organisation.objects.get(
                            pk=row['c_Ctact Client Org Name'])
                    except Organisation.DoesNotExist:
                        pass

                try:
                    contact = Contact.objects.create(
                        id=row['id'],
                        first_name=row['Ctact Name First'],
                        last_name=row['Ctact Name Last'],
                        mobile=row['Ctact Phone Mobile'],
                        direct_line=row['Ctact Phone DirectLine'],
                        email=handle_email(row['Ctact Email Main']),
                        secondary_email=row['Ctact Email Secondary'],
                        occupation=handle_occupation(row['Ctact Occupation']),
                        is_active=self.handle_active_status(
                            row['Ctact ActiveStatus']),
                        salutation=handle_salutations(row['Salutation']),
                        location=location,
                        postal_location=postal_location,
                    )
                    contact.organisations.add(organisation)
                except IntegrityError:
                    pass

        with open('csv/contacts.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Ctact Referrer ID']:
                    try:
                        contact = Contact.objects.get(pk=row['id'])
                        contact.referrer_id = row['Ctact Referrer ID']
                        contact.save()
                    except Exception:
                        pass

    def populate_organisations(self):
        def handle_industry(industry_name):
            if industry_name and industry_name != '*':
                try:
                    return Industry.objects.get(name=industry_name)
                except Industry.DoesNotExist:
                    return Industry.objects.create(name=industry_name)

                    return None

        def handle_group_status(group_status):
            if group_status == 'Parent':
                return 1

            return 2

        with open('csv/organisations.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Org Name'] != 'None' and row['Org Name']:
                    location = None
                    postal_location = None

                    if row['Org Addr Street 1']:
                        location = Location.objects.create(
                            address1=row['Org Addr Street 1'],
                            address2=row['Org Addr Street 2'],
                            suburb=row['Org Addr Suburb'],
                            state=self.handle_state(row['Org Addr State']),
                            post_code=row['Org Addr PC'],
                            country=row['Org Addr Country'],
                        )

                    if row['Org Addr Postal Street 1']:
                        postal_location = Location.objects.create(
                            address1=row['Org Addr Postal Street 1'],
                            address2=row['Org Addr Postal Street 2'],
                            suburb=row['Org Addr Postal Suburb'],
                            state=self.handle_state(
                                row['Org Addr Postal State']),
                            post_code=row['Org Addr Postal PC'],
                            country=row['Org Addr Postal Country'],
                        )

                    Organisation.objects.create(
                        id=row['id'],
                        name=row['Org Name'],
                        main_line=row['Org Main Phone'],
                        industry=handle_industry(row['Org Industry']),
                        website=row['Org Website'],
                        location=location,
                        postal_location=postal_location,
                        group_status=handle_group_status(
                            row['Org Group Status']),
                    )

        with open('csv/organisations.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Org Name'] != 'None' and row['Org Group Parent']:
                    organisation = Organisation.objects.get(pk=row['id'])

                    try:
                        parent = Organisation.objects.get(
                            name=row['Org Group Parent'])
                    except Organisation.DoesNotExist:
                        pass

                    organisation.group_parent = parent
                    organisation.save()

    def populate_clients(self):
        with open('csv/clients.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    contact = Contact.objects.get(pk=row['ContactID_Fk'])
                    contact.role = row['Role']
                    contact.save()
                except Contact.DoesNotExist:
                    contact = None

                organisation = None

                if row['OrganisationID_Fk'] != '1' and row['OrganisationID_Fk'] != '-1':
                    try:
                        organisation = Organisation.objects.get(
                            pk=row['OrganisationID_Fk'])
                    except Organisation.DoesNotExist:
                        pass

                if contact and organisation:
                    contact.organisations.add(organisation)

                if row['Office'] == 'Adelaide':
                    office = Office.objects.get(id=2)
                elif row['Office'] == 'Sydney':
                    office = Office.objects.get(id=1)
                else:
                    office = None

                Client.objects.create(
                    id=row['id'],
                    contact=contact,
                    organisation=organisation,
                    # is_active=self.handle_active_status(row['ActiveStatus']),
                    created_date=parser.parse(
                        row['DateCreated'], dayfirst=True),
                    office=office
                )

    def populate_users(self):
        # def handle_rate(rate):
        #     if rate:
        #         return rate.split('$')[1]
        #
        #     return 0

        def handle_admission_date(date):
            if date:
                return parser.parse(date, dayfirst=True)

            return None

        def handle_salutations(salutation):
            for row in SALUTATIONS:
                if row[1] == salutation:
                    return row[0]

            return None

        with open('csv/users.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    User.objects.create(
                        id=row['id'],
                        email=row['Email'],
                        first_name=row['NameFirst'],
                        last_name=row['NameLast'],
                        mobile=row['Mobile'],
                        salutation=handle_salutations(row['Salutation']),
                        rate=row['ChargeRate'] or 0,
                        admission_date=handle_admission_date(
                            row['DateAdmission']),
                    )
                except IntegrityError:
                    pass

    def populate_matters(self):
        def handle_status(status):
            if status == 'Open' or status == 'Ope':
                return 1
            elif status == 'Suspended':
                return 2
            elif status == 'Closed' or status == 'Close':
                return 3

        def handle_billing_method(method):
            if method == 'Fixed Price':
                return 1

            return 2

        def handle_conflict_status(status):
            if status == 'Outstanding':
                return 1
            elif status == 'No other parties':
                return 2
            elif status == 'Complete':
                return 3

        def handle_budget(budget):
            if not budget:
                return 0

            return float(budget)

        def handle_date(date):
            if not date:
                return None

            return parser.parse(date, dayfirst=True)

        with open('csv/matters.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    client = Client.objects.get(pk=row['ClientID_Fk'])
                except Client.DoesNotExist:
                    client = None

                try:
                    principal = User.objects.get(pk=row['Principal_Staff_Fk'])
                except ValueError:
                    principal = None

                try:
                    manager = User.objects.get(pk=row['Manager_Staff_Fk'])
                except ValueError:
                    manager = None
                except User.DoesNotExist:
                    print('Manager_Staff_Fk=' + row['Manager_Staff_Fk'])

                assistant = None
                if row['Assistant_Staff_Fk']:
                    assistant = User.objects.get(pk=row['Assistant_Staff_Fk'])

                try:
                    matter_type = MatterType.objects.get(
                        name=row['MatterType'])
                except MatterType.DoesNotExist:
                    matter_type = MatterType.objects.create(
                        name=row['MatterType'])

                conflict_parties_row = None
                if row['Conflict Parties']:
                    conflict_parties_row = row['Conflict Parties']
                Matter.objects.create(
                    id=row['id'],
                    client=client,
                    manager=manager,
                    principal=principal,
                    assistant=assistant,
                    billable_status=handle_status(row['Status']),
                    matter_type=matter_type,
                    name=row['MatterName'],
                    description=row['MatterDescription'],
                    created_date=handle_date(row['DateCreated']),
                    closed_date=handle_date(row['DateClosed']),
                    budget=handle_budget(row['Budget']),
                    # Change this limit
                    file_path=row['ClientFolderName'][:99] or None,
                    billing_method=handle_billing_method(row['BillingMethod']),
                    conflict_status=handle_conflict_status(
                        row['Conflict Status']),
                    conflict_parties=conflict_parties_row,
                )

    def populate_invoices(self):
        def handle_date(date):
            if date != '?':
                return parser.parse(date, dayfirst=True)

            return None

        def handle_entry_type(entry_type):
            if entry_type == 'Time Entry':
                return 2
            elif entry_type == 'Fixed Price':
                return 1

        with open('csv/invoices.csv', newline='', encoding="ISO-8859-1") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                matter = Matter.objects.get(pk=row['MatterID_Fk'])

                Invoice.objects.create(
                    id=row['id'],
                    billing_method=handle_entry_type(row['BillingMethod']),
                    matter=matter,
                    created_date=handle_date(row['DateCreated']),
                )

    def handle_billable_status(self, status):
        if status == 'Billable':
            return 1
        elif status == 'Non Billable':
            return 2

        return None

    def handle_gst(self, gst):
        if gst == 'GST (10%)':
            return 1
        elif gst == 'GST Export (0%)':
            return 2
        elif gst == 'BAS Excluded (0%)':
            return 3

        return 2

    def populate_time_entries(self):
        def handle_entry_type(entry_type):
            if entry_type == 'Time Entry':
                return 1
            elif entry_type == 'Disbursement':
                return 2
            elif entry_type == 'Fixed Price':
                return 3

            return 1

        def handle_rate(rate):
            if rate and rate != '?':
                return Decimal(rate)

            return None

        def handle_date(date):
            if date == '?':
                return None
            else:
                return parser.parse(date, dayfirst=True)

        with open('csv/time-entries.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    client = Client.objects.get(pk=row['ClientID_Fk'])
                except Exception:
                    client = None
                try:
                    staff = User.objects.get(pk=row['StaffID_Fk'])
                except Exception:
                    staff = None
                try:
                    matter = Matter.objects.get(pk=row['MatterID_Fk'])
                except Exception:
                    matter = None
                try:
                    invoice = Invoice.objects.get(pk=row['InvoiceID_Fk'])
                except Exception:
                    invoice = None

                TimeEntry.objects.create(
                    id=row['id'],
                    client=client,
                    staff_member=staff,
                    matter=matter,
                    invoice=invoice,
                    rate=handle_rate(row['Unit Rate pre GST']),
                    date=handle_date(row['Date entered']),
                    units=row['Units Actual'] or 0,
                    units_to_bill=row['Units Actual'] or 0,
                    status=self.handle_billable_status(
                        row['Billable Status']),
                    description=row['Entry Description'],
                    gst_status=self.handle_gst(row['GST Status']),
                    entry_type=handle_entry_type(row['Billing entry'])
                )

    def populate_payments(self):
        def handle_method(method):
            if method.lower() == 'eft':
                return 1
            elif method == 'BPAY':
                return 2
            elif method.lower() == 'credit card':
                return 3
            elif 'cheque' in method.lower():
                return 4
            elif method == 'Trust Account':
                return 5
            elif method == 'Trust Clearing Account':
                return 6
            elif method == 'Cash':
                return 7

            return None

        with open('csv/payments.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if not row['Payment Date']:
                    continue

                try:
                    invoice = Invoice.objects.get(pk=row['InvoiceID_Fk'])
                except Exception:
                    invoice = None

                try:
                    Payment.objects.create(
                        id=row['ID'],
                        invoice=invoice,
                        date=parser.parse(row['Payment Date'], dayfirst=True),
                        amount=Decimal(row['Payment Amount']),
                        method=handle_method(row['Payment Method']),
                    )
                except AttributeError:
                    continue

    def populate_matter_notes(self):
        def handle_date(date):
            if date:
                return parser.parse(date, dayfirst=True)

            return None

        with open('csv/matter_notes.csv', newline='', encoding="ISO-8859-1") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    matter = Matter.objects.get(pk=row['Matter_ID_fk'])
                except Matter.DoesNotExist:
                    continue

                user = None
                if row['Staff Name']:
                    try:
                        full_name = row['Staff Name'].split()
                        first_name = full_name[0]
                        last_name = full_name[1] if len(full_name) == 2 else ' '
                        user = User.objects.get(
                            first_name=first_name, last_name=last_name)
                    except User.DoesNotExist:
                        pass

                Note.objects.create(
                    matter=matter,
                    text=row['Update Entry'],
                    date_time=handle_date(row['Update Date']),
                    user=user
                )

    def populate_safe_storage(self):
        def handle_nominated_type(nominated_type):
            for nom_type in Document.NOMINATED_TYPES:
                if nom_type[1].lower() == nominated_type.lower():
                    return nom_type[0]

            return Document.NOMINATED_TYPES[-1][0]

        def handle_status(status):
            for stat in Document.DOCUMENT_STATUSES:
                if stat[1].lower() == status.lower():
                    return stat[0]

            return None

        def handle_andrew_executor(andrew_executor):
            if andrew_executor.lower() == 'No':
                return False

            elif andrew_executor.lower() == 'Yes':
                return True

            return False

        def handle_charging_clause(value):
            for row in Document.CHARGING_CLAUSE:
                if row[1].lower() == value.lower():
                    return row[0]

            return None

        def handle_date(date):
            if date:
                try:
                    return parser.parse(date, dayfirst=True)
                except ValueError:
                    return None

            return None

        document_type, is_created = DocumentType.objects.get_or_create(
            name="No selection")

        with open('csv/safe_storage_contacts.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:

                section = None

                if row['CodeLocation::Code']:
                    if row['CodeLocation::CodeLocation'] == 'SYD':
                        office = Office.objects.first()
                    else:
                        office = Office.objects.last()
                    try_section = Section.objects.filter(
                        number=row['CodeLocation::Code'], office=office)
                    if try_section.exists():
                        section = try_section.first()
                    else:
                        section = Section.objects.create(
                            number=row['CodeLocation::Code'],
                            office=office
                        )

                    # section, is_created = Section.objects.get_or_create(
                    #     office=office,
                    #     number=row['CodeLocation::Code']
                    #     )

                try:
                    try:
                        contact = Contact.objects.get(
                            pk=row['ContactList::FMP RelatedID'])
                    except Contact.DoesNotExist:
                        contact = None

                    document_type, is_created = DocumentType.objects.get_or_create(
                        name=row['DocumentType'])

                    Document.objects.create(
                        document_type=document_type,
                        contact=contact,
                        nominated_type=handle_nominated_type(
                            row['NominatedType']),
                        nominated_names=row['NominatedName.s'],
                        status=handle_status(row['DocumentStatus']),
                        notes=row['DocumentNotes'],
                        date=handle_date(row['DocumentDate']),
                        andrew_executor=handle_andrew_executor(
                            row['Will_AAExecutor']),
                        charging_clause=handle_charging_clause(
                            row['Will_ChargingClause']),
                        section=section,
                        date_removed=handle_date(row['DateRemoved'])
                    )
                except ValueError:
                    continue

        with open('csv/safe_storage_organisations.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:

                section = None

                if row['CodeLocation::Code']:
                    try:
                        section = Section.objects.get(
                            number=row['CodeLocation::Code'])
                    except Section.DoesNotExist:
                        section = Section.objects.create(
                            office=Office.objects.first(),
                            number=row['CodeLocation::Code'])
                try:
                    try:
                        organisation = Organisation.objects.get(
                            pk=row['ContactList::FMP RelatedOrgID'])
                    except Organisation.DoesNotExist:
                        organisation = None

                    document_type, is_created = DocumentType.objects.get_or_create(
                        name=row['DocumentType'])

                    Document.objects.create(
                        document_type=document_type,
                        organisation=organisation,
                        nominated_type=handle_nominated_type(
                            row['NominatedType']),
                        nominated_names=row['NominatedName.s'],
                        status=handle_status(row['DocumentStatus']),
                        notes=row['DocumentNotes'],
                        date=handle_date(row['DocumentDate']),
                        andrew_executor=handle_andrew_executor(
                            row['Will_AAExecutor']),
                        charging_clause=handle_charging_clause(
                            row['Will_ChargingClause']),
                        section=section,
                        date_removed=handle_date(row['DateRemoved'])
                    )
                except ValueError:
                    continue

    def populate_standard_disbursements(self):

        def handle_rate(rate):
            if rate and rate != '?':
                return Decimal(rate)

            return None

        def handle_gst(self, gst):
            if gst == 'GST (10%)':
                return 1
            elif gst == 'GST Export (0%)':
                return 2
            elif gst == 'BAS Excluded (0%)':
                return 3

            return 2

        with open('csv/standard_disbursements.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                StandartDisbursement.objects.create(
                    cost=handle_rate(row['Item_Value']),
                    description=row['Item_Description'],
                    gst_status=self.handle_gst(row['GST Status']),
                    name=row['Item_Name']
                )

    def create_admin_group(self):
        admin_group = Group.objects.create(name='Admin')
        for perm in Permission.objects.all():
            admin_group.permissions.add(perm)

    def create_xero_group(self):
        xero_group = Group.objects.create(name='Xero')
        xero_content_type = ContentType.objects.create(app_label='integration', model='xero_work')
        Permission.objects.create(codename='can_use_xero', name='Can use xero', content_type=xero_content_type)
        
    def create_mail_group(self):
        mail_group = Group.objects.create(name='Mail')
        mail_content_type = ContentType.objects.create(app_label='integration', model='mailbox')
        Permission.objects.create(codename='can_delete_mails', name='Can delete mails', content_type=mail_content_type)
        Permission.objects.create(codename='can_link_mails', name='Can link mails', content_type=mail_content_type)
