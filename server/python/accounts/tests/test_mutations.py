import pytest
from unittest.mock import patch

from django.contrib.auth.tokens import default_token_generator
from sitename.schema import schema
from billing.factories import MatterFactory, EntryTypeFactory
from core.factories import OccupationFactory, OfficeFactory, LeadStatusFactory
from graphene.test import Client
from graphql_relay.node.node import to_global_id
from billing.factories import MatterFactory
from ..factories import (ClientFactory, ContactFactory, LocationFactory,
                         OrganisationFactory, UserFactory)


@pytest.mark.django_db
def test_login_mutation(snapshot):
    """ Test success login mutation """
    user = UserFactory()
    user.set_password('qwe')
    user.save()

    client = Client(schema)
    executed = client.execute("""
        mutation login ($email: String!, $password: String!) {
            login (email: $email, password: $password) {
                errors
                user {
                    firstName
                    lastName
                }
            }
        }
    """, variable_values={'email': user.email, 'password': 'qwe'})

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_reset_password(snapshot):
    """ Test reset password mutation """
    user = UserFactory()

    client = Client(schema)
    executed = client.execute("""
        mutation resetPassword($uid: ID!, $newPassword: String!) {
            resetPassword(uid: $uid, newPassword: $newPassword) {
              error
            }
        }
    """, variable_values={'uid': user.id, 'newPassword': 'qwe'})

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_reset_password_with_no_exist_user(snapshot):
    """ Test reset password mutation with not exist user"""
    user = UserFactory()

    client = Client(schema)
    executed = client.execute("""
        mutation resetPassword($uid: ID!, $newPassword: String!) {
            resetPassword(uid: $uid, newPassword: $newPassword) {
              error
            }
        }
    """, variable_values={'uid': user.id+999, 'newPassword': 'qwe'})

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_check_reset_password(snapshot):
    """ Test success check reset password mutation """
    user = UserFactory()
    token = default_token_generator.make_token(user)

    client = Client(schema)
    executed = client.execute("""
        mutation checkResetPasswordToken($uid: ID!, $token: String!) {
            checkResetPasswordToken(uid: $uid, token: $token) {
                error
            }
      }
    """, variable_values={'uid': user.id, 'token': token})

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_check_reset_password_with_incorrect_token(snapshot):
    """ Test success check reset password mutation """
    user = UserFactory()
    default_token_generator.make_token(user)

    client = Client(schema)
    executed = client.execute("""
        mutation checkResetPasswordToken($uid: ID!, $token: String!) {
            checkResetPasswordToken(uid: $uid, token: $token) {
                error
            }
      }
    """, variable_values={'uid': user.id, 'token': 'failtokenforuser'})

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_check_reset_password_with_no_exist_user(snapshot):
    """ Test success check reset password mutation """
    user = UserFactory()
    token = default_token_generator.make_token(user)

    client = Client(schema)
    executed = client.execute("""
        mutation checkResetPasswordToken($uid: ID!, $token: String!) {
            checkResetPasswordToken(uid: $uid, token: $token) {
                error
            }
      }
    """, variable_values={'uid': user.id+666, 'token': token})

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_send_reset_password_email(snapshot):
    """ Test a success send reset password email mutation """
    user = UserFactory()
    user.email = 'user@email.com'
    user.save()

    client = Client(schema)
    reset_email_patch = patch('accounts.mutations.reset_password_email.delay')

    with reset_email_patch as mock_reset_email:
        executed = client.execute("""
            mutation sendResetPasswordEmail($email: String!) {
                sendResetPasswordEmail(email: $email) {
                        error
                }
          }
        """, variable_values={'email': user.email})

        mock_reset_email.assert_called_once_with(user.email)

        snapshot.assert_match(executed)


@pytest.mark.django_db
def test_send_reset_password_email_with_incorrect_email(snapshot):
    """ Test a failure send reset password email with incorrect email """

    client = Client(schema)
    executed = client.execute("""
        mutation sendResetPasswordEmail($email: String!) {
            sendResetPasswordEmail(email: $email) {
                    error
            }
      }
    """, variable_values={'email': 'incorrect@email.com'})

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_login_mutation_with_incorrect_password(snapshot):
    """ Test a login with incorrect password """

    user = UserFactory()
    client = Client(schema)

    executed = client.execute('''
        mutation login ($email: String!, $password: String!) {
            login (email: $email, password: $password) {
                errors
            }
        }
    ''', variable_values={'email': user.email, 'password': '123'})

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_login_mutation_with_incorrect_email(snapshot):
    """ Test a login with incorrect email """

    client = Client(schema)

    executed = client.execute('''
        mutation login ($email: String!, $password: String!) {
            login (email: $email, password: $password) {
                errors
            }
        }
    ''', variable_values={'email': 'wrong@email.com', 'password': 'wrong'})

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_login_mutation_with_remember_me_flag(snapshot):
    """ Test a login with remember me flag """

    user = UserFactory()
    user.set_password('qwe')
    user.save()
    remember_me = 'true'

    client = Client(schema)
    executed = client.execute('''
        mutation login ($email: String!, $password: String!, $rememberMe: Boolean!) {
            login (email: $email, password: $password, rememberMe: $rememberMe) {
                errors
            }
        }
    ''', variable_values={
            'email': user.email,
            'password': 'qwe',
            'rememberMe': remember_me,
        })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_register_mutation(snapshot):
    """ Test a success register mutation """

    user = UserFactory.build()
    user_password = 'qwe'
    client = Client(schema)

    executed = client.execute('''
        mutation register ($email: String!, $password: String!, $firstName: String!, $lastName: String!) {
            register (email: $email, password: $password, firstName: $firstName, lastName: $lastName) {
                errors
            }
        }
    ''', variable_values={'email': user.email, 'password': user_password, 'firstName': user.first_name, 'lastName': user.last_name})

    assert UserFactory(email=user.email)
    assert UserFactory(email=user.email).check_password(user_password)
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_register_mutation_without_data(snapshot):
    """ Test a register failure mutation because of no existing data """

    user = UserFactory.build()
    user_password = 'qwe'
    client = Client(schema)

    executed = client.execute('''
        mutation register ($email: String!, $password: String!, $firstName: String!, $lastName: String!) {
            register (email: $email, password: $password, firstName: $firstName, lastName: $lastName) {
                errors
            }
        }
    ''', variable_values={'email': '', 'password': '', 'firstName': '', 'lastName': ''})

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_register_mutation_with_existing_user(snapshot):
    """ Test a register failure mutation because of existing user """

    user = UserFactory()
    client = Client(schema)

    executed = client.execute('''
        mutation register ($email: String!, $password: String!, $firstName: String!, $lastName: String!) {
            register (email: $email, password: $password, firstName: $firstName, lastName: $lastName) {
                errors
            }
        }
    ''', variable_values={'email': user.email, 'password': 'qwe', 'firstName': user.first_name, 'lastName': user.last_name})

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_profile_mutation_without_init_data(snapshot):
    """ Test a success update mutation without init data on the profile """

    user = UserFactory()

    user_id = to_global_id('UserType', user.id)
    new_first_name = 'BobGuyForTest'
    new_email = "BobGuyForTest@gmail.com"
    new_location = LocationFactory()
    new_postal_location = LocationFactory()

    client = Client(schema)

    executed = client.execute('''
        mutation updateUser ($userId: ID!, $userData: UserInput!) {
            updateUser (userId: $userId, userData: $userData) {
                errors
                user {
                    email
                    firstName
                    location {
                        address1
                        address2
                    }
                    postalLocation {
                        address1
                        address2
                    }
                }
            }
        }
    ''', variable_values={
        'userId': user_id,
        'userData': {
            'email': new_email,
            'firstName': new_first_name,
            'location': {
                'address1': new_location.address1,
                'address2': new_location.address2,
            },
            'postalLocation': {
                'address1': new_postal_location.address1,
                'address2': new_postal_location.address2,
            },
        }
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_profile_mutation_with_init_data(snapshot):
    """ Test a success update mutation with init data on the profile """

    user = UserFactory()
    user.location = LocationFactory()
    user.postal_location = LocationFactory()
    user.save()
    new_location = LocationFactory()
    user_id = to_global_id('UserType', user.id)

    client = Client(schema)

    executed = client.execute('''
        mutation updateUser ($userId: ID!, $userData: UserInput!) {
            updateUser (userId: $userId, userData: $userData) {
                errors
                user {
                    email
                    firstName
                    location {
                        address1
                        address2
                    }
                    postalLocation {
                        address1
                        address2
                    }
                }
            }
        }
    ''', variable_values={
        'userId': user_id,
        'userData': {
            'email': user.email,
            'firstName': user.first_name,
            'location': {
                'address1': new_location.address1,
                'address2': new_location.address2,
            },
            'postalLocation': {
                'address1': new_location.address1,
                'address2': new_location.address2,
            },
        }
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_profile_mutation_with_no_existing_user(snapshot):
    """ Test a failure update profile mutation because of no existing user """

    user = UserFactory()
    user_id = to_global_id('UserType', user.id + 999)
    new_email = "new@email.com"
    new_first_name = 'Bob'

    client = Client(schema)

    executed = client.execute('''
        mutation updateUser ($userId: ID!, $userData: UserInput!) {
            updateUser (userId: $userId, userData: $userData) {
                errors
                user {
                    email
                    firstName
                }
            }
        }
    ''', variable_values={
        'userId': user_id,
        'userData': {
            'email': new_email,
            'firstName': new_first_name,
        }})

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_create_contact_mutation(snapshot):
    """ Test a success create contact mutation """

    new_occupation = OccupationFactory()
    new_location = LocationFactory()
    contact = ContactFactory.build()
    new_spouse = ContactFactory()
    organisations = OrganisationFactory.create_batch(3)

    client = Client(schema)
    executed = client.execute("""
        mutation createContact($contactData: ContactInput!) {
            createContact(contactData: $contactData) {
                errors
                contact {
                    fullName
                    mobile
                    email
                    occupation
                    location {
                        address1
                        address2
                    }
                    postalLocation {
                        postalAddress1
                        postalAddress2
                    }
                    organisations {
                        edges {
                            node {
                                name
                            }
                        }
                    }
                    spouse {
                        id
                        fullName
                    }
                    father {
                        id
                        fullName
                    }
                    mother {
                        id
                        fullName
                    }
                    referrer {
                        id
                        fullName
                    }
            }
            }
        }
    """, variable_values={
        'contactData': {
            'email': contact.email,
            'firstName': contact.first_name,
            'lastName': contact.last_name,
            'mobile': contact.mobile,
            'occupation': new_occupation.id,
            'location': {
                'address1': new_location.address1,
                'address2': new_location.address2,
            },
            'postalLocation': {
                'address1': new_location.address1,
                'address2': new_location.address2,
            },
            'organisations': [to_global_id(
                'OrganisationType', org.id) for org in organisations],
            'spouseId': to_global_id(
                'ContactType', new_spouse.id),
            'motherId': to_global_id(
                'ContactType', new_spouse.id),
            'fatherId': to_global_id(
                'ContactType', new_spouse.id),
            'referrerId': to_global_id(
                'ContactType', new_spouse.id),
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_create_contact_mutation_without_email(snapshot):
    """ Test a failure create mutation without email """

    contact = ContactFactory.build()
    organisations = OrganisationFactory.create_batch(3)
    new_occupation = OccupationFactory()
    client = Client(schema)
    executed = client.execute("""
        mutation createContact($contactData: ContactInput!) {
            createContact(contactData: $contactData) {
                errors
                contact {
                    fullName
                    email
                    occupation
                    organisations {
                        edges {
                            node {
                                name
                            }
                        }
                    }
                }
            }
        }
    """, variable_values={
        'contactData': {
            'email': '',
            'firstName': contact.first_name,
            'lastName': contact.last_name,
            'occupation': new_occupation.id,
            'organisations': [to_global_id(
                'OrganisationType', org.id) for org in organisations],
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_create_contact_mutation_with_no_existing_spouse(snapshot):
    """ Test a success create contact mutation with incorrect spouse """

    contact = ContactFactory.build()
    new_spouse = ContactFactory()
    new_occupation = OccupationFactory(id=1)
    client = Client(schema)
    executed = client.execute("""
        mutation createContact($contactData: ContactInput!) {
            createContact(contactData: $contactData) {
                errors
                contact {
                    fullName
                    email
                    occupation
                    spouse {
                        id
                        fullName
                    }
                }
            }
        }
    """, variable_values={
        'contactData': {
            'email': contact.email,
            'firstName': contact.first_name,
            'lastName': contact.last_name,
            'occupation': new_occupation.id,
            'spouseId': to_global_id(
                'ContactType', new_spouse.id+666),
        }
    })

    snapshot.assert_match(executed)

#
# @pytest.mark.django_db
# def test_create_contact_mutation_with_no_existing_father_id(snapshot):
#     """ Test a success create contact mutation """
#
#     contact = ContactFactory()
#     father = ContactFactory()
#     new_email = 'new@email.com'
#
#     client = Client(schema)
#     executed = client.execute("""
#         mutation createContact($contactData: ContactInput!) {
#             createContact(contactData: $contactData) {
#                 errors
#                 contact {
#                     fullName
#                     email
#                     father {
#                         id
#                     }
#                 }
#             }
#         }
#     """, variable_values={
#         'contactData': {
#             'email': new_email,
#             'firstName': contact.first_name,
#             'lastName': contact.last_name,
#             'fatherId':  to_global_id(
#                 'ContactType', father.id+666),
#         }
#     })
#
#     snapshot.assert_match(executed)
#
#
# @pytest.mark.django_db
# def test_create_contact_mutation_with_no_existing_mother_id(snapshot):
#     """ Test a success create contact mutation """
#
#     new_occupation = OccupationFactory(id=1)
#     contact = ContactFactory()
#     new_spouse = ContactFactory()
#     organisations = OrganisationFactory.create_batch(3)
#     new_email = 'new@email.com'
#
#     client = Client(schema)
#     executed = client.execute("""
#         mutation createContact($contactData: ContactInput!) {
#             createContact(contactData: $contactData) {
#                 errors
#                 contact {
#                     fullName
#                     email
#                     occupation
#                     organisations {
#                         edges {
#                             node {
#                                 name
#                             }
#                         }
#                     }
#                     mother {
#                         id
#                     }
#                 }
#             }
#         }
#     """, variable_values={
#         'contactData': {
#             'email': new_email,
#             'firstName': contact.first_name,
#             'lastName': contact.last_name,
#             'occupation': new_occupation.id,
#             'organisations': [to_global_id(
#                 'OrganisationType', org.id) for org in organisations],
#             'motherId': to_global_id(
#                 'ContactType', new_spouse.id+666),
#         }
#     })
#
#     snapshot.assert_match(executed)


@pytest.mark.django_db
def test_create_contact_mutation2(snapshot):
    """ Test create contact mutation if contact email already exists """

    client = Client(schema)
    contact = ContactFactory()
    new_contact = ContactFactory.build()

    executed = client.execute("""
        mutation createContact($contactData: ContactInput!) {
            createContact(contactData: $contactData) {
                errors
            }
        }
    """, variable_values={
        'contactData': {
            'email': contact.email,  # use existing email
            'firstName': new_contact.first_name,
            'lastName': new_contact.last_name,
            'mobile': new_contact.mobile,
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_contact_mutation(snapshot):
    """ Test a success update contact mutation """

    contact = ContactFactory()
    client_instance = ClientFactory()
    new_email = 'new@email.com'
    new_first_name = 'John'
    new_occupation = OccupationFactory()
    new_location = LocationFactory()
    new_organisations = OrganisationFactory.create_batch(3)
    client = Client(schema)

    update_xero_contact_patch = patch(
        'accounts.mutations.update_xero_contact.delay')
    with update_xero_contact_patch as mock_update_xero_contact:
        executed = client.execute("""
            mutation updateContact($contactId: ID!, $contactData: ContactInput!) {
                updateContact(contactId: $contactId, contactData: $contactData) {
                    errors
                    contact {
                        email
                        firstName
                        occupation
                        organisations {
                            edges {
                                node {
                                    name
                                }
                            }
                        }
                        location {
                            address1
                            address2
                        }
                        postalLocation {
                            postalAddress1
                            postalAddress2
                        }
                    }
                }
            }
        """, variable_values={
            'contactId': to_global_id('ContactType', client_instance.contact.id),
            'contactData': {
                'email': new_email,
                'firstName': new_first_name,
                'occupation': new_occupation.id,
                'organisations': [to_global_id(
                    'OrganisationType', org.id) for org in new_organisations],
                'location': {
                    'address1': new_location.address1,
                    'address2': new_location.address2,
                },
                'postalLocation': {
                    'address1': new_location.address1,
                    'address2': new_location.address2,
                },
            }
        })
        mock_update_xero_contact.assert_called_once_with(client_instance.id)
        snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_contact_mutation_with_init_location(snapshot):
    """ Test a success update contact mutation with init location """

    contact = ContactFactory()
    client_instance = ClientFactory()
    new_email = 'new@email.com'
    new_first_name = 'John'
    contact.location = LocationFactory()
    contact.postal_location = LocationFactory()
    contact.save()
    new_location = LocationFactory()
    client = Client(schema)

    update_xero_contact_patch = patch(
        'accounts.mutations.update_xero_contact.delay')
    with update_xero_contact_patch as mock_update_xero_contact:
        executed = client.execute("""
            mutation updateContact($contactId: ID!, $contactData: ContactInput!) {
                updateContact(contactId: $contactId, contactData: $contactData) {
                    errors
                    contact {
                        email
                        firstName
                        location {
                            address1
                            address2
                        }
                        postalLocation {
                            postalAddress1
                            postalAddress2
                        }
                    }
                }
            }
        """, variable_values={
            'contactId': to_global_id('ContactType', client_instance.contact.id),
            'contactData': {
                'email': new_email,
                'firstName': new_first_name,
                'location': {
                    'address1': new_location.address1,
                    'address2': new_location.address2,
                },
                'postalLocation': {
                    'address1': new_location.address1,
                    'address2': new_location.address2,
                },
            }
        })
        mock_update_xero_contact.assert_called_once_with(client_instance.id)
        snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_contact_mutation_with_no_existing_contact(snapshot):
    """ Test a failure update contact mutation with no existing contact """

    contact = ContactFactory()
    new_email = 'new@email.com'
    new_first_name = 'John'

    client = Client(schema)

    executed = client.execute("""
        mutation updateContact($contactId: ID!, $contactData: ContactInput!) {
            updateContact(contactId: $contactId, contactData: $contactData) {
                errors
                contact {
                    email
                    firstName
                }
            }
        }
    """, variable_values={
        'contactId': to_global_id('ContactType', contact.id+999),
        'contactData': {
            'email': new_email,
            'firstName': new_first_name,
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_contact_mutation_without_contact_id(snapshot):
    """ Test a update contact mutation without contact id"""
    new_email = 'new@email.com'
    new_first_name = 'John'
    client = Client(schema)

    executed = client.execute("""
        mutation updateContact($contactId: ID!, $contactData: ContactInput!) {
            updateContact(contactId: $contactId, contactData: $contactData) {
                errors
                contact {
                    email
                    firstName
                }
            }
        }
    """, variable_values={
        'contactId': '',
        'contactData': {
            'email': new_email,
            'firstName': new_first_name,
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_create_organisation_mutation(snapshot):
    """ Test a success create organisation mutation """

    client = Client(schema)
    organisation = OrganisationFactory.build()
    contacts = ContactFactory.create_batch(3)
    update_xero_contact_patch = patch(
        'accounts.mutations.update_xero_contact.delay')
    with update_xero_contact_patch as mock_update_xero_contact:
        executed = client.execute("""
            mutation createOrganisation($organisationData: OrganisationInput!) {
                createOrganisation(organisationData: $organisationData) {
                    errors
                    organisation {
                        name
                        clients {
                            edges {
                                node {
                                    name
                                }
                            }
                        }
                        contacts {
                            edges {
                                node {
                                    fullName
                                }
                            }
                        }
                    }
                }
            }
        """, variable_values={
            'organisationData': {
                'contacts': [to_global_id(
                    'ClientType', contact.id) for contact in contacts],
                'name': 'New Organisation',
                'groupStatus': organisation.group_status,
            }
        })
        mock_update_xero_contact.mock_calls == [
            mock_update_xero_contact.call(contact.id) for contact in contacts
        ]

        snapshot.assert_match(executed)


@pytest.mark.django_db
def test_create_organisation_mutation2(snapshot):
    """ Test success create organisation """

    client = Client(schema)
    organisation = OrganisationFactory()
    organisation2 = OrganisationFactory()
    location = LocationFactory()

    executed = client.execute("""
        mutation createOrganisation($organisationData: OrganisationInput!) {
            createOrganisation(organisationData: $organisationData) {
                errors
                organisation {
                    name
                    location {
                        address1
                        address2
                        suburb
                        state
                        postCode
                        country
                    }
                    groupParent {
                        id
                    }
                    postalLocation {
                        postalAddress1
                        postalAddress2
                        postalSuburb
                        postalState
                        postalPostCode
                        postalCountry
                    }
                    clients {
                        edges {
                            node {
                                name
                            }
                        }
                    }

                }
            }
        }
    """, variable_values={
        'organisationData': {
            'location': {
                'address1': location.address1,
                'address2': location.address2,
                'suburb': location.suburb,
                'state': location.state,
                'postCode': location.post_code,
                'country': location.country
            },
            'postalLocation': {
                'address1': location.address1,
                'address2': location.address2,
                'suburb': location.suburb,
                'state': location.state,
                'postCode': location.post_code,
                'country': location.country
            },
            'name': 'New Organisation',
            'groupStatus': organisation.group_status,
            'groupParent': {
                'id': to_global_id('OrganisationType', organisation2.id)
            }
        }
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_create_organisation_mutation3(snapshot):
    """ Test a success create organisation mutation """

    client = Client(schema)
    organisation = OrganisationFactory.build()
    contacts = ContactFactory.create_batch(3)
    update_xero_contact_patch = patch(
        'accounts.mutations.update_xero_contact.delay')
    with update_xero_contact_patch as mock_update_xero_contact:
        executed = client.execute("""
            mutation createOrganisation($organisationData: OrganisationInput!) {
                createOrganisation(organisationData: $organisationData) {
                    errors
                    organisation {
                        name
                        clients {
                            edges {
                                node {
                                    name
                                }
                            }
                        }
                        groupParent {
                            id
                        }
                        contacts {
                            edges {
                                node {
                                    fullName
                                }
                            }
                        }
                    }
                }
            }
        """, variable_values={
            'organisationData': {
                'contacts': [to_global_id('ClientType', contact.id) for contact in contacts],
                'name': 'New Organisation',
                'groupStatus': organisation.group_status,
                'groupParent': {
                    'id': ''
                }
            }
        })
        mock_update_xero_contact.mock_calls == [
            mock_update_xero_contact.call(contact.id) for contact in contacts
        ]
        snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_organisations_mutation(snapshot):
    """ Test a success update organisation mutation """

    client = Client(schema)
    contact = ContactFactory()
    organisations = OrganisationFactory.create_batch(3)

    client = Client(schema)
    update_xero_contact_patch = patch(
        'accounts.mutations.update_xero_contact.delay')
    with update_xero_contact_patch as mock_update_xero_contact:
        executed = client.execute("""
            mutation updateOrganisations($contactId: ID!, $organisations:[ID]!) {
                updateOrganisations(contactId: $contactId, organisations: $organisations) {
                    errors
                }
            }
        """, variable_values={
            'contactId': to_global_id('ContactType', contact.id),
            'organisations': [to_global_id(
                'OrganisationType', org.id) for org in organisations],
            })
        mock_update_xero_contact.mock_calls == [
            mock_update_xero_contact.call(org) for org in organisations
        ]
        snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_organisations_mutation_with_no_existing_user(snapshot):
    """ Test a failure update organisation mutation with no existing user """

    client = Client(schema)
    contact = ContactFactory()
    organisations = OrganisationFactory.create_batch(3)

    client = Client(schema)
    executed = client.execute("""
        mutation updateOrganisations($contactId: ID!, $organisations:[ID]!) {
            updateOrganisations(contactId: $contactId, organisations: $organisations) {
                errors
            }
        }
    """, variable_values={
        'contactId': to_global_id('ContactType', contact.id+666),
        'organisations': [to_global_id(
            'OrganisationType', org.id) for org in organisations],
        })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_organisations_mutation_without_contact_id(snapshot):
    """ Test a failure update organisation mutation without contact id """

    client = Client(schema)
    organisations = []

    client = Client(schema)
    executed = client.execute("""
        mutation updateOrganisations($contactId: ID!, $organisations:[ID]!) {
            updateOrganisations(contactId: $contactId, organisations: $organisations) {
                errors
            }
        }
    """, variable_values={
        'contactId': '',
        'organisations': [to_global_id(
            'OrganisationType', org.id) for org in organisations],
        })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_organisations_mutation_with_init_organisations(snapshot):
    """ Test a success update organisation mutation """

    client = Client(schema)
    contact = ContactFactory(organisations=OrganisationFactory.create_batch(3))
    organisations = []

    client = Client(schema)
    executed = client.execute("""
        mutation updateOrganisations($contactId: ID!, $organisations:[ID]!) {
            updateOrganisations(contactId: $contactId, organisations: $organisations) {
                errors
            }
        }
    """, variable_values={
        'contactId': to_global_id('ContactType', contact.id),
        'organisations': [to_global_id(
            'OrganisationType', org.id) for org in organisations],
        })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_organisations_mutation_with_delete_exception(snapshot):
    """ Test a update organisation mutation with delete exception """

    # Exeption raise when Clients cannot be deleted because
    # they have a Matter assigned to them. Client have to related with contact.
    # And it have just the same organisation with contact in nested fields.
    # LeadStatusFactory(id=1)
    # EntryTypeFactory(id=1)
    organisations = OrganisationFactory.create_batch(2)
    client_instance = ClientFactory(organisation=organisations[0])

    matter = MatterFactory()
    client_instance.matters.add(matter)

    contact = ContactFactory(organisations=organisations[0:1])
    client_instance.contact = contact

    contact.clients.add(client_instance)
    organisations = []
    contact.save()

    client = Client(schema)
    executed = client.execute("""
        mutation updateOrganisations($contactId: ID!, $organisations:[ID]!) {
            updateOrganisations(contactId: $contactId, organisations: $organisations) {
                errors
            }
        }
    """, variable_values={
        'contactId': to_global_id('ContactType', contact.id),
        'organisations': [
            to_global_id('OrganisationType', org.id) for org in organisations],
        })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_organisation_details_mutation(snapshot):
    """ Test a success update organisation mutation """

    client = Client(schema)

    organisation = OrganisationFactory()
    new_name = 'New Organisation'
    new_main_line = '08-8361-2004'

    executed = client.execute("""
    mutation updateOrganisation($organisationId: ID!, $organisationData: OrganisationInput!) {
       updateOrganisationDetails(organisationId: $organisationId,   organisationData: $organisationData) {
            errors
            organisation {
                name
                mainLine
            }
        }
    }
    """, variable_values={
        'organisationId': to_global_id('OrganisationType', organisation.id),
        'organisationData': {
            'name': new_name,
            'mainLine': new_main_line
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_organisation_details_mutation2(snapshot):
    """ Test a success update organisation mutation """

    client = Client(schema)

    organisation = OrganisationFactory()
    new_name = 'New Organisation'

    executed = client.execute("""
       mutation updateOrganisation($organisationId: ID!, $organisationData: OrganisationInput!) {
        updateOrganisationDetails(organisationId: $organisationId, organisationData: $organisationData) {
            errors
            organisation {
                name
            }
        }
       }
    """, variable_values={
        'organisationId': '',
        'organisationData': {
            'name': ''
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_organisation_details_mutation3(snapshot):
    """ Test a success update organisation mutation """

    client = Client(schema)

    organisation = OrganisationFactory()
    new_name = 'New Organisation'

    executed = client.execute("""
       mutation updateOrganisation($organisationId: ID!, $organisationData: OrganisationInput!) {
        updateOrganisationDetails(organisationId: $organisationId, organisationData: $organisationData) {
            errors
            organisation {
                name
            }
        }
       }
    """, variable_values={
        'organisationId': to_global_id('OrganisationType', 123123),
        'organisationData': {
            'name': new_name
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_organisation_details_mutation4(snapshot):
    """ Test a success update organisation mutation """

    client = Client(schema)

    organisation = OrganisationFactory()
    new_name = 'New Organisation'
    contacts = ContactFactory.create_batch(2)
    update_xero_contact_patch = patch(
        'accounts.mutations.update_xero_contact.delay')
    with update_xero_contact_patch as mock_update_xero_contact:
        executed = client.execute("""
           mutation updateOrganisation($organisationId: ID!, $organisationData: OrganisationInput!) {
            updateOrganisationDetails(organisationId: $organisationId, organisationData: $organisationData) {
                errors
                organisation {
                    name
                    contacts {
                        edges {
                            node {
                                id
                            }
                        }
                    }
                }
            }
           }
        """, variable_values={
            'organisationId': to_global_id('OrganisationType', organisation.id),
            'organisationData': {
                'name': new_name,
                'contacts': [to_global_id('ClientType', contact.id) for contact in contacts]
            }
        })
        mock_update_xero_contact.mock_calls == [
            mock_update_xero_contact.call(contact) for contact in contacts
        ]
        snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_ralationships_mutation(snapshot):
    """ Test a success update relationships mutation """

    new_spouse = ContactFactory()
    new_contact = ContactFactory(_spouses=[new_spouse, ])
    new_contact.mother = new_spouse
    new_contact.father = new_spouse
    new_contact.save()

    client = Client(schema)
    executed = client.execute("""
       mutation updateReferrer($relationship: RelationshipInput!) {
        updateReferrer( relationship: $relationship) {
            errors
            contact {
                id
            }
            spouse {
                id
            }
            father {
                id
            }
            mother {
                id
            }
            referrer {
                id
            }
        }
    }
    """, variable_values={
        'relationship': {
            'contactId':  to_global_id(
                'ContactType', new_contact.id),
            'spouseId': to_global_id(
                'ContactType', new_spouse.id),
            'motherId': to_global_id(
                'ContactType', new_spouse.id),
            'fatherId': to_global_id(
                'ContactType', new_spouse.id),
            'referrerId': to_global_id(
                'ContactType', new_spouse.id),
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_ralationships_mutation_with_init_relations(snapshot):
    """ Test a success update relationships mutation with init relations """

    new_spouse = ContactFactory()
    new_contact = ContactFactory(_spouses=[new_spouse, ])
    new_contact.referrer = new_spouse
    new_contact.mother = new_spouse
    new_contact.father = new_spouse
    new_contact.save()

    client = Client(schema)
    executed = client.execute("""
       mutation updateReferrer($relationship: RelationshipInput!) {
        updateReferrer( relationship: $relationship) {
            errors
            contact {
                id
            }
        }
    }
    """, variable_values={
        'relationship': {
            'contactId':  to_global_id(
                'ContactType', new_contact.id),
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_ralationships_mutation_without_contact_id(snapshot):
    """ Test a failure update relationships mutation without contact id """

    client = Client(schema)
    executed = client.execute("""
       mutation updateReferrer($relationship: RelationshipInput!) {
        updateReferrer( relationship: $relationship) {
            errors
            contact {
                id
            }
        }
    }
    """, variable_values={
        'relationship': {
            'contactId': '',
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_ralationships_mutation_with_no_exist_contact(snapshot):
    """ Test a failure update relationships mutation with no exist contact """

    new_contact = ContactFactory()

    client = Client(schema)
    executed = client.execute("""
       mutation updateReferrer($relationship: RelationshipInput!) {
        updateReferrer( relationship: $relationship) {
            errors
            contact {
                id
            }
        }
    }
    """, variable_values={
        'relationship': {
            'contactId':  to_global_id(
                'ContactType', new_contact.id+999),
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_ralationships_mutation_with_no_exist_spouse(snapshot):
    """ Test a failure update relationships mutation with no exist spouse """

    new_contact = ContactFactory()

    client = Client(schema)
    executed = client.execute("""
       mutation updateReferrer($relationship: RelationshipInput!) {
        updateReferrer( relationship: $relationship) {
            errors
            contact {
                id
            }
            spouse {
                id
            }
        }
    }
    """, variable_values={
        'relationship': {
            'contactId':  to_global_id(
                'ContactType', new_contact.id),
            'spouseId':  to_global_id(
                'ContactType', new_contact.id+999),
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_ralationships_mutation_with_no_exist_mother(snapshot):
    """ Test a failure update relationships mutation with no exist mother """

    new_contact = ContactFactory()
    new_spouse = ContactFactory()

    client = Client(schema)
    executed = client.execute("""
       mutation updateReferrer($relationship: RelationshipInput!) {
        updateReferrer( relationship: $relationship) {
            errors
            contact {
                id
            }
            spouse {
                id
            }
            mother {
                id
            }
        }
    }
    """, variable_values={
        'relationship': {
            'contactId':  to_global_id(
                'ContactType', new_contact.id),
            'spouseId':  to_global_id(
                'ContactType', new_spouse.id),
            'motherId':  to_global_id(
                'ContactType', new_spouse.id+666),
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_ralationships_mutation_with_no_exist_father(snapshot):
    """ Test a failure update relationships mutation with no exist father """

    new_contact = ContactFactory()
    new_spouse = ContactFactory()
    client = Client(schema)
    executed = client.execute("""
       mutation updateReferrer($relationship: RelationshipInput!) {
        updateReferrer( relationship: $relationship) {
            errors
            contact {
                id
            }
            spouse {
                id
            }
            mother {
                id
            }
            father {
                id
            }
        }
    }
    """, variable_values={
        'relationship': {
            'contactId':  to_global_id(
                'ContactType', new_contact.id),
            'spouseId':  to_global_id(
                'ContactType', new_spouse.id),
            'motherId':  to_global_id(
                'ContactType', new_spouse.id),
            'fatherId':  to_global_id(
                'ContactType', new_spouse.id+666),
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_ralationships_mutation_with_no_exist_referrer(snapshot):
    """ Test a failure update relationships mutation with no exist referrer """

    new_contact = ContactFactory()
    new_spouse = ContactFactory()

    client = Client(schema)
    executed = client.execute("""
       mutation updateReferrer($relationship: RelationshipInput!) {
        updateReferrer( relationship: $relationship) {
            errors
            contact {
                id
            }
            referrer {
                id
            }
        }
    }
    """, variable_values={
        'relationship': {
            'contactId':  to_global_id(
                'ContactType', new_contact.id),
            'referrerId':  to_global_id(
                'ContactType', new_spouse.id+666),
        }
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_organisation_location_mutation(snapshot):
    """ Test a success update organisation location mutation """

    client = Client(schema)

    organisation = OrganisationFactory()
    location = LocationFactory()

    executed = client.execute("""
         mutation updateOrganisationLocation(
           $id: ID!
           $address1: String
           $address2: String
           $state: Int
           $country: String
           $postCode: String
           $suburb: String
           $postalAddress1: String
           $postalAddress2: String
           $postalState: Int
           $postalCountry: String
           $postalPostCode: String
           $postalSuburb: String
           $addressesAreEquals: Boolean
         ) {
           updateOrganisationLocation(
             id: $id
             address1: $address1
             address2: $address2
             state: $state
             country: $country
             postCode: $postCode
             suburb: $suburb
             postalAddress1: $postalAddress1
             postalAddress2: $postalAddress2
             postalState: $postalState
             postalCountry: $postalCountry
             postalPostCode: $postalPostCode
             postalSuburb: $postalSuburb
             addressesAreEquals: $addressesAreEquals
           ) {
             errors
           }
         }
    """, variable_values={
        'id': to_global_id('OrganisationType', organisation.id),
        'address1': location.address1,
        'address2': location.address2,
        'state': location.state,
        'country': location.country,
        'postCode': location.post_code,
        'suburb': location.suburb,
        'postalAddress1': location.address1,
        'postalAddress2': location.address2,
        'postalState': location.state,
        'postalCountry': location.country,
        'postalPostCode': location.post_code,
        'postalSuburb': location.suburb,
        'addressesAreEquals': False,
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_organisation_location_mutation2(snapshot):
    """ Test a success update organisation location mutation """

    client = Client(schema)

    organisation = OrganisationFactory()
    location = LocationFactory()

    executed = client.execute("""
         mutation updateOrganisationLocation(
           $id: ID!
           $address1: String
           $address2: String
           $state: Int
           $country: String
           $postCode: String
           $suburb: String
           $postalAddress1: String
           $postalAddress2: String
           $postalState: Int
           $postalCountry: String
           $postalPostCode: String
           $postalSuburb: String
           $addressesAreEquals: Boolean
         ) {
           updateOrganisationLocation(
             id: $id
             address1: $address1
             address2: $address2
             state: $state
             country: $country
             postCode: $postCode
             suburb: $suburb
             postalAddress1: $postalAddress1
             postalAddress2: $postalAddress2
             postalState: $postalState
             postalCountry: $postalCountry
             postalPostCode: $postalPostCode
             postalSuburb: $postalSuburb
             addressesAreEquals: $addressesAreEquals
           ) {
             errors
           }
         }
    """, variable_values={
        'id': to_global_id('OrganisationType', 123123),
        'address1': location.address1,
        'address2': location.address2,
        'state': location.state,
        'country': location.country,
        'postCode': location.post_code,
        'suburb': location.suburb,
        'postalAddress1': location.address1,
        'postalAddress2': location.address2,
        'postalState': location.state,
        'postalCountry': location.country,
        'postalPostCode': location.post_code,
        'postalSuburb': location.suburb,
        'addressesAreEquals': False,
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_organisation_location_mutation3(snapshot):
    """ Test a success update organisation location mutation """

    client = Client(schema)

    organisation = OrganisationFactory()
    organisation.location.delete()
    location = LocationFactory()

    executed = client.execute("""
         mutation updateOrganisationLocation(
           $id: ID!
           $address1: String
           $address2: String
           $state: Int
           $country: String
           $postCode: String
           $suburb: String
           $postalAddress1: String
           $postalAddress2: String
           $postalState: Int
           $postalCountry: String
           $postalPostCode: String
           $postalSuburb: String
           $addressesAreEquals: Boolean
         ) {
           updateOrganisationLocation(
             id: $id
             address1: $address1
             address2: $address2
             state: $state
             country: $country
             postCode: $postCode
             suburb: $suburb
             postalAddress1: $postalAddress1
             postalAddress2: $postalAddress2
             postalState: $postalState
             postalCountry: $postalCountry
             postalPostCode: $postalPostCode
             postalSuburb: $postalSuburb
             addressesAreEquals: $addressesAreEquals
           ) {
             errors
           }
         }
    """, variable_values={
        'id': to_global_id('OrganisationType', organisation.id),
        'address1': location.address1,
        'address2': location.address2,
        'state': location.state,
        'country': location.country,
        'postCode': location.post_code,
        'suburb': location.suburb,
        'postalAddress1': location.address1,
        'postalAddress2': location.address2,
        'postalState': location.state,
        'postalCountry': location.country,
        'postalPostCode': location.post_code,
        'postalSuburb': location.suburb,
        'addressesAreEquals': True,
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_organisation_location_mutation4(snapshot):
    """ Test a success update organisation location mutation """

    client = Client(schema)

    organisation = OrganisationFactory()
    location = LocationFactory()
    organisation.location.address1 = location.address1
    organisation.location.address2 = location.address2
    organisation.location.state = location.state
    organisation.location.country = location.country
    organisation.location.post_code = location.post_code
    organisation.location.suburb = location.suburb

    executed = client.execute("""
         mutation updateOrganisationLocation(
           $id: ID!
           $address1: String
           $address2: String
           $state: Int
           $country: String
           $postCode: String
           $suburb: String
           $postalAddress1: String
           $postalAddress2: String
           $postalState: Int
           $postalCountry: String
           $postalPostCode: String
           $postalSuburb: String
           $addressesAreEquals: Boolean
         ) {
           updateOrganisationLocation(
             id: $id
             address1: $address1
             address2: $address2
             state: $state
             country: $country
             postCode: $postCode
             suburb: $suburb
             postalAddress1: $postalAddress1
             postalAddress2: $postalAddress2
             postalState: $postalState
             postalCountry: $postalCountry
             postalPostCode: $postalPostCode
             postalSuburb: $postalSuburb
             addressesAreEquals: $addressesAreEquals
           ) {
             errors
           }
         }
    """, variable_values={
        'id': to_global_id('OrganisationType', organisation.id),
        'address1': location.address1,
        'address2': location.address2,
        'state': location.state,
        'country': location.country,
        'postCode': location.post_code,
        'suburb': location.suburb,
        'postalAddress1': location.address1,
        'postalAddress2': location.address2,
        'postalState': location.state,
        'postalCountry': location.country,
        'postalPostCode': location.post_code,
        'postalSuburb': location.suburb,
        'addressesAreEquals': True,
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_organisation_location_mutation_without_id(snapshot):
    """ Test a success update organisation location mutation without id """

    client = Client(schema)
    executed = client.execute("""
         mutation updateOrganisationLocation($id: ID!) {
           updateOrganisationLocation(id: $id) {
             errors
           }
         }
    """, variable_values={
        'id': '',
    })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_organisation_associaton_mutation(snapshot):
    """Test success update organisation mutation"""

    client = Client(schema)

    organisation = OrganisationFactory()
    contact = ContactFactory()

    executed = client.execute("""
        mutation updateAssociaton($organisationId: ID!, $contacts: [ID]!) {
          updateOrganisationAssociation(organisationId: $organisationId, contacts: $contacts) {
            errors
          }
        }
    """, variable_values={
        'organisationId': to_global_id('OrganisationType', organisation.id),
        'contacts': [to_global_id('ContactType', contact.id)],
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_organisation_associaton_mutation_without_id(snapshot):
    """Test a failure update organisation mutation without id"""

    contact = ContactFactory()

    client = Client(schema)
    executed = client.execute("""
        mutation updateAssociaton($organisationId: ID!, $contacts: [ID]!) {
          updateOrganisationAssociation(organisationId: $organisationId, contacts: $contacts) {
            errors
          }
        }
    """, variable_values={
        'organisationId': '',
        'contacts': [to_global_id('ContactType', contact.id)],
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_organisation_associaton_mutation2(snapshot):
    """Test success update organisation mutation"""

    client = Client(schema)

    organisation = OrganisationFactory()
    contact = ContactFactory()

    executed = client.execute("""
        mutation updateAssociaton($organisationId: ID!, $contacts: [ID]!) {
          updateOrganisationAssociation(organisationId: $organisationId, contacts: $contacts) {
            errors
          }
        }
    """, variable_values={
        'organisationId': to_global_id('OrganisationType', 123),
        'contacts': [to_global_id('ContactType', contact.id)],
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_organisation_associaton_mutation3(snapshot):
    """Test success update organisation mutation"""

    client = Client(schema)

    organisation = OrganisationFactory()
    contact = ContactFactory()
    contact2 = ContactFactory()

    executed = client.execute("""
        mutation updateAssociaton($organisationId: ID!, $contacts: [ID]!) {
          updateOrganisationAssociation(organisationId: $organisationId, contacts: $contacts) {
            errors
          }
        }
    """, variable_values={
        'organisationId': to_global_id('OrganisationType', organisation.id),
        'contacts': [
            to_global_id('ContactType', contact.id),
            to_global_id('ContactType', contact2.id)
            ],
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_organisation_associaton_mutation4(snapshot):
    """Test success update organisation mutation"""

    client = Client(schema)

    organisation = OrganisationFactory()
    old_contacts = ContactFactory.create_batch(size=5)
    organisation.contacts.add(*old_contacts)
    contact = old_contacts[0]
    matter = MatterFactory()
    client_instance = ClientFactory()
    client.contact = contact
    client.organisation = organisation
    matter.client = client_instance
    contacts = old_contacts[:2]

    executed = client.execute("""
        mutation updateAssociaton($organisationId: ID!, $contacts: [ID]!) {
          updateOrganisationAssociation(organisationId: $organisationId, contacts: $contacts) {
            errors
          }
        }
    """, variable_values={
        'organisationId': to_global_id('OrganisationType', organisation.id),
        'contacts': [
            to_global_id('ContactType', contact.id) for contact in contacts],
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_organisation_associaton_mutation_with_delete_exception(snapshot):
    """ Test failure update organisation mutation with delete exception """

    # Exeption raise when Clients cannot be deleted because
    # they have a Matter assigned to them. Client have to related with contact.
    # And it have just the same organisation with contact in nested fields.

    contacts = ContactFactory.create_batch(3)

    client_instance = ClientFactory()
    matter = MatterFactory()
    client_instance.matters.add(matter)

    organisation = OrganisationFactory()
    client_instance.organisation = organisation
    organisation.contacts.add(*contacts)
    contacts[0].organisation = organisation

    client_instance.contact = contacts[0]
    client_instance.save()
    contacts = []

    client = Client(schema)
    executed = client.execute("""
        mutation updateAssociaton($organisationId: ID!, $contacts: [ID]!) {
          updateOrganisationAssociation(organisationId: $organisationId, contacts: $contacts) {
            errors
          }
        }
    """, variable_values={
        'organisationId': to_global_id(
            'OrganisationType', organisation.id),
        'contacts': [
            to_global_id('ContactType', cont.id) for cont in contacts],
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_create_client_mutation(snapshot):
    """Test a success creating client with two contact
        and organisation mutation"""

    client = Client(schema)
    organisation = OrganisationFactory()
    contact = ContactFactory()
    second_contact = ContactFactory()
    client_instance = ClientFactory()
    update_xero_contact_patch = patch(
        'accounts.mutations.update_xero_contact.delay')
    with update_xero_contact_patch as mock_update_xero_contact:
        executed = client.execute("""
          mutation createClient($clientData: ClientInput!) {
            createClient(clientData: $clientData) {
                errors
                client {
                    organisation {
                        id
                        mainLine
                    }
                    contact {
                        id
                        mobile
                    }
                    secondContact {
                        id
                        mobile
                    }
                    office {
                        id
                    }
                    isActive
                }
            }
        }
        """, variable_values={
            'clientData': {
                'organisation': {
                    'id': to_global_id('OrganisationType', organisation.id),
                },
                'contact': {
                    'id': to_global_id('ContactType', contact.id),
                    'mobile': contact.mobile
                },
                'secondContact': {
                    'id': to_global_id('ContactType', second_contact.id),
                    'mobile': ''
                },
                'office': {
                    'id': client_instance.office_id
                },
                'isActive': client_instance.is_active
            },
        })
        mock_update_xero_contact.assert_called_once_with(contact.clients.last().id)
        snapshot.assert_match(executed)


@pytest.mark.django_db
def test_create_client_mutation2(snapshot):
    """Tets a success creating client with one contact"""

    client = Client(schema)
    client_instance = ClientFactory()
    contact = ContactFactory()
    update_xero_contact_patch = patch(
        'accounts.mutations.update_xero_contact.delay')
    with update_xero_contact_patch as mock_update_xero_contact:
        executed = client.execute("""
          mutation createClient($clientData: ClientInput!) {
            createClient(clientData: $clientData) {
                errors
                client {
                    contact {
                        id
                        mobile
                    }
                    office {
                        id
                    }
                    isActive
                }
            }
        }
        """, variable_values={
            'clientData': {
                'contact': {
                    'id': to_global_id('ContactType', contact.id),
                    'mobile': contact.mobile
                },
                'office': {
                    'id': client_instance.office_id
                },
                'isActive': client_instance.is_active
            },
        })
        mock_update_xero_contact.assert_called_once_with(contact.clients.last().id)
        snapshot.assert_match(executed)


@pytest.mark.django_db
def test_create_client_mutation3(snapshot):
    """Test a success creation client with two contacts"""

    client = Client(schema)
    first_contact = ContactFactory()
    second_contact = ContactFactory()
    client_instance = ClientFactory()
    is_active = True
    update_xero_contact_patch = patch(
        'accounts.mutations.update_xero_contact.delay')
    with update_xero_contact_patch as mock_update_xero_contact:
        executed = client.execute("""
          mutation createClient($clientData: ClientInput!) {
            createClient(clientData: $clientData) {
                errors
                client {
                    contact {
                        id
                        mobile
                    }
                    secondContact {
                        id
                        mobile
                    }
                    office {
                        id
                    }
                    isActive
                }
            }
        }
        """, variable_values={
            'clientData': {
                'contact': {
                    'id': to_global_id('ContactType', first_contact.id),
                    'mobile': first_contact.mobile
                },
                'secondContact': {
                    'id': to_global_id('ContactType', second_contact.id),
                    'mobile': second_contact.mobile
                },
                'office': {
                    'id': client_instance.office_id
                },
                'isActive': is_active
            },
        })
        mock_update_xero_contact.assert_called_once_with(first_contact.clients.last().id)
        snapshot.assert_match(executed)


@pytest.mark.django_db
def test_create_client_mutation4(snapshot):
    """Test a success creaition client with one contact and organisation"""

    client = Client(schema)
    client_instance = ClientFactory()
    organisation = OrganisationFactory()
    contact = ContactFactory()
    is_active = True
    update_xero_contact_patch = patch(
        'accounts.mutations.update_xero_contact.delay')
    with update_xero_contact_patch as mock_update_xero_contact:
        executed = client.execute("""
          mutation createClient($clientData: ClientInput!) {
            createClient(clientData: $clientData) {
                errors
                client {
                    contact {
                        id
                        mobile
                    }
                    organisation {
                        id
                        mainLine
                    }
                    office {
                        id
                    }
                    isActive
                }
            }
        }
        """, variable_values={
            'clientData': {
                'organisation': {
                    'id': to_global_id('OrganisationType', organisation.id),
                    'mainLine': organisation.main_line
                },
                'contact': {
                    'id': to_global_id('ContactType', contact.id),
                    'mobile': contact.mobile
                },
                'office': {
                    'id': client_instance.office_id
                },
                'isActive': is_active
            },
        })
        mock_update_xero_contact.assert_called_once_with(contact.clients.last().id)
        snapshot.assert_match(executed)


@pytest.mark.django_db
def test_create_client_mutation5(snapshot):
    """Test a successe creation client with incorrect information"""
    client = Client(schema)
    contact = ContactFactory()
    client_instance = ClientFactory()
    update_xero_contact_patch = patch(
        'accounts.mutations.update_xero_contact.delay')
    with update_xero_contact_patch as mock_update_xero_contact:
        executed = client.execute("""
          mutation createClient($clientData: ClientInput!) {
            createClient(clientData: $clientData) {
                errors
                client {
                    organisation {
                        id
                        mainLine
                    }
                    contact {
                        id
                        mobile
                    }
                    secondContact {
                        id
                        mobile
                    }
                    office {
                        id
                    }
                    isActive
                }
            }
        }
        """, variable_values={
            'clientData': {
                'organisation': {
                    'id': to_global_id('OrganisationType', 123123223),
                },
                'contact': {
                    'id': to_global_id('ContactType', contact.id),
                    'mobile': contact.mobile
                },
                'secondContact': {
                    'id': to_global_id('ContactType', 123123123),
                    'mobile': ''
                },
                'office': {
                    'id': client_instance.office_id
                },
                'isActive': client_instance.is_active
            },
        })
        mock_update_xero_contact.assert_called_once_with(contact.clients.last().id)
        snapshot.assert_match(executed)


@pytest.mark.django_db
def test_create_client_mutation6(snapshot):
    """Test a successe creation client with incorrect information"""
    client = Client(schema)
    contact = ContactFactory()
    client_instance = ClientFactory()

    executed = client.execute("""
      mutation createClient($clientData: ClientInput!) {
        createClient(clientData: $clientData) {
            errors
            client {
                contact {
                    id
                    mobile
                }
                secondContact {
                    id
                    mobile
                }
                office {
                    id
                }
                isActive
            }
        }
    }
    """, variable_values={
        'clientData': {
            'contact': {
                'id': to_global_id('ContactType', 12312321),
                'mobile': contact.mobile
            },
            'secondContact': {
                'id': to_global_id('ContactType', contact.id),
                'mobile': ''
            },
            'office': {
                'id': client_instance.office_id
            },
            'isActive': client_instance.is_active
        },
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_create_client_mutation7(snapshot):
    """Test a successe creation client with incorrect information"""
    client = Client(schema)
    contact = ContactFactory()
    client_instance = ClientFactory()

    executed = client.execute("""
      mutation createClient($clientData: ClientInput!) {
        createClient(clientData: $clientData) {
            errors
            client {
                contact {
                    id
                    mobile
                }
                office {
                    id
                }
                isActive
            }
        }
    }
    """, variable_values={
        'clientData': {
            'contact': {
                'id': '',
                'mobile': contact.mobile
            },
            'office': {
                'id': client_instance.office_id
            },
            'isActive': client_instance.is_active
        },
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_client_mutation(snapshot):
    """Test a success update client mutation with incorrect id"""

    client = Client(schema)

    executed = client.execute("""
        mutation updateDetails($clientData: ClientInput!) {
        updateClientDetails(clientData: $clientData) {
          errors
          client {
            id
          }
        }
      }
    """, variable_values={
        'clientData': {
            'id': to_global_id('ClientType', 123123123),
        }
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_client_mutation2(snapshot):
    """Test a success update client mutation with missing id"""

    client = Client(schema)
    # client_instance = ClientFactory()

    executed = client.execute("""
        mutation updateDetails($clientData: ClientInput!) {
        updateClientDetails(clientData: $clientData) {
          errors
          client {
            id
          }
        }
      }
    """, variable_values={
        'clientData': {
            'id': '',
        }
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_client_mutation3(snapshot):
    """Test a success update client mutation"""

    client = Client(schema)
    client_instance = ClientFactory()
    update_xero_contact_patch = patch(
        'accounts.mutations.update_xero_contact.delay')
    with update_xero_contact_patch as mock_update_xero_contact:
        executed = client.execute("""
            mutation updateDetails($clientData: ClientInput!) {
            updateClientDetails(clientData: $clientData) {
              errors
              client {
                id
                organisation {
                  id
                  mainLine
                  website
                }
                contact {
                  id
                  mobile
                  role
                }
                secondContact {
                  id
                  mobile
                  role
                }
                isActive
                office {
                  id
                }
            }
          }
         }
        """, variable_values={
            'clientData': {
                'id': to_global_id('ClientType', client_instance.id),
                'organisation': {
                    'id': to_global_id(
                        'OrganisationType', client_instance.organisation.id),
                    'mainLine': '2222222222',
                    'website': 'www.hhh.com'
                },
                'contact': {
                    'id': to_global_id(
                        'ContactType', client_instance.contact.id),
                    'mobile': client_instance.contact.mobile,
                    'role': 'OtherRole',
                },
                'secondContact': {
                    'id': to_global_id(
                        'ContactType', client_instance.second_contact.id),
                    'mobile': client_instance.second_contact.mobile,
                    'role': 'Myrole',
                },
                'isActive': True,
                'office': {
                    'id': client_instance.office_id
                }
            }
        })
        mock_update_xero_contact.assert_called_once_with(client_instance.id)
        snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_client_mutation4(snapshot):
    """Test a success update client mutation with incorrect organisation id"""

    client = Client(schema)
    client_instance = ClientFactory()

    executed = client.execute("""
        mutation updateDetails($clientData: ClientInput!) {
        updateClientDetails(clientData: $clientData) {
          errors
          client {
            id
            organisation {
              id
              mainLine
              website
            }
            contact {
              id
              mobile
              role
            }
            secondContact {
              id
              mobile
              role
            }
            isActive
            office {
              id
            }
        }
      }
     }
    """, variable_values={
        'clientData': {
            'id': to_global_id('ClientType', client_instance.id),
            'organisation': {
                'id': to_global_id(
                    'OrganisationType', 123),
                'mainLine': '2222222222',
                'website': 'www.hhh.com'
            },
            'contact': {
                'id': to_global_id(
                    'ContactType', client_instance.contact.id),
                'mobile': client_instance.contact.mobile,
                'role': 'OtherRole',
            },
            'secondContact': {
                'id': to_global_id(
                    'ContactType', client_instance.second_contact.id),
                'mobile': client_instance.second_contact.mobile,
                'role': 'Myrole',
            },
            'isActive': True,
            'office': {
                'id': client_instance.office_id
            }
        }
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_client_mutation5(snapshot):
    """Test a success update client mutation if second contact is missing"""

    client = Client(schema)
    client_instance = ClientFactory()
    update_xero_contact_patch = patch(
        'accounts.mutations.update_xero_contact.delay')
    with update_xero_contact_patch as mock_update_xero_contact:
        executed = client.execute("""
            mutation updateDetails($clientData: ClientInput!) {
            updateClientDetails(clientData: $clientData) {
              errors
              client {
                id
                organisation {
                  id
                  mainLine
                  website
                }
                contact {
                  id
                  mobile
                  role
                }
                secondContact {
                  id
                  mobile
                  role
                }
                isActive
                office {
                  id
                }
            }
          }
         }
        """, variable_values={
            'clientData': {
                'id': to_global_id('ClientType', client_instance.id),
                'organisation': {
                    'id': to_global_id(
                        'OrganisationType', client_instance.organisation_id),
                    'mainLine': '2222222222',
                    'website': 'www.hhh.com'
                },
                'contact': {
                    'id': to_global_id(
                        'ContactType', client_instance.contact.id),
                    'mobile': client_instance.contact.mobile,
                    'role': 'OtherRole',
                },
                'secondContact': {
                    'id': None,
                    'mobile': client_instance.second_contact.mobile,
                    'role': 'Myrole',
                },
                'isActive': True,
                'office': {
                    'id': client_instance.office_id
                }
            }
        })
        mock_update_xero_contact.assert_called_once_with(client_instance.id)
        snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_client_mutation6(snapshot):
    """Test a success update client mutation if second contact
        and organisation is missing"""

    client = Client(schema)
    client_instance = ClientFactory()

    executed = client.execute("""
        mutation updateDetails($clientData: ClientInput!) {
            updateClientDetails(clientData: $clientData) {
              errors
              client {
                id
                organisation {
                  id
                  mainLine
                  website
                }
                contact {
                  id
                  mobile
                  role
                }
                secondContact {
                  id
                  mobile
                  role
                }
                isActive
                office {
                  id
                }
            }
          }
     }
    """, variable_values={
        'clientData': {
            'id': to_global_id('ClientType', client_instance.id),
            'organisation': {
                'id': to_global_id(
                    'ContactType', client_instance.organisation.id),
                'mainLine': '2222222222',
                'website': 'www.hhh.com'
            },
            'contact': {
                'id': to_global_id(
                    'ContactType', client_instance.contact.id),
                'mobile': client_instance.contact.mobile,
                'role': 'OtherRole',
            },
            'secondContact': {
                'id': to_global_id(
                    'ContactType', 0),
                'mobile': client_instance.second_contact.mobile,
                'role': 'Myrole',
            },
            'isActive': True,
            'office': {
                'id': client_instance.office_id
            }
        }
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_client_mutation7(snapshot):
    """Test a success update client mutation if contact
        is doesn't exists"""

    client = Client(schema)
    client_instance = ClientFactory()

    executed = client.execute("""
        mutation updateDetails($clientData: ClientInput!) {
        updateClientDetails(clientData: $clientData) {
          errors
          client {
            id
            contact {
              id
              mobile
              role
            }
            isActive
            office {
              id
            }
        }
      }
     }
    """, variable_values={
        'clientData': {
            'id': to_global_id('ClientType', client_instance.id),
            'contact': {
                'id': to_global_id(
                    'ContactType', 1235),
                'mobile': client_instance.contact.mobile,
                'role': 'OtherRole',
            },
            'isActive': True,
            'office': {
                'id': client_instance.office_id
            }
        }
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_client_mutation8(snapshot):
    """Test a success updating client with missing
        organisation and second contact"""

    client = Client(schema)
    office = OfficeFactory(id=1)
    client_instance = ClientFactory()
    organisation = OrganisationFactory()
# update_xero_contact_patch = patch(
#     'accounts.mutations.update_xero_contact.delay')
# with update_xero_contact_patch as mock_update_xero_contact:
    executed = client.execute("""
        mutation updateDetails($clientData: ClientInput!) {
            updateClientDetails(clientData: $clientData) {
              errors
              client {
                id
                organisation {
                  id
                  mainLine
                  website
                }
                contact {
                  id
                  mobile
                  role
                }
                isActive
                office {
                  id
                }
            }
          }
     }
    """, variable_values={
        'clientData': {
            'id': to_global_id('ClientType', client_instance.id),
            'contact': {
                'id': to_global_id(
                    'ContactType', 1235),
                'mobile': client_instance.contact.mobile,
                'role': 'OtherRole',
            },
            'isActive': True,
            'office': {
                'id': client_instance.office_id
            }
        }
    })
    # mock_update_xero_contact.assert_called_once_with(client_instance.id)
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_remove_client_mutation(snapshot, request):
    """Test a success removing client"""

    staff_member = UserFactory()
    request.user = staff_member
    client = Client(schema, context=request)

    client_instance = ClientFactory()

    executed = client.execute("""
        mutation removeClient($instanceId: ID!, $instanceType: Int!) {
            removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
                errors
            }
        }
    """, variable_values={
        'instanceId': to_global_id('ClientType', client_instance.id),
        'instanceType': 3
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_remove_client_mutation2(snapshot, request):
    """Test a succes removing client with missing id"""

    staff_member = UserFactory()
    request.user = staff_member
    client = Client(schema, context=request)

    executed = client.execute("""
        mutation removeClient($instanceId: ID!, $instanceType: Int!) {
            removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
                errors
            }
        }
    """, variable_values={
        'instanceId': to_global_id('ClientType', 12121),
        'instanceType': 3
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_remove_client_mutation3(snapshot, request):
    """Test a failed removing client"""

    staff_member = UserFactory()
    request.user = staff_member
    client = Client(schema, context=request)
    matter = MatterFactory()
    client_instance = ClientFactory()
    client_instance.matters.add(matter)

    executed = client.execute("""
        mutation removeClient($instanceId: ID!, $instanceType: Int!) {
            removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
                errors
            }
        }
    """, variable_values={
        'instanceId': to_global_id('ClientType', client_instance.id),
        'instanceType': 3
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_remove_contact_mutation(snapshot, request):
    """Test a success removing contact"""

    staff_member = UserFactory()
    request.user = staff_member
    client = Client(schema, context=request)

    contact = ContactFactory()

    executed = client.execute("""
        mutation removeContact($instanceId: ID!, $instanceType: Int!) {
            removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
                errors
            }
        }
    """, variable_values={
        'instanceId': to_global_id('ContactType', contact.id),
        'instanceType': 1
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_remove_contact_mutation2(snapshot, request):
    """Test a failed removing contact"""

    staff_member = UserFactory()
    request.user = staff_member
    client = Client(schema, context=request)

    executed = client.execute("""
        mutation removeContact($instanceId: ID!, $instanceType: Int!) {
            removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
                errors
            }
        }
    """, variable_values={
        'instanceId': to_global_id('ContactType', 0),
        'instanceType': 1
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_remove_contact_mutation3(snapshot, request):
    """Test a failed removing contact"""

    staff_member = UserFactory()
    request.user = staff_member
    client = Client(schema, context=request)
    client_instance = ClientFactory()
    contact = ContactFactory()
    contact.clients.add(client_instance)

    executed = client.execute("""
        mutation removeContact($instanceId: ID!, $instanceType: Int!) {
            removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
                errors
            }
        }
    """, variable_values={
        'instanceId': to_global_id('ContactType', contact.id),
        'instanceType': 1
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_remove_organisation_mutation(snapshot, request):
    """Test a success removing organisation"""

    staff_member = UserFactory()
    request.user = staff_member
    client = Client(schema, context=request)

    organisation = OrganisationFactory()

    executed = client.execute("""
        mutation removeOrganisation($instanceId: ID!, $instanceType: Int!) {
            removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
                errors
            }
        }
    """, variable_values={
        'instanceId': to_global_id('OrganisationType', organisation.id),
        'instanceType': 2
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_remove_organisation_mutation2(snapshot, request):
    """Test a failed removing organisation"""

    staff_member = UserFactory()
    request.user = staff_member
    client = Client(schema, context=request)

    executed = client.execute("""
        mutation removeOrganisation($instanceId: ID!, $instanceType: Int!) {
            removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
                errors
            }
        }
    """, variable_values={
        'instanceId': to_global_id('OrganisationType', 0),
        'instanceType': 2
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_remove_organisation_mutation3(snapshot, request):
    """Test a failed removing organisation"""

    staff_member = UserFactory()
    request.user = staff_member
    client = Client(schema, context=request)
    client_instance = ClientFactory()
    organisation = OrganisationFactory()
    organisation.clients.add(client_instance)

    executed = client.execute("""
        mutation removeOrganisation($instanceId: ID!, $instanceType: Int!) {
            removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
                errors
            }
        }
    """, variable_values={
        'instanceId': to_global_id('OrganisationType', organisation.id),
        'instanceType': 2
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_create_contact_mutation3(snapshot):
    """ Test a success create contact mutation """

    occupation = OccupationFactory(id=1)
    client = Client(schema)
    contact = ContactFactory.build()

    executed = client.execute("""
        mutation createContact($contactData: ContactInput!) {
            createContact(contactData: $contactData) {
                errors
                contact {
                    fullName
                    mobile
                    email
                    occupation
                }
            }
        }
    """, variable_values={
        'contactData': {
            'email': contact.email,
            'firstName': '',
            'lastName': '',
            'mobile': contact.mobile,
            'occupation': occupation.id,
        }
    })

    snapshot.assert_match(executed)
