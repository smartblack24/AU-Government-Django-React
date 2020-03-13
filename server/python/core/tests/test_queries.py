import pytest

from sitename.schema import schema
from graphene.test import Client
from billing.factories import NoteFactory
from accounts.factories import (ClientFactory, ContactFactory, LocationFactory,
                                OrganisationFactory, UserFactory)
from ..factories import (IndustryFactory, MatterTypeFactory, OfficeFactory,
                         InvoiceStatusFactory, MatterStatusFactory,
                         OccupationFactory, SectionFactory, DocumentFactory,
                         MatterSubTypeFactory, DocumentTypeFactory)

from graphql_relay.node.node import to_global_id


@pytest.mark.django_db
def test_get_industries_query(snapshot, request):
    """ Test get industries query """

    IndustryFactory.create_batch(size=4)

    staff_member = UserFactory(id=1)
    request.user = staff_member
    client = Client(schema, context=request)
    query = client.execute("""
        query getIndustries {
            industries {
                name
            }
        }
    """)
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_get_matter_types_query(snapshot, request):
    """ Test get matter types query """

    MatterTypeFactory.create_batch(size=4)

    client = Client(schema)
    query = client.execute("""
        query getMatterTypes {
            matterTypes {
                name
            }
        }
    """)
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_get_matter_sub_types_query(snapshot, request):
    """ Test get matter sub types query """

    matter_type = MatterTypeFactory()
    MatterSubTypeFactory.create_batch(size=4, matter_type=matter_type)

    client = Client(schema)
    query = client.execute("""
        query getMatterSubTypes($matterTypeId: ID!) {
            matterSubTypes(matterTypeId: $matterTypeId) {
                name
            }
        }
    """, variable_values={
            'matterTypeId': matter_type.id,
        })
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_get_matter_sub_types_query_without_id(snapshot, request):
    """ Test get matter sub types query """

    MatterSubTypeFactory.create_batch(size=4)

    client = Client(schema)
    query = client.execute("""
        query getMatterSubTypes {
            matterSubTypes {
                name
            }
        }
    """)
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_get_invoice_statuses_query(snapshot, request):
    """ Test get invoice statuses query """

    InvoiceStatusFactory.create_batch(size=4)

    client = Client(schema)
    query = client.execute("""
        query getInvoiceStatuses {
            invoiceStatuses {
                name
            }
        }
    """)
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_get_offices_query(snapshot, request):
    """ Test get offices query """

    location_a = LocationFactory(suburb='Adelaide')
    location_s = LocationFactory(suburb='Sydney')
    location_unknow = LocationFactory(suburb='UnknowPlace')
    OfficeFactory.create_batch(size=2, location=location_a)
    OfficeFactory.create_batch(size=2, location=location_s)
    OfficeFactory.create_batch(size=2, location=location_unknow)

    client = Client(schema)
    query = client.execute("""
        query getOffices {
            offices {
                phone
                suburb
                name
                shortName
            }
        }
    """)
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_get_documents_query(snapshot, request):
    """ Test get documents query """

    DocumentFactory.create_batch(size=4)

    staff_member = UserFactory(id=1)
    request.user = staff_member
    client = Client(schema, context=request)
    query = client.execute("""
        query getDocuments {
            documents(first:3) {
                edges{
                    node {
                        status
                        statusDisplay
                        nominatedType
                        nominatedTypeDisplay
                        chargingClause
                        chargingClauseDisplay
                        documentType {
                            name
                        }
                    }
                }
            }
        }
    """)

    snapshot.assert_match(query)


@pytest.mark.django_db
def test_get_documents_query_with_contact_id(snapshot, request):
    """ Test get documents query with contact id """

    DocumentFactory.create_batch(size=4)
    contact = ContactFactory()
    staff_member = UserFactory(id=1)
    request.user = staff_member
    client = Client(schema, context=request)
    query = client.execute("""
        query getDocuments($contactId: ID!) {
            documents(first:3, contactId: $contactId) {
                edges{
                    node {
                        status
                        documentType {
                            name
                        }
                    }
                }
            }
        }
    """, variable_values={
            'contactId': to_global_id('ContactType', contact.id),
        })

    snapshot.assert_match(query)


@pytest.mark.django_db
def test_get_documents_query_with_organisation_id(snapshot, request):
    """ Test get documents query with organisation id """

    DocumentFactory.create_batch(size=4)
    organisation = OrganisationFactory()

    staff_member = UserFactory(id=1)
    request.user = staff_member
    client = Client(schema, context=request)
    query = client.execute("""
        query getDocuments($organisationId: ID!) {
            documents(first:3, organisationId: $organisationId) {
                edges{
                    node {
                        status
                        documentType {
                            name
                        }
                    }
                }
            }
        }
    """, variable_values={
            'organisationId': to_global_id(
                'OrganisationType',
                organisation.id
            ),
        })

    snapshot.assert_match(query)


@pytest.mark.django_db
def test_get_document_types_query(snapshot, request):
    """ Test get document types query """

    DocumentTypeFactory.create_batch(size=4)

    client = Client(schema)
    query = client.execute("""
        query documentTypes {
            documentTypes {
                name
            }
        }
    """)
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_get_sections_query(snapshot, request):
    """ Test get sections types query """

    SectionFactory.create_batch(size=4)

    client = Client(schema)
    query = client.execute("""
        query sections {
            sections {
                number
            }
        }
    """)
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_get_occupations_query(snapshot, request):
    """ Test get occupations query """

    OccupationFactory.create_batch(size=4)

    client = Client(schema)
    query = client.execute("""
        query getOccupations {
            occupations {
                name
            }
        }
    """)
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_get_occupation_by_id_query(snapshot, request):
    """ Test get occupation by id query """

    occupation = OccupationFactory()

    client = Client(schema)
    query = client.execute("""
        query getOccupation($occupationId: ID!) {
            occupation(occupationId: $occupationId) {
                name
            }
        }
    """,  variable_values={
            'occupationId': occupation.id,
        }
    )
    snapshot.assert_match(query)


@pytest.mark.django_db
def test_get_occupation_by_id_query_without_data(snapshot, request):
    """ Test get occupation by id query without data """

    occupation = OccupationFactory()

    client = Client(schema)
    query = client.execute("""
        query getOccupation($occupationId: ID!) {
            occupation(occupationId: $occupationId) {
                name
            }
        }
    """,  variable_values={
            'occupationId': occupation.id+66,
        }
    )
    snapshot.assert_match(query)
