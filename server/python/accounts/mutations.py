import base64
from decimal import Decimal

import graphene
from accounts.models import User
from sitename.decorators import login_required
from sitename.utils import obtain_jwt, get_xero_client
from core.models import Occupation
from django.contrib.auth.tokens import default_token_generator
from django.core.files.base import ContentFile
from gmailbox.models import GmailAccount
from gmailbox.utils import get_user_mails
from graphql_relay.node.node import from_global_id, to_global_id
from dateutil import parser

from .inputs import (ClientInput, ContactInput, OrganisationInput,
                     RelationshipInput, UserInput)
from .models import Client, Contact, Location, Organisation
from .schema import (ClientType, ContactType, LocationType, OrganisationType,
                     PostalLocationType, UserType)
from .tasks import (reset_password_email, update_xero_contact, create_all_contacts_in_xero, get_user_mails_task)


class ResetPassword(graphene.Mutation):
    class Arguments:
        uid = graphene.ID(required=True)
        new_password = graphene.String(required=True)

    error = graphene.String()

    @staticmethod
    def mutate(root, info, uid, new_password):
        error = ''

        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            error = 'User cannot be find!'
            return ResetPassword(error=error)

        user.set_password(new_password)
        user.save()

        return ResetPassword(error=error)


class CheckResetPasswordToken(graphene.Mutation):
    class Arguments:
        token = graphene.String(required=True)
        uid = graphene.ID(required=True)

    error = graphene.String()

    @staticmethod
    def mutate(root, info, uid, token):
        error = ''
        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            error = 'User cannot be find!'
            return CheckResetPasswordToken(error=error)

        if not default_token_generator.check_token(user, token):
            error = 'Invalid token!'

        return CheckResetPasswordToken(error=error)


class SendResetPasswordEmail(graphene.Mutation):
    class Arguments:
        email = graphene.String()

    error = graphene.String()

    @staticmethod
    def mutate(root, info, email):
        error = ''

        if User.objects.filter(email=email).exists():
            reset_password_email.delay(email)
        else:
            error = 'Cannot find user with the provided email!'
            return SendResetPasswordEmail(error=error)

        return SendResetPasswordEmail(error=error)


class UpdateLocationMixin(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        address1 = graphene.String()
        address2 = graphene.String()
        suburb = graphene.String()
        state = graphene.Int()
        post_code = graphene.String()
        country = graphene.String()
        postal_address1 = graphene.String()
        postal_address2 = graphene.String()
        postal_suburb = graphene.String()
        postal_state = graphene.Int()
        postal_post_code = graphene.String()
        postal_country = graphene.String()
        addresses_are_equals = graphene.Boolean()

    errors = graphene.List(graphene.String)
    location = graphene.Field(lambda: LocationType)
    postal_location = graphene.Field(lambda: PostalLocationType)

    @staticmethod
    def mutate(root, info, **args):
        id = args.get('id')
        errors = []

        if not id:
            errors.append('Instance id must be specified')

        return errors


class UpdateRelationshipsMutation(graphene.Mutation):
    class Arguments:
        relationship = RelationshipInput()

    errors = graphene.List(graphene.String)
    contact = graphene.Field(lambda: ContactType)
    referrer = graphene.Field(lambda: ContactType)
    spouse = graphene.Field(lambda: ContactType)
    mother = graphene.Field(lambda: ContactType)
    father = graphene.Field(lambda: ContactType)

    @staticmethod
    @login_required
    def mutate(root, info, **args):
        relationship = args.get('relationship')
        errors = []
        contact = None
        referrer = None
        spouse = None
        mother = None
        father = None

        if not relationship.contact_id:
            errors.append('Contact id must be specified')

        if not errors:
            contact_id = from_global_id(relationship.contact_id)[1]
            try:
                contact = Contact.objects.get(pk=contact_id)
            except Contact.DoesNotExist:
                errors.append('Contact with the provided id does not exist')
                return UpdateRelationshipsMutation(
                    errors=errors,
                    contact=None,
                    referrer=None,
                    spouse=None,
                    mother=None,
                    father=None,
                )

            if relationship.referrer_id:
                referrer_id = from_global_id(relationship.referrer_id)[1]
                try:
                    referrer = Contact.objects.get(pk=referrer_id)

                    contact.referrer = referrer
                except Contact.DoesNotExist:
                    errors.append(
                        'Contact with the provided id does not exist')
                    return UpdateRelationshipsMutation(
                        errors=errors,
                        contact=None,
                        referrer=None,
                        spouse=None,
                        mother=None,
                        father=None,
                    )
            elif contact.referrer and not relationship.referrer_id:
                contact.referrer = None

            if relationship.spouse_id:
                spouse_id = from_global_id(relationship.spouse_id)[1]
                try:
                    spouse = Contact.objects.get(pk=spouse_id)

                    contact.set_spouse(spouse.id)
                    spouse.set_spouse(contact.id)
                except Contact.DoesNotExist:
                    errors.append(
                        'Contact with the provided id does not exist')
                    return UpdateRelationshipsMutation(
                        errors=errors,
                        contact=None,
                        referrer=None,
                        spouse=None,
                        mother=None,
                        father=None,
                    )
            elif contact.get_spouse() and not relationship.spouse_id:
                contact.remove_spouse()

            if relationship.mother_id:
                mother_id = from_global_id(relationship.mother_id)[1]
                try:
                    mother = Contact.objects.get(pk=mother_id)

                    contact.mother = mother
                except Contact.DoesNotExist:
                    errors.append(
                        'Contact with the provided id does not exist')
                    return UpdateRelationshipsMutation(
                        errors=errors,
                        contact=None,
                        referrer=None,
                        spouse=None,
                        mother=None,
                        father=None,
                    )

            elif contact.mother and not relationship.mother_id:
                contact.mother = None

            if relationship.father_id:
                father_id = from_global_id(relationship.father_id)[1]
                try:
                    father = Contact.objects.get(pk=father_id)

                    contact.father = father
                except Contact.DoesNotExist:
                    errors.append(
                        'Contact with the provided id does not exist')
                    return UpdateRelationshipsMutation(
                        errors=errors,
                        contact=None,
                        referrer=None,
                        spouse=None,
                        mother=None,
                        father=None,
                    )

            elif contact.father and not relationship.father_id:
                contact.father = None

            contact.save()

        return UpdateRelationshipsMutation(
            errors=errors,
            contact=contact,
            referrer=referrer,
            spouse=spouse,
            mother=mother,
            father=father,
        )


class UpdateOrganisationLocationMutation(UpdateLocationMixin):
    @staticmethod
    @login_required
    def mutate(root, info, **args):
        errors = UpdateLocationMixin.mutate(root, info, **args)
        addresses_are_equals = args.get('addresses_are_equals', False)
        location = None
        postal_location = None

        if not errors:
            organisation_id = from_global_id(args.get('id'))[1]
            try:
                organisation = Organisation.objects.get(pk=organisation_id)
            except Organisation.DoesNotExist:
                errors.append(
                    'Organisation with the provided id does not exist')
                return UpdateOrganisationLocationMutation(
                    errors=errors,
                    location=location,
                    postal_location=postal_location
                )

            if organisation.location:
                organisation.location.address1 = args.get('address1')
                organisation.location.address2 = args.get('address2')
                organisation.location.suburb = args.get('suburb')
                organisation.location.state = args.get('state')
                organisation.location.post_code = args.get('post_code')
                organisation.location.country = args.get('country')
                organisation.location.save()
            else:
                location = Location.objects.create(
                    address1=args.get('address1'),
                    address2=args.get('address2'),
                    suburb=args.get('suburb'),
                    state=args.get('state'),
                    post_code=args.get('post_code'),
                    country=args.get('country'),
                )
                organisation.location = location

            if addresses_are_equals:
                organisation.postal_location = organisation.location
            else:
                postal_location = Location.objects.create(
                    address1=args.get('postal_address1'),
                    address2=args.get('postal_address2'),
                    suburb=args.get('postal_suburb'),
                    state=args.get('postal_state'),
                    post_code=args.get('postal_post_code'),
                    country=args.get('postal_country'),
                )
                organisation.postal_location = postal_location

            for client in Client.objects.filter(organisation=organisation):
                update_xero_contact.delay(client.id)

            organisation.save()

        return UpdateOrganisationLocationMutation(
            errors=errors,
            location=location,
            postal_location=postal_location
        )


class UpdateOrganisationsMutation(graphene.Mutation):
    class Arguments:
        contact_id = graphene.ID()
        organisations = graphene.List(graphene.ID)

    errors = graphene.List(graphene.String)
    contact = graphene.Field(lambda: ContactType)

    @staticmethod
    @login_required
    def mutate(root, info, **args):
        contact_id = args.get('contact_id')
        new_organisations = args.get('organisations')
        contact = None
        errors = []

        if not contact_id:
            errors.append('Contact id must be specified')

        if not errors:
            # from relay global id to Django model id
            contact_id = from_global_id(contact_id)[1]
            new_organisations = [from_global_id(
                gid)[1] for gid in new_organisations]

            try:
                contact = Contact.objects.get(pk=contact_id)
            except Contact.DoesNotExist:
                errors.append('Contact with the provided id does not exist')
                return UpdateOrganisationsMutation(errors=errors, contact=None)

            existing_organisations = [
                str(org.id) for org in contact.organisations.all()
            ]

            difference = set(existing_organisations) ^ set(new_organisations)

            if difference <= set(existing_organisations):
                for pk in list(difference):
                    try:
                        Client.objects.get(
                            contact=contact,
                            organisation_id=pk
                        ).delete()
                    except Client.DoesNotExist:
                        pass

                    except Exception:
                        errors.append(to_global_id('OrganisationType', pk))

                if errors:
                    errors.append(
                        'Some Clients cannot be deleted because\
                         they have a Matter assigned to them'
                    )
                    return UpdateOrganisationsMutation(
                        errors=errors,
                        contact=contact
                    )

                contact.organisations.remove(*list(difference))
            else:
                contact.organisations.add(*list(difference))

                for pk in list(difference):
                    Client.objects.get_or_create(
                        contact=contact,
                        organisation_id=pk
                    )

            clients = Client.objects.filter(contact_id=contact_id)

            for client in clients:
                update_xero_contact.delay(client.id)

        return UpdateOrganisationsMutation(errors=errors, contact=contact)


class UpdateOrganisationAssociation(graphene.Mutation):
    class Arguments:
        organisation_id = graphene.ID()
        contacts = graphene.List(graphene.ID)

    errors = graphene.List(graphene.String)
    organisation = graphene.Field(lambda: OrganisationType)

    @staticmethod
    @login_required
    def mutate(root, info, **args):
        organisation_id = args.get('organisation_id')
        new_contacts = args.get('contacts')
        errors = []

        if not organisation_id:
            errors.append('Organisation id must be specified')

        if not errors:
            organisation_id = from_global_id(organisation_id)[1]
            try:
                organisation = Organisation.objects.get(pk=organisation_id)
            except Organisation.DoesNotExist:
                errors.append(
                    'Organisation with the provided id does not exist')
                return UpdateOrganisationAssociation(
                    errors=errors,
                    organisation=None,
                )

            new_contacts = [int(from_global_id(pk)[1]) for pk in new_contacts]

            existing_contacts = organisation.contacts.values_list(
                'id', flat=True)

            difference = set(existing_contacts) ^ set(new_contacts)

            if difference <= set(existing_contacts):
                for pk in list(difference):
                    try:
                        Client.objects.get(
                            organisation=organisation,
                            contact_id=pk
                        ).delete()
                    except Client.DoesNotExist:
                        pass

                    except Exception:
                        errors.append(pk)

                if errors:
                    errors.append(
                        'Some Clients cannot be deleted because\
                         they have a Matter assigned to them'
                    )
                    return UpdateOrganisationAssociation(
                        errors=errors,
                        organisation=organisation
                    )

                organisation.contacts.remove(*list(difference))
            else:
                organisation.contacts.add(*list(difference))

                for pk in list(difference):
                    Client.objects.create(
                        organisation=organisation, contact_id=pk)

        return UpdateOrganisationAssociation(
            errors=errors,
            organisation=organisation
        )


class LoginMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        remember_me = graphene.Boolean()

    token = graphene.String()
    errors = graphene.List(graphene.String)
    user = graphene.Field(lambda: UserType)

    @staticmethod
    def mutate(root, info, **args):
        email = args.get('email')
        password = args.get('password')
        errors = []
        user = None
        token = None

        if not errors:
            try:
                user = User.objects.get(email=email)
                if not user.check_password(password):
                    errors.append("Email or password is invalid")
                    user = None
                else:
                    if args.get('remember_me'):
                        token = obtain_jwt(user.id, forever=True)
                    else:
                        token = obtain_jwt(user.id, forever=False)
            except User.DoesNotExist:
                errors.append("Email or password is invalid")

        return LoginMutation(token=token, errors=errors, user=user)


class RegisterMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String()
        password = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()

    errors = graphene.List(graphene.String)

    @staticmethod
    def mutate(root, info, **args):
        email = args.get('email')
        first_name = args.get('first_name')
        last_name = args.get('last_name')
        password = args.get('password')
        errors = []

        if not email:
            errors.append("Email must be specified")
        elif User.objects.filter(email=email).exists():
            errors.append("User with the email already exists!")

        if not password:
            errors.append("Password must be specified")

        if not first_name:
            errors.append('First name must be specified')

        if not last_name:
            errors.append('Last name must be specified')

        if not errors:
            user = User.objects.create(**args)
            user.set_password(password)
            user.save()

        return RegisterMutation(errors=errors)


class CreateContactMutation(graphene.Mutation):
    class Arguments:
        contact_data = ContactInput()

    errors = graphene.List(graphene.String)
    contact = graphene.Field(ContactType)

    @staticmethod
    @login_required
    def mutate(root, info, **args):
        contact_data = args.get('contact_data')
        errors = []
        contact = None

        if not contact_data.email:
            # errors.append("Email must be specified")
            pass
        elif Contact.objects.filter(email=contact_data.email).exists():
            errors.append("The email already exists")

        if not contact_data.first_name:
            errors.append('First name must be specified')

        if not contact_data.last_name:
            errors.append('Last name must be specified')

        if not contact_data.mobile:
            # errors.append("Mobile number must be specified")
            pass

        if not errors:
            contact = Contact()
            contact.update(
                exclude=[
                    'postal_location',
                    'location',
                    'organisations',
                    'occupation',
                    'place_of_birth',
                    'date_of_birth',
                    'date_of_death'
                ],
                **contact_data
            )
            if contact_data.date_of_birth:
                contact.date_of_birth = parser.parse(
                    contact_data.date_of_birth)
            if contact_data.date_of_death:
                contact.date_of_death = parser.parse(
                    contact_data.date_of_death)
            if contact_data.place_of_birth:
                contact.place_of_birth = contact_data.place_of_birth
            if contact_data.occupation:
                occupation = Occupation.objects.get(
                    pk=contact_data.occupation)
                contact.occupation = occupation

            if contact_data.location:
                contact.location = Location.objects.create(
                    **contact_data.location)

            if contact_data.postal_location:
                contact.postal_location = Location.objects.create(
                    **contact_data.location)

            if contact_data.spouse_id:
                try:
                    spouse_id = from_global_id(contact_data.spouse_id)[1]
                    spouse = Contact.objects.get(pk=spouse_id)
                    contact.set_spouse(spouse.id)
                    spouse.set_spouse(contact.id)
                except Contact.DoesNotExist:
                    errors.append('Can\'t find spouse with provided id')
                    return CreateContactMutation(
                        errors=errors,
                        contact=contact
                    )

            if contact_data.mother_id:
                try:
                    mother_id = from_global_id(contact_data.mother_id)[1]
                    mother = Contact.objects.get(pk=mother_id)
                    contact.mother = mother
                except Contact.DoesNotExist:
                    errors.append('Can\'t find mother with provided id')
                    return CreateContactMutation(
                        errors=errors,
                        contact=contact
                    )

            if contact_data.father_id:
                try:
                    father_id = from_global_id(contact_data.father_id)[1]
                    father = Contact.objects.get(pk=father_id)
                    contact.father = father
                except Contact.DoesNotExist:
                    errors.append('Can\'t find father with provided id')
                    return CreateContactMutation(
                        errors=errors,
                        contact=contact
                    )

            for pk in contact_data.organisations:
                organisation_id = from_global_id(pk)[1]
                contact.organisations.add(organisation_id)
                Client.objects.create(
                    contact=contact, organisation_id=organisation_id)

            if contact_data.referrer_id:
                referer_id = from_global_id(contact_data.referrer_id)[1]
                contact.referrer_id = referer_id

            contact.save()

        return CreateContactMutation(errors=errors, contact=contact)


class UpdateContactMutation(graphene.Mutation):
    class Arguments:
        contact_id = graphene.ID()
        contact_data = ContactInput()

    errors = graphene.List(graphene.String)
    contact = graphene.Field(ContactType)

    @staticmethod
    @login_required
    def mutate(root, info, **args):
        contact_data = args.get('contact_data')
        contact_id = args.get('contact_id')
        errors = []
        contact = None

        if not contact_id:
            errors.append("Contact id must be specified")

        if contact_data.link_mails and not info.context.user.can_link_mails:
            errors.append('User does not have permission to hide or show mails')

        if not errors:
            contact_id = from_global_id(contact_id)[1]
            try:
                contact = Contact.objects.get(pk=contact_id)

                contact.update(
                    exclude=[
                        'postal_location',
                        'location',
                        'contact_id',
                        'organisations',
                        'occupation',
                        'place_of_birth',
                        'date_of_birth',
                        'date_of_death'
                    ],
                    **contact_data
                )
                if contact_data.date_of_birth:
                    contact.date_of_birth = parser.parse(
                        contact_data.date_of_birth)
                if contact_data.date_of_death:
                    contact.date_of_death = parser.parse(
                        contact_data.date_of_death)
                if contact_data.place_of_birth:
                    contact.place_of_birth = contact_data.place_of_birth
                if contact_data.occupation:
                    occupation = Occupation.objects.get(
                        pk=contact_data.occupation)
                    contact.occupation = occupation

                if contact_data.organisations:
                    contact.organisations.set(
                        [from_global_id(o)[1] for o in contact_data.organisations])

                if contact_data.location:
                    if contact.location:
                        contact.location.update(**contact_data.location)
                        contact.location.save()
                    else:
                        contact.location = Location.objects.create(
                            **contact_data.location)

                if contact_data.postal_location:
                    if contact.postal_location:
                        contact.postal_location.update(
                            **contact_data.postal_location)
                        contact.postal_location.save()
                    else:
                        contact.postal_location = Location.objects.create(
                            **contact_data.postal_location
                        )

                contact.save()

                clients = Client.objects.filter(contact_id=contact.id)

                for client in clients:
                    update_xero_contact.delay(client.id)

            except Contact.DoesNotExist:
                errors.append('User with the specified id does not exist')
                return UpdateContactMutation(errors=errors, contact=None)
        return UpdateContactMutation(errors=errors, contact=contact)


class CreateOrganisationMutation(graphene.Mutation):
    class Arguments:
        organisation_data = OrganisationInput()

    errors = graphene.List(graphene.String)
    organisation = graphene.Field(lambda: OrganisationType)

    @staticmethod
    @login_required
    def mutate(root, info, **args):
        organisation_data = args.get('organisation_data')
        errors = []
        organisation = None

        if not errors:
            if organisation_data.contacts:
                contacts = [from_global_id(pk)[1]
                            for pk in organisation_data.contacts]
            else:
                contacts = []

            organisation = Organisation()
            organisation.update(
                exclude=[
                    'postal_location',
                    'location',
                    'group_parent',
                    'contacts'
                ],
                **organisation_data
            )

            if organisation_data.location:
                organisation.location = Location.objects.create(
                    **organisation_data.location)

            if organisation_data.postal_location:
                organisation.postal_location = Location.objects.create(
                    **organisation_data.postal_location)

            if organisation_data.group_parent:
                if organisation_data.group_parent.id:
                    group_parent_id = from_global_id(
                        organisation_data.group_parent.id)[1]
                    organisation.group_parent = Organisation.objects.get(
                        pk=group_parent_id
                    )
                else:
                    organisation.group_parent = organisation

            organisation.save()
            organisation.contacts.set(contacts)

            for pk in contacts:
                Client.objects.create(
                    organisation=organisation, contact_id=pk)

            clients = Client.objects.filter(contact_id__in=contacts)

            for client in clients:
                update_xero_contact.delay(client.id)

        return CreateOrganisationMutation(
            errors=errors,
            organisation=organisation
        )


class UpdateOrganisationDetailsMutation(graphene.Mutation):
    class Arguments:
        organisation_id = graphene.ID()
        organisation_data = OrganisationInput()

    errors = graphene.List(graphene.String)
    organisation = graphene.Field(lambda: OrganisationType)

    @staticmethod
    @login_required
    def mutate(root, info, **args):
        organisation_id = args.get('organisation_id')
        organisation_data = args.get('organisation_data')
        errors = []
        organisation = None
        user = info.context.user

        if not organisation_id:
            errors.append('Organisation id must be specified')

        if not organisation_data.name:
            errors.append('Organisation name must be specified')

        if organisation_data.link_mails and not user.can_link_mails:
            errors.append('User does not have permission to hide or show mails')

        if not errors:
            organisation_id = from_global_id(organisation_id)[1]
            try:
                organisation = Organisation.objects.get(pk=organisation_id)
            except Organisation.DoesNotExist:
                return UpdateOrganisationDetailsMutation(
                    errors=errors,
                    organisation=None
                )

            organisation.update(
                exclude=[
                    'contacts',
                    'location',
                    'postal_location',
                    'main_line'
                    ],
                **organisation_data
            )

            if organisation_data.main_line:
                organisation.main_line = organisation_data.main_line

            if organisation_data.contacts:
                contacts = [from_global_id(pk)[1]
                            for pk in organisation_data.contacts]
            else:
                contacts = []

            organisation.contacts.set(contacts)

            for pk in contacts:
                client = Client.objects.filter(
                    organisation=organisation, contact_id=pk)
                if not client.exists():
                    Client.objects.create(
                        organisation=organisation, contact_id=pk)

            organisation.save()

            clients = Client.objects.filter(contact_id__in=contacts)

            for client in clients:
                update_xero_contact.delay(client.id)

        return UpdateOrganisationDetailsMutation(
            errors=errors,
            organisation=organisation
        )


class UpdateUserMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        user_data = UserInput()

    errors = graphene.List(graphene.String)
    user = graphene.Field(lambda: UserType)

    @staticmethod
    @login_required
    def mutate(root, info, **args):
        user_id = from_global_id(args.get('user_id'))[1]
        user_data = args.get('user_data')
        errors = []
        user = None

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            errors.append('User with the provided id does not exist')
            return UpdateUserMutation(errors=errors, user=user)

        user.update(
            exclude=['rate', 'photo', 'location', 'postal_location'],
            **user_data
        )

        if user_data.location:
            if user.location:
                user.location.update(**user_data.location)
                user.location.save()
            else:
                user.location = Location.objects.create(**user_data.location)

        if user_data.postal_location:
            if user.postal_location:
                user.postal_location.update(**user_data.postal_location)
                user.postal_location.save()
            else:
                user.postal_location = Location.objects.create(
                    **user_data.postal_location
                )

        if user_data.photo:
            img_format, img_str = user_data.photo.split(';base64,')
            ext = img_format.split('/')[-1]
            photo = ContentFile(base64.b64decode(
                img_str), name=str(user.id) + ext)

            user.photo = photo

        user.rate = Decimal(user_data.rate or 0)
        user.save()

        return UpdateUserMutation(errors=errors, user=user)


class UpdateClientDetails(graphene.Mutation):
    class Arguments:
        client_data = ClientInput()

    errors = graphene.List(graphene.String)
    client = graphene.Field(lambda: ClientType)

    @staticmethod
    def mutate(root, info, **args):
        client_data = args.get('client_data')
        errors = []
        client = None
        organisation = None

        if not client_data.id:
            errors.append('Client id must be specified')
        if not errors:
            # convert from Relay global id to Django model id
            client_id = from_global_id(client_data.id)[1]

            try:
                client = Client.objects.get(pk=client_id)
            except Client.DoesNotExist:
                errors.append('Client with the provided id does not exist')
                return UpdateClientDetails(errors=errors, client=client)

            try:
                # convert from Relay global id to Django model id
                contact_id = from_global_id(client_data.contact['id'])[1]

                contact = Contact.objects.get(pk=contact_id)
            except Contact.DoesNotExist:
                errors.append('Contact with the provided id does not exist')
                return UpdateClientDetails(errors=errors, client=client)

            # convert from Relay global id to Django model id
            organisation_id = from_global_id(
                client_data.organisation.id)[1]

            if organisation_id and organisation_id != '-1':
                try:
                    organisation = Organisation.objects.get(
                        pk=organisation_id)

                    organisation.main_line = client_data.organisation.main_line
                    organisation.website = client_data.organisation.website
                    organisation.save()
                    client.organisation = organisation
                except Organisation.DoesNotExist:
                    errors.append(
                        'Organisation with the provided id does not exist'
                    )
                    return UpdateClientDetails(errors=errors, client=client)
            else:
                client.organisation = None

            if client_data.second_contact:
                try:
                    # convert from Relay global id to Django model id
                    second_contact_id = from_global_id(
                        client_data.second_contact.get('id'))[1]

                    second_contact = Contact.objects.get(pk=second_contact_id)

                    second_contact.mobile = client_data.second_contact.mobile
                    second_contact.role = client_data.second_contact.role
                    second_contact.save()
                    if organisation is not None:
                        second_contact.organisations.add(organisation)
                except Contact.DoesNotExist:
                    errors.append(
                        'Contact with the provided id does not exist'
                    )
                    return UpdateClientDetails(errors=errors, client=client)
                except Exception:
                    second_contact = None
            else:
                second_contact = None
            client.contact = contact
            client.contact.role = client_data.contact.role
            client.contact.mobile = client_data.contact.mobile
            client.is_active = client_data.is_active
            client.office_id = client_data.office['id']
            client.contact.save()
            client.second_contact = second_contact
            client.save()

            update_xero_contact.delay(client.id)

        return UpdateClientDetails(errors=errors, client=client)


class CreateClientMutation(graphene.Mutation):
    class Arguments:
        client_data = ClientInput()

    errors = graphene.List(graphene.String)
    client = graphene.Field(lambda: ClientType)

    @staticmethod
    def mutate(root, info, **args):
        errors = []
        client_data = args.get('client_data')
        client = None

        if not client_data.contact.id:
            errors.append('Contact id must be specified')

        if not errors:
            client = Client()

            try:
                # convert from Relay global id to Django model id
                contact_id = from_global_id(client_data.contact.id)[1]

                contact = Contact.objects.get(pk=contact_id)
            except Contact.DoesNotExist:
                errors.append('Contact with the provided id does not exist')
                return UpdateClientDetails(errors=errors, client=client)

            if client_data.organisation:
                try:
                    # convert from Relay global id to Django model id
                    organisation_id = from_global_id(
                        client_data.organisation.id)[1]

                    organisation = Organisation.objects.get(pk=organisation_id)

                    organisation.main_line = client_data.organisation.main_line
                    organisation.website = client_data.organisation.website
                    organisation.save()
                    client.organisation = organisation
                    contact.organisations.add(organisation)
                except Organisation.DoesNotExist:
                    organisation = None

            if client_data.second_contact:
                try:
                    # convert from Relay global id to Django model id
                    contact_id = from_global_id(
                        client_data.second_contact.id)[1]

                    second_contact = Contact.objects.get(
                        pk=contact_id)
                    second_contact.mobile = client_data.second_contact.mobile
                    second_contact.role = client_data.second_contact.role
                    client.second_contact = second_contact
                    client.second_contact.save()
                    if client_data.organisation:
                        second_contact.organisations.add(organisation)
                except Contact.DoesNotExist:
                    second_contact = None

            client.contact = contact
            client.contact.role = client_data.contact.role
            client.contact.mobile = client_data.contact.mobile
            client.is_active = client_data.is_active
            client.office_id = client_data.office.id
            client.contact.save()
            client.save()

            update_xero_contact.delay(client.id)

        return CreateClientMutation(errors=errors, client=client)


class CreateAllContactsInXeroMutation(graphene.Mutation):
    errors = graphene.List(graphene.String)
    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, **args):
        try:
            create_all_contacts_in_xero.delay()
        except Exception as e:
            errors.append('Failed to create contacts in Xero')
            return CreateAllContactsInXeroMutation(errors=errors, success=False)

        return CreateAllContactsInXeroMutation(success=True)

class SyncMailsMutation(graphene.Mutation):
    errors = graphene.List(graphene.String)
    success = graphene.Boolean()

    @staticmethod
    @login_required
    def mutate(root, info, **args):
        errors = []

        user = info.context.user

        try:
            get_user_mails_task.delay(user.id)
            return SyncMailsMutation(errors=errors, success=True)
        except Exception as e:
            print(str(e))
            errors.append('Failed to start downloading mails')
            return SyncMailsMutation(errors=errors, success=False)

        return SyncMailsMutation(success=True)
