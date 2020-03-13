import { gql } from 'react-apollo';

export default gql`
  fragment CreateOrganisation on OrganisationType {
    name
    mainLine
    website
    industryId
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
`;
