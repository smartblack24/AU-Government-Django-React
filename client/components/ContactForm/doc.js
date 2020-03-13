import { gql } from 'react-apollo'

export default gql`
  fragment ContactDetails on ContactType {
    email
    secondaryEmail
    firstName
    lastName
    middleName
    mobile
    salutation
    occupation
    skype
    directLine
    voi
    beverage
    isActive
    linkMails
    referrerId
    spouseId
    motherId
    fatherId
    dateOfBirth
    dateOfDeath
    placeOfBirth
    estimatedWealth
    preferredFirstName
    location {
      address1
      address2
      suburb
      state
      postCode
      country
    }
    postalLocation {
      address1
      address2
      suburb
      state
      postCode
      country
    }
  }
`
