from datetime import date

import pytest

from ..factories import (ClientFactory, ContactFactory, LocationFactory,
                         OrganisationFactory, UserFactory)
from ..utils import format_address


@pytest.mark.django_db
def test_user():
    """ Test User model """

    user = UserFactory()

    assert user.rate == 0
    assert user.admission_date == date.today()
    assert user.full_name == "{} {}".format(user.first_name, user.last_name)
    assert user.get_short_name() == user.first_name
    assert str(user) == user.full_name


@pytest.mark.django_db
def test_location():
    """ Test Location model """

    location = LocationFactory()
    not_eq_location = LocationFactory()

    assert str(location) == "{}, {}, {}, {}, {}".format(
        location.address1,
        location.address2,
        location.suburb,
        location.get_state_display(),
        location.country
    )

    assert location.__eq__(not_eq_location) == False
    assert location.__eq__(None) == False
    assert location.__eq__(location) == True


@pytest.mark.django_db
def test_contact():
    """ Test Contact model """

    spouse = ContactFactory()
    contact = ContactFactory(_spouses=(spouse,))
    child1 = ContactFactory(father=contact)
    child2 = ContactFactory(mother=contact)

    assert contact.full_name == "{} {}".format(
        contact.first_name,
        contact.last_name
    )
    assert str(contact) == contact.full_name
    assert contact.formatted_postal_address is None
    assert contact.formatted_street_address is None
    assert contact.get_spouse() == spouse

    spouse2 = ContactFactory()
    # change spouse of the contact
    contact.set_spouse(spouse2.id)

    assert contact.get_spouse() == spouse2

    contact.remove_spouse()

    assert contact.get_spouse() is None
    assert contact.children == [child1, child2]


@pytest.mark.django_db
def test_organisation():
    """ Test Organisation model """

    organisation = OrganisationFactory()

    assert str(organisation) == organisation.name
    assert organisation.formatted_street_address == str(
        organisation.formatted_street_address)


@pytest.mark.django_db
def test_client():
    """ Test Client model """

    client = ClientFactory()

    assert str(client) == "{} - {} and {}".format(
        client.organisation.name,
        client.contact.full_name,
        client.second_contact.full_name,
    )

    client = ClientFactory(second_contact=None)

    assert str(client) == "{} - {}".format(
        client.organisation.name,
        client.contact.full_name,
    )

    client = ClientFactory(contact=None)

    assert str(client) == "{} - {}".format(
        client.organisation.name,
        client.second_contact.full_name,
    )

    client = ClientFactory(organisation=None)

    assert str(client) == "{} and {}".format(
        client.contact.full_name,
        client.second_contact.full_name,
    )

    client = ClientFactory(contact=None, second_contact=None)

    assert str(client) == client.organisation.name

    client = ClientFactory(organisation=None, contact=None)

    assert str(client) == client.second_contact.full_name

    client = ClientFactory(organisation=None, second_contact=None)

    assert str(client) == client.contact.full_name

    client = ClientFactory(
        organisation=None, contact=None, second_contact=None)

    assert str(client) == "Have neither Organisation or Contact associated"

    assert client.has_matter is bool(client.matters.count())

    client = ClientFactory(organisation=None)

    assert client.invoicing_location == client.contact.postal_location
    assert client.invoicing_address == ''

    client = ClientFactory()

    assert client.invoicing_location == client.organisation.postal_location
    assert client.invoicing_address == ''
