import { gql } from 'react-apollo'

export default gql`
  fragment ClientDetails on ClientType {
    id
    organisation {
      id
      mainLine
      website
    }
    contact {
      id
      mobile
      role
    }
    secondContact {
      id
      mobile
      role
    }
    isActive
    office {
      id
    }
  }
`
