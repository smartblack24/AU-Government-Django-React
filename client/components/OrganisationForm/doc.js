import { gql } from 'react-apollo'

export default gql`
  fragment OrganisationDetails on OrganisationType {
    name
    mainLine
    website
    industryId
    linkMails
    groupStatus
    groupParent {
      id
    }
    businessSearchWords
    contacts
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
