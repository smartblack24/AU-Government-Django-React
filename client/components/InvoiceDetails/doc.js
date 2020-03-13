import { gql } from 'react-apollo'

export const invoiceInfoDoc = gql`
  fragment InvoiceInfo on InvoiceType {
    matter {
      id
      client {
        id
      }
      description
      manager {
        id
      }
    }
    billingMethod
    createdDate
    dueDate
    status {
      id
    }
  }
`
