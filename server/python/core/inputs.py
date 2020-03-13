import graphene


class IDField(graphene.InputObjectType):
    id = graphene.ID(requried=True)


class DocumentInput(graphene.InputObjectType):
    contact_id = graphene.ID()
    organisation_id = graphene.ID()
    document_id = graphene.ID()
    date = graphene.String()
    date_removed = graphene.String()
    status = graphene.Int()
    notes = graphene.String()
    document_type_id = graphene.Int()
    nominated_type = graphene.String()
    nominated_names = graphene.String()
    andrew_executor = graphene.Boolean()
    charging_clause = graphene.Int()
    section_id = graphene.ID()
