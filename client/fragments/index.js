import { gql } from 'react-apollo'

export const locationFragment = gql`
  fragment Location on LocationType {
    id
    address1
    address2
    state
    postCode
    country
    suburb
    stateDisplay
  }
`

export const postalLocationFragment = gql`
  fragment PostalLocation on PostalLocationType {
    id
    postalAddress1
    postalAddress2
    postalSuburb
    postalState
    postalPostCode
    postalCountry
  }
`

export const noteFragment = gql`
  fragment Note on NoteType {
    id
    dateTime
    text
    user {
      id
      fullName
    }
  }
`

export const contactFragment = gql`
  fragment Contact on ContactType {
    id
    firstName
    lastName
    fullName
    middleName
    email
    mobile
    secondaryEmail
    skype
    voi
    isGeneral
    directLine
    salutation
    occupation
    beverage
    isActive
    preferredFirstName
    dateOfBirth
    dateOfDeath
    placeOfBirth
    estimatedWealth
    estimatedWealthDate
    addressesAreEquals
    linkMails
    notes {
      ...Note
    }
    children {
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
    spouse {
      id
      fullName
      spouse {
        id
      }
    }
    location {
      ...Location
    }
    postalLocation {
      ...PostalLocation
    }
    organisations {
      edges {
        cursor
        node {
          id
          name
        }
      }
    }
    referrer {
      id
      fullName
    }
    referrers {
      edges {
        cursor
        node {
          id
          fullName
        }
      }
    }
  }
  ${locationFragment},
  ${noteFragment},
  ${postalLocationFragment}
`

export const userFragment = gql`
  fragment User on UserType {
    id
    firstName
    lastName
    fullName
    email
    secondEmail
    photo
    mobile
    groups
    rate
    admissionDate
    salutation
    isActive
    canUseXero
    canDeleteMails
    canLinkMails
    gmail
    addressesAreEquals
    unitsToday
    unitsWeek
    unitsMonth
    mailEnabled
    location {
      ...Location
    }
    postalLocation {
      ...Location
    }
  }
  ${locationFragment}
`

export const organisationFragment = gql`
  fragment Organisation on OrganisationType {
    id
    name
    website
    mainLine
    businessSearchWords
    linkMails
    industry {
      id
      name
    }
    groupStatus
    groupParent {
      id
      name
    }
    addressesAreEquals
    location {
      ...Location
    }
    postalLocation {
      ...PostalLocation
    }
    contacts {
      edges {
        cursor
        node {
          id
          fullName
          secondContact {
            id
            fullName
          }
        }
      }
    }
  }
  ${locationFragment},
  ${postalLocationFragment}
`

export const clientFragment = gql`
  fragment Client on ClientType {
    id
    name
    isActive
    mattersCount
    invoicingAddress
    streetAddress
    office {
      id
      suburb
    }
    matters {
      edges {
        cursor
        node {
          id
          name
          leadStatus
          leadStatusDisplay
          entryType
          leadDate
          billableStatus
          billableStatusDisplay
        }
      }
    }
    organisation {
      id
      name
      mainLine
      website
      location {
        id
        stateDisplay
        postCode
      }
    }
    contact {
      id
      fullName
      mobile
      role
    }
    secondContact {
      id
      fullName
      mobile
      role
    }
  }
`
//
// const disbursementRecordedFragment = gql`
//   fragment DisbursementRecorded on TimeEntryType {
//     id
//     description
//     date
//     units
//     rate
//     cost
//     statusDisplay
//     gstStatusDisplay
//     gstStatus
//     entryType
//     staffMember {
//       id
//       fullName
//     }
//   }
// `

const timeEntryRecordedFragment = gql`
  fragment TimeEntryRecorded on TimeEntryType {
    id
    date
    units
    unitsToBill
    cost
    rate
    statusDisplay
    gstStatusDisplay
    gstStatus
    description
    billedValue
    entryType
    recordType
    staffMember {
      id
      fullName
    }
  }
`

export const matterTypeFragment = gql`
  fragment MatterType on MatterTypeType {
    id
    name
  }
`

export const matterFragment = gql`
  fragment Matter on MatterType {
    id
    name
    isPaid
    description
    daysOpen
    matterStatus
    leadStatus
    conflictStatus
    conflictParties
    createdDate
    leadDate
    fundsInTrust
    billableStatus
    billableStatusDisplay
    closedDate
    budget
    totalTimeValue
    totalTimeInvoiced
    totalInvoicedValue
    billingMethod
    amountOutstanding
    referrerThanked
    isReferrerThanked
    standardTermsSent
    isStandardTermsSent
    conflictCheckSent
    isConflictCheckSent
    wip
    filePath
    matterId
    entryType
    matterType {
      ...MatterType
    }
    matterSubType {
      id
    }
    invoices {
      edges {
        node {
          id
          number
          createdDate
          dueDate
          valueExGst
          valueInclGst
          netOutstanding
        }
      }
    }
    notes {
      ...Note
    }
    unbilledTime {
      ...TimeEntryRecorded
    }
    client {
      id
      name
    }
    principal {
      id
      fullName
    }
    manager {
      id
      fullName
    }
    assistant {
      id
      fullName
    }
  }
  ${matterTypeFragment}
  ${noteFragment}
  ${timeEntryRecordedFragment}
`

export const timeEntryFragment = gql`
  fragment TimeEntry on TimeEntryType {
    id
    description
    units
    unitsToBill
    date
    statusDisplay
    status
    gstStatus
    isBilled
    rate
    recordType
    invoice {
      id
    }
    staffMember {
      id
      fullName
    }
    client {
      id
      name
    }
    matter {
      id
      name
      entryType
      billableStatusDisplay
    }
  }
`

export const disbursementFragment = gql`
  fragment Disbursement on TimeEntryType {
    id
    description
    units
    rate
    date
    status
    gstStatus
    client {
      id
      name
    }
    matter {
      id
      name
    }
    staffMember {
      id
      fullName
    }
  }
`

export const standartDisbursementFragment = gql`
  fragment StandartDisbursement on StandartDisbursementType {
    id
    name
    description
    cost
    gstStatus
  }
`

export const fixedPriceItemFragment = gql`
  fragment FixedPriceItem on TimeEntryType {
    id
    date
    rate
    description
    status
    gstStatus
    cost
    gstStatusDisplay
    units
    unitsToBill
    entryType
    staffMember {
      id
      fullName
    }
  }
`

export const paymentFragment = gql`
  fragment Payment on PaymentType {
    id
    method
    methodDisplay
    amount
    date
  }
`

export const invoiceFragment = gql`
  fragment Invoice on InvoiceType {
    id
    number
    createdDate
    dueDate
    valueInclGst
    valueExGst
    billingMethod
    status {
      id
    }
    timeEntryValue
    fixedPriceValue
    statusDisplay
    receivedPayments
    netOutstanding
    history
    isPaid
    totalBilledValue
    friendlyReminder
    firstReminder
    secondReminder
    canSendXero
    isInXero
    # fixedPriceItems: timeEntries(entryType: "3") {
    #   edges {
    #     cursor
    #     node {
    #       ...FixedPriceItem
    #     }
    #   }
    # }
    payments {
      ...Payment
    }
    matter {
      id
      name
      description
      billingMethod
      totalTimeValue
      client {
        id
        name
      }
      manager {
        id
        fullName
      }
    }
    # disbursements: timeEntries(entryType: "2") {
    #   edges {
    #     cursor
    #     node {
    #       ...DisbursementRecorded
    #     }
    #   }
    # }
    # timeEntries(entryType: "1") {
    #   edges {
    #     cursor
    #     node {
    #       ...TimeEntryRecorded
    #     }
    #   }
    # }
  }
  ${paymentFragment}
`

export const mailFragment = gql`
  fragment Mail on MailType {
    id
    senderName
    senderAddress
    recipientName
    recipientAddress
    subject
    date
    attachments {
      id
      data
      name
      size
      contentType
    }
    matter {
      id
      name
    }
    availableMatters {
      id
      name
      billableStatusDisplay
    }
  }
`

export const sectionFragment = gql`
  fragment Section on SectionType {
    id
    number
    office {
      id
      shortName
    }
  }
`

export const documentFragment = gql`
  fragment Document on DocumentType {
    id
    contact {
      id
      fullName
    }
    organisation {
      id
      name
    }
    owner {
      id
      fullName
    }
    section {
      ...Section
    }
    documentType {
      id
      name
    }
    date
    dateRemoved
    status
    statusDisplay
    notes
    nominatedType
    nominatedTypeDisplay
    nominatedNames
    andrewExecutor
    chargingClause
    chargingClauseDisplay
  }
  ${sectionFragment}
`
