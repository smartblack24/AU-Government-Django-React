import { gql } from 'react-apollo'
import * as fragments from 'fragments'

export const getUser = gql`
  query me {
    me {
      ...User
    }
  }
  ${fragments.userFragment}
`

export const getProfile = gql`
  query user($id: ID!) {
    user(id: $id) {
      ...User
    }
  }
  ${fragments.userFragment}
`

export const getUsers = gql`
  query users {
    users {
      id
      fullName
    }
  }
`
export const getContacts = gql`
  query contacts {
    contacts {
      ...Contact
    }
  }
  ${fragments.contactFragment}
`

export const getContact = gql`
  query contact($id: ID!) {
    contact(id: $id) {
      ...Contact
    }
  }
  ${fragments.contactFragment}
`

export const getOrganisations = gql`
  query organisations {
    organisations {
      ...Organisation
    }
  }
  ${fragments.organisationFragment}
`

export const getOrganisation = gql`
  query organisation($id: ID!) {
    organisation(id: $id) {
      ...Organisation
    }
  }
  ${fragments.organisationFragment}
`

export const getClients = gql`
  query clients {
    clients {
      ...Client
    }
  }
  ${fragments.clientFragment}
`

export const getClient = gql`
  query client($id: ID!) {
    client(id: $id) {
      ...Client
    }
  }
  ${fragments.clientFragment}
`

export const getMatters = gql`
  query matters {
    matters {
      ...Matter
    }
  }
  ${fragments.matterFragment}
`

export const getMatter = gql`
  query matter($id: ID!) {
    matter(id: $id) {
      ...Matter
    }
  }
  ${fragments.matterFragment}
`

export const getTimeEntries = gql`
  query timeEntries {
    timeEntries {
      ...TimeEntry
    }
  }
  ${fragments.timeEntryFragment}
`

export const getTimeEntry = gql`
  query timeEntry($id: ID!) {
    timeEntry(id: $id) {
      ...TimeEntry
    }
  }
  ${fragments.timeEntryFragment}
`

export const getStandartDisbursements = gql`
  query standartDisbursements($name: String, $skip: Boolean!) {
    standartDisbursements(name_Icontains: $name) @skip(if: $skip) {
      edges {
        cursor
        node {
          ...StandartDisbursement
        }
      }
    }
  }
  ${fragments.standartDisbursementFragment}
`

export const getMinimalMatters = gql`
  query {
    matters {
      id
      name
      client {
        id
        name
      }
    }
  }
`

export const getMinimalUsers = gql`
  query {
    users {
      id
      fullName
      rate
    }
  }
`

export const getMinimalClients = gql`
  query {
    clients {
      id
      name
      matters(excludeStatus: 3) {
        id
        principal {
          id
        }
        manager {
          id
        }
        assistant {
          id
        }
      }
    }
  }
`

export const getInvoices = gql`
  query {
    invoices {
      ...Invoice
    }
  }
  ${fragments.invoiceFragment}
`

export const getInvoice = gql`
  query invoice($id: ID!) {
    invoice(id: $id) {
      ...Invoice
    }
  }
  ${fragments.invoiceFragment}
`

export const getIndustries = gql`
  query {
    industries {
      id
      name
    }
  }
`

export const getMatterTypes = gql`
  query matterTypes {
    matterTypes {
      id
      name
      subtypes {
        id
        name
      }
    }
  }
`

export const getMatterSubTypes = gql`
  query matterSubType($matterTypeId: ID) {
    matterSubTypes(matterTypeId: $matterTypeId) {
      id
      name
    }
  }
`

export const getNewMatterReports = gql`
  query newMattersReports {
    mattersPerYearReports {
      id
      month
      years {
        id
        name
        count
      }
    }
  }
`

export const getClientValueReports = gql`
  query clientValueReports($clients: [ID], $fromDate: String, $toDate: String, $skip: Boolean!) {
    clientValueReports(clients: $clients, fromDate: $fromDate, toDate: $toDate) @skip(if: $skip) {
      id
      name
      value
    }
  }
`

export const getInvoiceStatuses = gql`
  query invoiceStatuses {
    invoiceStatuses {
      id
      name
    }
  }
`

export const getDocuments = gql`
  query documents($contactId: ID, $organisationId: ID) {
    documents(contactId: $contactId, organisationId: $organisationId) {
      ...Document
    }
  }
  ${fragments.documentFragment}
`

export const getSections = gql`
  query sections {
    sections {
      ...Section
    }
  }
  ${fragments.sectionFragment}
`

export const getOffices = gql`
  query offices {
    offices {
      id
      suburb
      shortName
    }
  }
`

export const getMails = gql`
  query mails(
    $contactId: String,
    $organisationId: String,
    $matterId: String,
    $sender: String,
    $recipient: String,
    $subject: String,
    $dateFrom: String,
    $dateTo: String,
    $orderBy: String,
    $after: String
  ) {
    mails (
      contactId: $contactId
      organisationId: $organisationId
      matterId: $matterId
      sender: $sender
      recipient: $recipient
      subject: $subject
      dateFrom: $dateFrom
      dateTo: $dateTo
      orderBy: $orderBy
      first: 15
      after: $after
    ){
      totalPages
      edges {
        cursor
        node {
          id
          senderName
          senderAddress
          recipientName
          recipientAddress
          subject
          date
          hasAttachments
        }
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
`
