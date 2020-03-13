import graphene

from sitename.decorators import login_required
from gmailbox.models import GmailAccount
from graphql_relay.node.node import from_global_id

from .models import Mail
from .schema import MailType
from .utils import get_gmail_service

class ActivateGmailAccountMutation(graphene.Mutation):
    class Arguments:
        activation_data = graphene.String(required=True)

    errors = graphene.List(graphene.String)
    success = graphene.Field(graphene.Boolean)

    @staticmethod
    @login_required
    def mutate(root, info, **args):
        errors = []

        user = info.context.user
        activation_data = args.get('activation_data')

        try:
            service = get_gmail_service(activation_data)
            profile = service.users().getProfile(userId='me').execute()

            if not profile:
                errors.append('Invalid token')
                return ActivateGmailAccountMutation(errors=errors, success=False)

            address = profile['emailAddress']

            if hasattr(user, 'gmail_account'):
                user.gmail_account.token = activation_data
                user.gmail_account.address = address
                user.gmail_account.save()
            else:
                GmailAccount.objects.create(
                    user=user,
                    token=activation_data,
                    address=address,
                )

            return ActivateGmailAccountMutation(errors=errors, success=True)

        except Exception as e:
            print(str(e))
            errors.append('Failed to activate gmail')
            return ActivateGmailAccountMutation(errors=errors, success=False)


class DeactivateGmailAccountMutation(graphene.Mutation):
    errors = graphene.List(graphene.String)
    success = graphene.Field(graphene.Boolean)

    @staticmethod
    @login_required
    def mutate(root, info, **args):
        errors = []

        user = info.context.user

        print(user)

        try:
            gmail_account = user.gmail_account
            if gmail_account:
                gmail_account.delete()
            
            return DeactivateGmailAccountMutation(errors=errors, success=True)
        except Exception as e:
            print(str(e))
            errors.append('Failed to activate gmail')
            return DeactivateGmailAccountMutation(errors=errors, success=False)

class UpdateMailMatterMutation(graphene.Mutation):
    class Arguments:
        mail_id = graphene.ID(required=True)
        matter_id = graphene.String(required=True)

    errors = graphene.List(graphene.String)
    mail = graphene.Field(lambda: MailType)

    @staticmethod
    def mutate(root, info, **args):
        mail_id = from_global_id(args.get('mail_id'))[1]
        matter_id = args.get('matter_id')

        errors = []
        mail = None

        try:
            mail = Mail.objects.get(pk=mail_id)
            matter = from_global_id(matter_id)[1] if matter_id != 'no_matter' else None
            mail.matter_id = matter
            mail.save()
            return UpdateMailMatterMutation(errors=errors, mail=mail)

        except Mail.DoesNotExist:
            errors.append('Mail with the provided id does not exist')
            return UpdateMailMatterMutation(errors=errors, mail=None)

class UpdateMailsMatterMutation(graphene.Mutation):
    class Arguments:
        mails = graphene.List(graphene.ID)
        matter_id = graphene.String(required=True)

    errors = graphene.List(graphene.String)
    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, **args):
        mail_ids = [from_global_id(mail)[1] for mail in args.get('mails')]
        matter_id = args.get('matter_id')

        errors = []

        try:
            mails = Mail.objects.filter(id__in=mail_ids)
            matter = from_global_id(matter_id)[1] if matter_id != 'no_matter' else None

            print(matter)

            mails.update(matter=matter)
            return UpdateMailsMatterMutation(errors=errors, success=True)

        except Mail.DoesNotExist:
            errors.append('Mail with the provided id does not exist')
            return UpdateMailsMatterMutation(errors=errors, success=False)

class DeleteMailsMutation(graphene.Mutation):
    class Arguments:
        mails = graphene.List(graphene.ID)

    errors = graphene.List(graphene.String)
    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, **args):
        user = info.context.user
        errors = []
        mail_ids = [from_global_id(mail)[1] for mail in args.get('mails')]

        if not user.can_delete_mails:
            errors.append('User does not have permission to delete mails')
            return DeleteMailsMutation(errors=errors, success=False)

        try:
            Mail.objects.filter(id__in=mail_ids).delete()
            return DeleteMailsMutation(errors=errors, success=True)
        except Exception as e:
            print(str(e))
            errors.append('Failed to delete mails')
            return DeleteMailsMutation(errors=errors, success=False)

class HideMailMutation(graphene.Mutation):
    class Arguments:
        mail_id = graphene.ID(required=True)

    errors = graphene.List(graphene.String)

    @staticmethod
    def mutate(root, info, **args):
        mail_id = from_global_id(args.get('mail_id'))[1]
        errors = []

        try:
            mail = Mail.objects.get(pk=mail_id)
            mail.hidden = True
            mail.save()
            return HideMailMutation(errors=errors)

        except Mail.DoesNotExist:
            errors.append('Mail with the provided id does not exist')
            return HideMailMutation(errors=errors)
