import datetime
import factory
from core.factories import IndustryFactory, OccupationFactory, OfficeFactory
from factory import fuzzy


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'accounts.User'
        django_get_or_create = ('email',)

    first_name = factory.Sequence(lambda n: 'john%s' % n)
    last_name = factory.Sequence(lambda n: 'johnson%s' % n)
    email = factory.LazyAttribute(lambda o: '%s@example.org' % o.first_name)


class LocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'accounts.Location'

    address1 = factory.Sequence(lambda n: 'address%s' % n)
    address2 = factory.Sequence(lambda n: 'address%s' % n)
    suburb = factory.Sequence(lambda n: 'suburb%s' % n)
    state = 1
    post_code = '12345'
    country = 'Australia'


class ContactFactory(UserFactory, factory.django.DjangoModelFactory):
    class Meta:
        model = 'accounts.Contact'

    first_name = factory.Sequence(lambda n: 'Bob%s' % n)
    last_name = factory.Sequence(lambda n: 'Smith%s' % n)
    email = factory.LazyAttribute(lambda o: '%s@gmail.com' % o.first_name)
    occupation = factory.SubFactory(OccupationFactory)
    mobile = '1231231'

    @factory.post_generation
    def _spouses(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of spouses were passed in, use them
            for spouse in extracted:
                self._spouses.add(spouse)

    @factory.post_generation
    def organisations(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of organisations were passed in, use them
            for org in extracted:
                self.organisations.add(org)


class OrganisationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'accounts.Organisation'

    name = factory.Sequence(lambda n: 'Organisation %s' % n)
    industry = factory.SubFactory(IndustryFactory)
    group_status = fuzzy.FuzzyInteger(1, 2)
    location = factory.SubFactory(LocationFactory)


class ClientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'accounts.Client'

    contact = factory.SubFactory(ContactFactory)
    second_contact = factory.SubFactory(ContactFactory)
    organisation = factory.SubFactory(OrganisationFactory)
    office = factory.SubFactory(OfficeFactory)
    created_date = fuzzy.FuzzyNaiveDateTime(
        datetime.datetime(2017, 1, 1),
        datetime.datetime.now()
        )
