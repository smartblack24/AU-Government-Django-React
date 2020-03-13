import graphene
from accounts.models import Client, Contact, Organisation
from sitename.decorators import login_required, login_required_relay
from billing.models import Matter, Note, TimeEntry
from django.db.models import FloatField
from django.db.models.functions import Cast
from graphene import relay
from graphql_relay.node.node import from_global_id
from invoicing.models import Invoice, Payment
from sitename.utils import get_xero_client

from .inputs import DocumentInput
from .models import Document, Office, Section
from .schema import DocumentType, SectionType


class RemoveInstanceMutation(relay.ClientIDMutation):
    class Input:
        instance_id = graphene.ID(requried=True)
        instance_type = graphene.Int(requried=True)

    errors = graphene.List(graphene.String)

    @classmethod
    @login_required_relay
    def mutate_and_get_payload(cls, root, info, **input):
        try:
            instance_id = from_global_id(input.get('instance_id'))[1]
        except Exception:
            instance_id = input.get('instance_id')

        instance_type = input.get('instance_type')
        errors = []

        if not instance_id:
            errors.append('Instance id must be specified')

        if not instance_type:
            errors.append('Instance type must be specified')

        if not errors:
            if instance_type is 1:
                try:
                    Contact.objects.get(pk=instance_id).delete()
                except Contact.DoesNotExist:
                    errors.append(
                        'Contact with the provided id does not exists'
                    )
                    return RemoveInstanceMutation(errors=errors)

                except Exception as e:
                    errors.append(str(e))
                    return RemoveInstanceMutation(errors=errors)

            elif instance_type is 2:
                try:
                    Organisation.objects.get(pk=instance_id).delete()
                except Organisation.DoesNotExist:
                    errors.append(
                        'Organisation with the provided id does not exists'
                    )
                    return RemoveInstanceMutation(errors=errors)

                except Exception as e:
                    errors.append(str(e))
                    return RemoveInstanceMutation(errors=errors)

            elif instance_type is 3:
                try:
                    client = Client.objects.get(pk=instance_id)
                    client.delete()
                except Client.DoesNotExist:
                    errors.append(
                        'Client with the provided id does not exists'
                    )
                    return RemoveInstanceMutation(errors=errors)
                except Exception as e:
                    errors.append(str(e))
                    return RemoveInstanceMutation(errors=errors)

            elif instance_type is 4:
                try:
                    Matter.objects.get(pk=instance_id).delete()
                except Matter.DoesNotExist:
                    errors.append(
                        'Matter with the provided id does not exists'
                    )
                    return RemoveInstanceMutation(errors=errors)

                except Exception as e:
                    errors.append(str(e))
                    return RemoveInstanceMutation(errors=errors)

            elif instance_type is 5:
                try:
                    time_entry = TimeEntry.objects.get(pk=instance_id)

                    if bool(time_entry.invoice):
                        raise PermissionError

                    time_entry.delete()
                except TimeEntry.DoesNotExist:
                    errors.append(
                        'TimeEntry with the provided id does not exist'
                    )
                    return RemoveInstanceMutation(errors=errors)
                except PermissionError:
                    errors.append(
                        'You can\'t delete a billed time entry!'
                    )
                    return RemoveInstanceMutation(errors=errors)

            elif instance_type is 6:
                try:
                    disbursement = TimeEntry.objects.get(pk=instance_id)

                    if bool(disbursement.invoice):
                        raise PermissionError

                    disbursement.delete()
                except TimeEntry.DoesNotExist:
                    errors.append(
                        'Disbursement with the provided id does not exist'
                    )
                    return RemoveInstanceMutation(errors=errors)
                except PermissionError:
                    errors.append(
                        'You can\'t delete a billed disbursement!'
                    )
                    return RemoveInstanceMutation(errors=errors)

            elif instance_type is 7:
                if info.context.user.has_perm('billing.delete_note'):
                    try:
                        note = Note.objects.get(pk=instance_id)
                        note.delete()
                    except Note.DoesNotExist:
                        errors.append(
                            'Note with the provided id does not exist'
                        )
                        return RemoveInstanceMutation(errors=errors)
                else:
                    errors.append(
                        'You do not have a permission to delete a note!'
                    )
                    return RemoveInstanceMutation(errors=errors)

            elif instance_type is 8:
                if info.context.user.has_perm('invoicing.delete_invoice'):
                    try:
                        invoice = Invoice.objects.get(pk=instance_id)

                        res = invoice.delete_in_xero()

                        if not res.get('success'):
                            errors.append(res.get('error'))
                            return RemoveInstanceMutation(errors=errors)

                        invoice.delete()

                    except Invoice.DoesNotExist:
                        errors.append('Invoice with the provided id does not exists')
                        return RemoveInstanceMutation(errors=errors)

                    except Exception as e:
                        errors.append('Failed to delete the invoice')
                        return RemoveInstanceMutation(errors=errors)

                else:
                    errors.append('You do not have a permission to delete an invoice!')
                    return RemoveInstanceMutation(errors=errors)

            elif instance_type is 9:
                if info.context.user.has_perm('invoicing.delete_payment'):
                    try:
                        Payment.objects.get(pk=instance_id).delete()
                    except Payment.DoesNotExist:
                        errors.append(
                            'Payment with the provided id does not exists'
                        )
                        return RemoveInstanceMutation(errors=errors)
                else:
                    errors.append(
                        'You do not have a permission to delete a payment!'
                    )
                    return RemoveInstanceMutation(errors=errors)

        return RemoveInstanceMutation(errors=errors)


class CreateDocument(graphene.Mutation):
    class Arguments:
        document = DocumentInput()

    errors = graphene.List(graphene.String)
    document = graphene.Field(lambda: DocumentType)

    @staticmethod
    @login_required
    def mutate(root, info, **args):
        errors = []
        section_id = args.get('document').section_id

        if section_id:
            section = Section.objects.get(pk=section_id)
        else:
            if Section.objects.exists():
                section_number = str(int(Section.objects.annotate(
                    section_number=Cast('number', FloatField())
                ).order_by('section_number').last().section_number + 1))
                section = Section.objects.create(
                    number=section_number,
                    office=Office.objects.first()
                )
            else:
                section = Section.objects.create(
                    number=1, office=Office.objects.first())

        document = Document(owner=info.context.user, section=section)
        document.update(exclude=['section_id'], **args.get('document'))
        document.save()

        return CreateDocument(errors=errors, document=document)


class UpdateDocument(graphene.Mutation):
    class Arguments:
        document = DocumentInput()

    errors = graphene.List(graphene.String)
    document = graphene.Field(lambda: DocumentType)

    @staticmethod
    @login_required
    def mutate(root, info, **args):
        errors = []
        data = args.get('document')

        try:
            document_id = from_global_id(data.document_id)[1]
            document = Document.objects.get(pk=document_id)
        except Document.DoesNotExist:
            errors.append("Document with the provided id does not exist")
            return UpdateDocument(errors=errors, document=document)

        document.update(**args.get('document'))
        document.save()

        return UpdateDocument(errors=errors, document=document)


class UpdateSection(graphene.Mutation):
    class Arguments:
        section_id = graphene.ID()
        office_id = graphene.ID()
        document_ids = graphene.List(graphene.ID)

    errors = graphene.List(graphene.String)
    section = graphene.Field(lambda: SectionType)

    @staticmethod
    @login_required
    def mutate(root, info, **args):
        errors = []
        section_id = args.get('section_id')
        office_id = args.get('office_id')
        document_ids = args.get('document_ids')
        section = None

        try:
            section = Section.objects.get(pk=section_id)
            section.office_id = office_id
            section.save()

            Document.objects.filter(id__in=document_ids).update(
                section_id=section_id
            )
        except Exception:
            errors.append("Unknown error has occurred")
            return UpdateSection(errors=errors, section=section)

        return UpdateSection(errors=errors, section=section)
