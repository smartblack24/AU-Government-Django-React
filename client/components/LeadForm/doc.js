import { gql } from 'react-apollo'

export default gql`
  fragment MatterDetails on MatterType {
    name
    description
    conflictStatus
    conflictParties
    createdDate
    closedDate
    budget
    billingMethod
    billableStatus
    fundsInTrust
    matterStatus
    referrerThanked
    isReferrerThanked
    standardTermsSent
    isStandardTermsSent
    conflictCheckSent
    isConflictCheckSent
    filePath
    entryType
    leadDate
    leadStatus
    lost
    won
    client {
      id
    }
    principal {
      id
    }
    manager {
      id
    }
    assistant {
      id
    }
    matterType {
      id
    }
    matterSubType {
      id
    }
  }
`
