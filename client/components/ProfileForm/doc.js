import { gql } from 'react-apollo'

export default gql`
  fragment UserDetails on UserType {
    email
    secondEmail
    firstName
    lastName
    rate
    isActive
    mobile
    admissionDate
    salutation
    photo
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
