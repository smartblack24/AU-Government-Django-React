import pytest

from sitename.schema import schema
from graphene.test import Client
from graphql_relay.node.node import to_global_id
from ..factories import DocumentFactory, SectionFactory, OfficeFactory
from accounts.factories import UserFactory


@pytest.mark.django_db
def test_remove_instance_mutation_without_data(snapshot, request):
    """Test a failed removing instance"""

    staff_member = UserFactory()
    request.user = staff_member
    client = Client(schema, context=request)

    executed = client.execute("""
        mutation removeInstance($instanceId: ID!, $instanceType: Int!) {
            removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
                errors
            }
        }
    """, variable_values={
        'instanceId': '',
        'instanceType': 0,
    })
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_create_document_mutation_with_section_id(snapshot, request):
    """ Test a success create document mutation with section id """

    document = DocumentFactory()
    request.user = UserFactory()
    section = document.section

    client = Client(schema, context=request)
    executed = client.execute("""
        mutation createDocument ($document: DocumentInput!) {
            createDocument (document: $document) {
                errors
                document {
                    section{
                        id
                    }
                }
            }
        }
    """, variable_values={
            'document': {
                'sectionId': section.id,
            }
        })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_create_document_mutation_without_section_id(snapshot, request):
    """ Test a success create document mutation without section id """

    request.user = UserFactory()

    client = Client(schema, context=request)
    executed = client.execute("""
        mutation createDocument ($document: DocumentInput!) {
            createDocument (document: $document) {
                errors
                document {
                    section{
                        id
                    }
                }
            }
        }
    """, variable_values={
            'document': {
                'sectionId': '',
            }
        })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_create_document_mutation_with_not_exist_section(snapshot, request):
    """ Test a success create document mutation with not exist section id """

    document = DocumentFactory()
    request.user = UserFactory()

    client = Client(schema, context=request)
    executed = client.execute("""
        mutation createDocument ($document: DocumentInput!) {
            createDocument (document: $document) {
                errors
                document {
                    section{
                        id
                    }
                }
            }
        }
    """, variable_values={
            'document': {
                'sectionId': '',
            }
        })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_document_mutation(snapshot, request):
    """ Test a success update document mutation """

    document = DocumentFactory()
    request.user = UserFactory()
    new_section = SectionFactory()
    client = Client(schema, context=request)
    executed = client.execute("""
        mutation updateDocument ($document: DocumentInput!) {
            updateDocument (document: $document) {
                errors
                document {
                    id
                    section{
                        id
                    }
                }
            }
        }
    """, variable_values={
            'document': {
                'documentId': to_global_id('DocumentType', document.id),
                'sectionId': new_section.id,
            }
        })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_document_mutation_with_not_exist_document(snapshot, request):
    """ Test a failure update document mutation with not exist document """

    request.user = UserFactory()
    new_section = SectionFactory()
    client = Client(schema, context=request)
    executed = client.execute("""
        mutation updateDocument ($document: DocumentInput!) {
            updateDocument (document: $document) {
                errors
                document {
                    id
                    section{
                        id
                    }
                }
            }
        }
    """, variable_values={
            'document': {
                'documentId': to_global_id('DocumentType', 1421242),
                'sectionId': new_section.id,
            }
        })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_section_mutation(snapshot, request):
    """ Test a success update section mutation """

    document = DocumentFactory()
    request.user = UserFactory()
    section = SectionFactory()
    new_office = OfficeFactory()
    client = Client(schema, context=request)
    executed = client.execute("""
        mutation updateSection ($sectionId: ID!,
                                $officeId: ID!,
                                $documentIds: [ID]!){
            updateSection (sectionId: $sectionId,
                           officeId: $officeId,
                           documentIds: $documentIds) {
                errors
            }
        }
    """, variable_values={
            'documentIds': [document.id, ],
            'sectionId': section.id,
            'officeId': new_office.id,
        })

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_update_section_mutation_with_incorrect_document_id(snapshot, request):
    """ Test a failure update section mutation with incorrect document id """

    document = DocumentFactory()
    request.user = UserFactory()
    section = SectionFactory()
    new_office = OfficeFactory()
    client = Client(schema, context=request)
    executed = client.execute("""
        mutation updateSection ($sectionId: ID!,
                                $officeId: ID!,
                                $documentIds: [ID]!){
            updateSection (sectionId: $sectionId,
                           officeId: $officeId,
                           documentIds: $documentIds) {
                errors
            }
        }
    """, variable_values={
            'documentIds': [
                to_global_id('DocumentType', document.id), ],
            'sectionId': section.id,
            'officeId': new_office.id,
        })

    snapshot.assert_match(executed)
