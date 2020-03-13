import graphene
from accounts.mutations import (CheckResetPasswordToken, CreateClientMutation,
                                CreateContactMutation,
                                CreateOrganisationMutation, LoginMutation,
                                RegisterMutation, ResetPassword,
                                SendResetPasswordEmail, UpdateClientDetails,
                                UpdateContactMutation,
                                UpdateOrganisationAssociation,
                                UpdateOrganisationDetailsMutation,
                                UpdateOrganisationLocationMutation,
                                UpdateOrganisationsMutation,
                                UpdateRelationshipsMutation,
                                UpdateUserMutation,
                                CreateAllContactsInXeroMutation,
                                SyncMailsMutation)
from accounts.schema import Query as AccountsQuery
from billing.mutations import (CreateMatterMutation, CreateNoteMutation,
                               CreateTimeEntryMutation, UpdateMatterMutation,
                               UpdateNoteMutation, UpdateTimeEntryMutation,
                               LostMatterMutation, WinMatterMutation)
from billing.schema import Query as BillingQuery
from core.mutations import (CreateDocument, RemoveInstanceMutation,
                            UpdateDocument, UpdateSection)
from core.schema import Query as CoreQuery
from gmailbox.mutations import (ActivateGmailAccountMutation, DeactivateGmailAccountMutation,
                                UpdateMailMatterMutation, UpdateMailsMatterMutation,
                                DeleteMailsMutation, HideMailMutation)
from gmailbox.schema import Query as MailQuery
from invoicing.mutations import (AddPaymentMutation, CreateFixedPriceItem,
                                 CreateInvoiceMutation, RemoveFixedPriceItem,
                                 RemoveTimeRecordMutation, SendInvoiceEmail,
                                 SendInvoiceToXero, FetchPaymentsFromXero,
                                 FetchAllPaymentsFromXero,
                                 UpdateFixedPriceItem,
                                 UpdateInvoiceInfoMutation,
                                 UpdateInvoiceMutation)
from invoicing.schema import Query as InvoiceQuery
from reporting.schema import Query as ReportingQuery


class Mutation(graphene.ObjectType):
    register = RegisterMutation.Field()
    login = LoginMutation.Field()
    update_contact = UpdateContactMutation.Field()
    create_contact = CreateContactMutation.Field()
    update_organisations = UpdateOrganisationsMutation.Field()
    update_referrer = UpdateRelationshipsMutation.Field()
    update_organisation_details = UpdateOrganisationDetailsMutation.Field()
    update_organisation_location = UpdateOrganisationLocationMutation.Field()
    update_organisation_association = UpdateOrganisationAssociation.Field()
    create_organisation = CreateOrganisationMutation.Field()
    update_user = UpdateUserMutation.Field()
    remove_instance = RemoveInstanceMutation.Field()
    update_client_details = UpdateClientDetails.Field()
    lost_matter = LostMatterMutation.Field()
    win_matter = WinMatterMutation.Field()
    update_matter = UpdateMatterMutation.Field()
    create_matter = CreateMatterMutation.Field()
    create_client = CreateClientMutation.Field()
    create_time_entry = CreateTimeEntryMutation.Field()
    create_note = CreateNoteMutation.Field()
    update_note = UpdateNoteMutation.Field()
    update_time_entry = UpdateTimeEntryMutation.Field()
    create_invoice = CreateInvoiceMutation.Field()
    update_invoice_info = UpdateInvoiceInfoMutation.Field()
    update_invoice = UpdateInvoiceMutation.Field()
    remove_time_record = RemoveTimeRecordMutation.Field()
    add_payment = AddPaymentMutation.Field()
    activate_gmail_account = ActivateGmailAccountMutation.Field()
    deactivate_gmail_account = DeactivateGmailAccountMutation.Field()
    update_mail_matter = UpdateMailMatterMutation.Field()
    update_mails_matter = UpdateMailsMatterMutation.Field()
    delete_mails = DeleteMailsMutation.Field()
    hide_mail = HideMailMutation.Field()
    create_document = CreateDocument.Field()
    update_document = UpdateDocument.Field()
    update_section = UpdateSection.Field()
    create_fixed_price_item = CreateFixedPriceItem.Field()
    update_fixed_price_item = UpdateFixedPriceItem.Field()
    remove_fixed_price_item = RemoveFixedPriceItem.Field()
    send_invoice_email = SendInvoiceEmail.Field()
    send_invoice_to_xero = SendInvoiceToXero.Field()
    fetch_payments_from_xero = FetchPaymentsFromXero.Field()
    fetch_all_payments_from_xero = FetchAllPaymentsFromXero.Field()
    create_all_contacts_in_xero = CreateAllContactsInXeroMutation.Field()
    send_reset_password_email = SendResetPasswordEmail.Field()
    check_reset_password_token = CheckResetPasswordToken.Field()
    reset_password = ResetPassword.Field()
    sync_mails = SyncMailsMutation.Field()


class Query(
    ReportingQuery,
    AccountsQuery,
    BillingQuery,
    InvoiceQuery,
    CoreQuery,
    MailQuery,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
