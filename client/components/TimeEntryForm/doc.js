import { gql } from 'react-apollo'

export default gql`
  fragment TimeEntryDetails on MatterType {
    description
    client {
      id
    }
    staffMember {
      id
    }
    matter {
      id
    }
    units
    status
    date
    time
    gstStatus
    rate
    recordType
  }
`
