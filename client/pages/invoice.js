import React from 'react'
import { graphql } from 'react-apollo'
import gql from 'graphql-tag'
// import { getInvoice } from 'queries'
import Page from 'components/Page'
import LoadSpinner from 'components/LoadSpinner'
import InvoiceDetail from 'components/InvoiceDetails'
import withData from 'lib/withData'
import withAuth from 'lib/withAuth'

const getInvoice = gql`
  query invoice($id: ID!) {
    invoice(id: $id) {
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
      payments {
        id
        method
        methodDisplay
        amount
        date
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
    }
  }
`

const Invoice = ({ data, user }) => {
  if (data.loading) {
    return (
      <Page user={user} pageTitle="Invoice details">
        <LoadSpinner />
      </Page>
    )
  }

  return (
    <Page user={user} wrappedByCard={false} pageTitle="Invoice details">
      <InvoiceDetail user={user} initialValues={data.invoice} />
    </Page>
  )
}

export default withData(
  withAuth(
    graphql(getInvoice, {
      options: ({ url }) => ({
        variables: { id: url.query.id },
      }),
    })(Invoice),
  ),
)
