from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal

import graphene
from accounts.models import Client, User
from sitename.utils import check_for_existence, get_xero_client
from billing.models import FIXED_PRICE_ITEM, Matter, TimeEntry
from billing.schema import TimeEntryType
from dateutil import parser
from graphql_relay.node.node import from_global_id
from xero.exceptions import XeroException

from .inputs import InvoiceFixedPriceItemInput, InvoiceInfoInput, InvoiceInput
from .models import Invoice, Payment
from .schema import InvoiceType, PaymentType
from .tasks import send_email, update_invoice_payments

METHODS = [
    'EFT', 'BPAY', 'Credit Card', 'Cheque',
    'Trust Account', 'Trust Clearing Account',
    'Cash', 'Write Off'
]


class CreateInvoiceMutation(graphene.Mutation):
    class Arguments:
        invoice_data = InvoiceInput()

    errors = graphene.List(graphene.String)
    invoice = graphene.Field(lambda: InvoiceType)

    @staticmethod
    def mutate(root, info, **args):
        errors = []
        invoice = None
        invoice_data = args.get('invoice_data')

        try:
            check_for_existence(
                *[(time_entry.id, TimeEntry)
                  for time_entry in
                  invoice_data.recorded_time],
                (invoice_data.matter.id, Matter),
            )
        except Exception as e:
            errors.append(str(e))
            return CreateInvoiceMutation(errors=errors, invoice=None)

        matter_id = from_global_id(invoice_data.matter.id)[1]

        invoice = Invoice.objects.create(
            matter_id=matter_id,
            created_date=datetime.now(),
            payment_terms_id=1,
            billing_method=invoice_data.billing_method,
        )

        for fixed_price_item in invoice_data.fixed_price_items:
            fixed_price_item = {**fixed_price_item}
            del fixed_price_item['id']

            TimeEntry.objects.create(
                entry_type=FIXED_PRICE_ITEM,
                invoice=invoice,
                staff_member=info.context.user,
                **fixed_price_item
            )
        if len(invoice_data.recorded_time):
            for time in invoice_data.recorded_time:
                time_entry_id = from_global_id(time.id)[1]
                time_entry = TimeEntry.objects.get(pk=time_entry_id)
                time_entry.units_to_bill = time.units_to_bill
                time_entry.save()

                invoice.time_entries.add(time_entry)

        invoice.matter.update(
            **invoice_data.matter,
            exclude=['time_entries', 'budget']
        )
        invoice.matter.budget = invoice_data.matter.budget or 0
        invoice.save()

        return CreateInvoiceMutation(errors=errors, invoice=invoice)


class UpdateInvoiceInfoMutation(graphene.Mutation):
    class Arguments:
        invoice_id = graphene.ID()
        invoice_data = InvoiceInfoInput()

    errors = graphene.List(graphene.String)
    invoice = graphene.Field(lambda: InvoiceType)

    @staticmethod
    def mutate(root, info, **args):
        errors = []
        invoice = None
        invoice_id = args.get('invoice_id')
        invoice_data = args.get('invoice_data')

        try:
            check_for_existence(
                (invoice_data.matter.client.id, Client),
                (invoice_data.matter.id, Matter),
                (invoice_data.matter.manager.id, User),
                (invoice_id, Invoice),
            )
        except Exception as e:
            errors.append(str(e))
            return UpdateInvoiceInfoMutation(errors=errors, invoice=None)

        invoice_id = from_global_id(invoice_id)[1]
        invoice = Invoice.objects.get(pk=invoice_id)

        res = invoice.can_update()

        if not res.get('success'):
            errors.append(res.get('error'))
            return UpdateInvoiceInfoMutation(errors=errors, invoice=None)

        invoice.update(**invoice_data)
        invoice.matter.update(**invoice_data.matter)

        if invoice.is_in_xero:
            invoice.send_to_xero()
        invoice.save()
        invoice.refresh_from_db()

        return UpdateInvoiceInfoMutation(errors=errors, invoice=invoice)


class UpdateInvoiceMutation(graphene.Mutation):
    class Arguments:
        invoice_id = graphene.ID()
        recorded_time = graphene.List(graphene.ID)

    errors = graphene.List(graphene.String)
    invoice = graphene.Field(lambda: InvoiceType)

    @staticmethod
    def mutate(root, info, **args):
        errors = []
        invoice = None
        recorded_time = args.get('recorded_time')
        invoice_id = args.get('invoice_id')

        try:
            check_for_existence(
                *[(time_entry_id, TimeEntry)
                  for time_entry_id in recorded_time],
                (invoice_id, Invoice),
            )
        except Exception as e:
            errors.append(str(e))
            return UpdateInvoiceMutation(errors=errors, invoice=None)

        invoice_id = from_global_id(invoice_id)[1]
        invoice = Invoice.objects.get(pk=invoice_id)

        res = invoice.can_update()

        if not res.get('success'):
            errors.append(res.get('error'))
            return UpdateInvoiceInfoMutation(errors=errors, invoice=None)

        invoice.time_entries.set(
            [TimeEntry.objects.get(pk=pk)
             for pk in recorded_time]
        )

        if invoice.is_in_xero:
            invoice.send_to_xero()
        invoice.save()
        return UpdateInvoiceMutation(errors=errors, invoice=invoice)


class RemoveTimeRecordMutation(graphene.Mutation):
    class Arguments:
        time_record_id = graphene.ID()
        time_record_type = graphene.Int()

    errors = graphene.List(graphene.String)

    @staticmethod
    def mutate(root, info, **args):
        errors = []
        time_record_id = from_global_id(args.get('time_record_id'))[1]
        time_record_type = args.get('time_record_type')

        if time_record_type is 1:
            time_record_model = TimeEntry

        try:
            check_for_existence((time_record_id, time_record_model))
        except Exception as e:
            errors.append(str(e))
            return RemoveTimeRecordMutation(errors=errors)

        time_record = time_record_model.objects.get(pk=time_record_id)
        time_record.invoice = None
        time_record.save()

        return RemoveTimeRecordMutation(errors=errors)


class AddPaymentMutation(graphene.Mutation):
    class Arguments:
        invoice_id = graphene.ID()
        date = graphene.String()
        method = graphene.Int()
        amount = graphene.Float()

    errors = graphene.List(graphene.String)
    payment = graphene.Field(lambda: PaymentType)

    @staticmethod
    def mutate(root, info, **args):
        errors = []
        payment = None

        if not info.context.user.has_perm('invoicing.add_payment'):
            errors.append('You do not have a permission to add a payment!')
            return AddPaymentMutation(errors=errors)

        try:
            invoice_id = from_global_id(args.get('invoice_id'))[1]
            invoice = Invoice.objects.get(id=invoice_id)

            if not invoice.xero_invoice_id:
                errors.append('Invoice is manually entered in Xero')
                return AddPaymentMutation(errors=errors)

            xero = get_xero_client()
            res = xero.invoices.filter(InvoiceID=invoice.xero_invoice_id)

            if not res:
                errors.append('Invoice is manually entered in Xero')
                return AddPaymentMutation(errors=errors)

            payment_data = {
                'Invoice': {
                    'InvoiceID': invoice.xero_invoice_id,
                },
                'Account': {
                    'Code': '090',
                },
                'Amount': args.get('amount'),
                'Date': parser.parse(args.get('date')),
                'Reference': METHODS[args.get('method') - 1],
            }

            xero_payment = xero.payments.put(payment_data)[0]
            print(xero_payment)

            payment = Payment.objects.create(
                invoice_id=invoice.id,
                amount=Decimal(args.get('amount')).quantize(
                    Decimal('.01'),
                    rounding=ROUND_HALF_UP
                ),
                date=parser.parse(args.get('date')),
                method=args.get('method'),
                xero_payment_id=xero_payment.get('PaymentID')
            )
            payment.invoice.save()

            return AddPaymentMutation(errors=errors, payment=payment)

        except Invoice.DoesNotExist:
            errors.append('Invoice with provided id does not exist')
            return AddPaymentMutation(errors=errors)
        except XeroException as e:
            print(str(e))
            errors.append('Failed to create payment in Xero')
            return AddPaymentMutation(errors=errors)
        except Exception as e:
            print(str(e))
            errors.append('Failed to create payment')
            return AddPaymentMutation(errors=errors)

        return AddPaymentMutation(errors=errors, payment=payment)


class RemoveFixedPriceItem(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    errors = graphene.List(graphene.String)
    invoice = graphene.Field(lambda: InvoiceType)

    @staticmethod
    def mutate(root, info, id):
        errors = []
        invoice = None
        time_id = from_global_id(id)[1]

        try:
            fixed_price_item = TimeEntry.objects.get(id=time_id)
            invoice = fixed_price_item.invoice
            fixed_price_item.delete()
            fixed_price_item.invoice.save()
        except TimeEntry.DoesNotExist:
            errors.append('Fixed price item with provided id does not exist')
            return RemoveFixedPriceItem(errors=errors, invoice=invoice)

        return RemoveFixedPriceItem(errors=errors, invoice=invoice)


class CreateFixedPriceItem(graphene.Mutation):
    class Arguments:
        invoice_id = graphene.ID()
        fixed_price_item = InvoiceFixedPriceItemInput()

    errors = graphene.List(graphene.String)
    invoice = graphene.Field(lambda: InvoiceType)

    @staticmethod
    def mutate(root, info, **args):
        errors = []
        invoice = None
        fixed_price_item = args.get('fixed_price_item')

        try:
            check_for_existence(
                (args.get('invoice_id'), Invoice),
            )
        except Exception as e:
            errors.append(str(e))
            return CreateFixedPriceItem(errors=errors, invoice=invoice)

        invoice_id = from_global_id(args.get('invoice_id'))[1]
        invoice = Invoice.objects.get(id=invoice_id)

        res = invoice.can_update()

        if not res.get('success'):
            errors.append(res.get('error'))
            return UpdateInvoiceInfoMutation(errors=errors, invoice=None)

        TimeEntry.objects.create(
            invoice=invoice,
            entry_type=3,
            staff_member=info.context.user,
            **fixed_price_item
        )

        if invoice.is_in_xero:
            invoice.send_to_xero()
        invoice.save()
        return CreateFixedPriceItem(invoice=invoice)


class UpdateFixedPriceItem(graphene.Mutation):
    class Arguments:
        invoice_id = graphene.ID()
        fixed_price_item = InvoiceFixedPriceItemInput()

    errors = graphene.List(graphene.String)
    fixed_price_item = graphene.Field(lambda: TimeEntryType)
    invoice = graphene.Field(lambda: InvoiceType)

    @staticmethod
    def mutate(root, info, **args):
        errors = []
        fixed_price_item = None
        invoice = None
        fixed_price_item_data = args.get('fixed_price_item')
        fixed_price_item_id = from_global_id(fixed_price_item_data.id)[1]

        try:
            check_for_existence(
                (fixed_price_item_data.id, TimeEntry)
            )
        except Exception as e:
            errors.append(str(e))
            return UpdateFixedPriceItem(
                errors=errors,
                invoice=None,
                fixed_price_item=None
            )

        fixed_price_item = TimeEntry.objects.get(id=fixed_price_item_id)
        invoice = fixed_price_item.invoice
        fixed_price_item.update(**fixed_price_item_data)
        fixed_price_item.invoice.save()
        return UpdateFixedPriceItem(
            fixed_price_item=fixed_price_item,
            invoice=invoice
        )


class SendInvoiceEmail(graphene.Mutation):
    class Arguments:
        invoice_id = graphene.ID(required=True)

    errors = graphene.List(graphene.String)
    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, **args):
        errors = []
        try:
            check_for_existence(
                (args.get('invoice_id'), Invoice),
            )
        except Exception as e:
            errors.append(str(e))
            return SendInvoiceEmail(errors=errors, success=False)

        invoice_id = from_global_id(args.get('invoice_id'))[1]
        send_email.delay(invoice_id, staff_member_email=info.context.user.email)

        return SendInvoiceEmail(success=True)


class SendInvoiceToXero(graphene.Mutation):
    class Arguments:
        invoice_id = graphene.ID(required=True)

    errors = graphene.List(graphene.String)
    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, **args):
        errors = []

        try:
            invoice_id = from_global_id(args.get('invoice_id'))[1]
            invoice = Invoice.objects.get(id=invoice_id)

            res = invoice.send_to_xero()

            if not res.get('success'):
                errors.append(res.get('error'))
                return SendInvoiceToXero(errors=errors, success=False)

        except Invoice.DoesNotExist:
            errors.append('Invoice with the provided id does not exist')
            return SendInvoiceToXero(errors=errors, success=False)

        except Exception as e:
            print(str(e))
            errors.append('Failed to create invoice in Xero')
            return SendInvoiceToXero(errors=errors, success=False)

        return SendInvoiceToXero(success=True)


class FetchPaymentsFromXero(graphene.Mutation):
    class Arguments:
        invoice_id = graphene.ID(required=True)

    errors = graphene.List(graphene.String)
    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, **args):
        errors = []

        try:
            invoice_id = from_global_id(args.get('invoice_id'))[1]
            invoice = Invoice.objects.get(id=invoice_id)

            res = invoice.fetch_payments_from_xero()

            if not res.get('success'):
                errors.append(res.get('error'))
                return FetchPaymentsFromXero(errors=errors, success=False)

        except Invoice.DoesNotExist:
            errors.append('Invoice with the provided id does not exist')
            return FetchPaymentsFromXero(errors=errors, success=False)

        except Exception as e:
            print(str(e))
            errors.append('Failed to fetch payments from Xero')
            return FetchPaymentsFromXero(errors=errors, success=False)

        invoice.save()
        return FetchPaymentsFromXero(success=True)


class FetchAllPaymentsFromXero(graphene.Mutation):
    errors = graphene.List(graphene.String)
    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, **args):
        errors = []

        try:
            update_invoice_payments.delay()
        except Exception as e:
            print(str(e))
            errors.append('Failed to fetch all payments from Xero')
            return FetchAllPaymentsFromXero(errors=errors, success=False)

        return FetchAllPaymentsFromXero(success=True)
