import graphene
from core.inputs import IDField
from core.scalars import Decimal


class LocationInput(graphene.InputObjectType):
    address1 = graphene.String()
    address2 = graphene.String()
    suburb = graphene.String()
    state = graphene.Int()
    post_code = graphene.String()
    country = graphene.String()


class UserInput(graphene.InputObjectType):
    email = graphene.String()
    second_email = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    rate = graphene.Float()
    is_active = graphene.Boolean()
    mobile = graphene.String()
    admission_date = graphene.String()
    salutation = graphene.Int()
    photo = graphene.String()
    location = graphene.InputField(LocationInput)
    postal_location = graphene.InputField(LocationInput)


class ClientContactInput(graphene.InputObjectType):
    id = graphene.ID()
    mobile = graphene.String()
    role = graphene.String()


class ClientOrganisationInput(graphene.InputObjectType):
    id = graphene.ID()
    main_line = graphene.String()
    website = graphene.String()


class ClientInput(graphene.InputObjectType):
    id = graphene.ID()
    organisation = graphene.InputField(ClientOrganisationInput)
    contact = graphene.InputField(ClientContactInput)
    second_contact = graphene.InputField(ClientContactInput)
    office = graphene.InputField(IDField)
    is_active = graphene.Boolean()


class RelationshipInput(graphene.InputObjectType):
    contact_id = graphene.ID()
    referrer_id = graphene.ID()
    spouse_id = graphene.ID()
    mother_id = graphene.ID()
    father_id = graphene.ID()


class ContactInput(graphene.InputObjectType):
    email = graphene.String()
    secondary_email = graphene.String()
    first_name = graphene.String()
    middle_name = graphene.String()
    last_name = graphene.String()
    mobile = graphene.String()
    salutation = graphene.Int()
    occupation = graphene.Int()
    skype = graphene.String()
    direct_line = graphene.String()
    voi = graphene.Boolean()
    beverage = graphene.String()
    is_active = graphene.Boolean()
    organisations = graphene.List(graphene.ID)
    referrer_id = graphene.ID()
    spouse_id = graphene.ID()
    mother_id = graphene.ID()
    father_id = graphene.ID()
    date_of_birth = graphene.String()
    date_of_death = graphene.String()
    place_of_birth = graphene.String()
    estimated_wealth = Decimal()
    preferred_first_name = graphene.String()
    location = graphene.InputField(LocationInput)
    postal_location = graphene.InputField(LocationInput)
    link_mails = graphene.Boolean()


class OrganisationInput(graphene.InputObjectType):
    name = graphene.String()
    main_line = graphene.String()
    website = graphene.String()
    industry_id = graphene.ID()
    group_status = graphene.Int()
    group_parent = graphene.InputField(IDField)
    business_search_words = graphene.String()
    contacts = graphene.List(graphene.ID)
    location = graphene.InputField(LocationInput)
    postal_location = graphene.InputField(LocationInput)
    link_mails = graphene.Boolean()
