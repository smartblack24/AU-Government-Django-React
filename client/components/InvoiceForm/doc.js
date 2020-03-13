import { gql } from 'react-apollo'

export default gql`
  fragment InvoiceDoc on InvoiceType {
    id
    billingMethod
    matter {
      id
      description
      budget
      client {
        id
      }
    }
    fixedPriceItems
  }
`
