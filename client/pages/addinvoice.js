import React from 'react'
import { graphql } from 'react-apollo'

import { getMatter } from 'queries'
import Page from 'components/Page'
import withData from 'lib/withData'
import withAuth from 'lib/withAuth'
import InvoiceForm from 'components/InvoiceForm'
import LoadSpinner from 'components/LoadSpinner'

const AddInvoice = ({ data, user }) => {
  if (data.loading) {
    return (
      <Page user={user} pageTitle="Add an invoice">
        <LoadSpinner />
      </Page>
    )
  }

  const initialValues = {
    matter: data.matter,
    client: data.matter.client,
    fixedPriceItems: [],
  }

  return (
    <Page user={user} wrappedByCard={false} pageTitle="Add an invoice">
      <InvoiceForm initialValues={initialValues} />
    </Page>
  )
}

export default withData(
  withAuth(
    graphql(getMatter, { options: ({ url }) => ({ variables: { id: url.query.id } }) })(AddInvoice),
  ),
)
