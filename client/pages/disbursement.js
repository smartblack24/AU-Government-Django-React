import React from 'react'
import { graphql } from 'react-apollo'

import { getTimeEntry } from 'queries'
import withData from 'lib/withData'
import withAuth from 'lib/withAuth'
import Page from 'components/Page'
import TimeEntryForm from 'components/TimeEntryForm'
import LoadSpinner from 'components/LoadSpinner'

const DisbursementPage = ({ data, user }) => {
  if (data.loading) {
    return (
      <Page user={user} wrappedByCard={false} pageTitle="Disbursement">
        <LoadSpinner />
      </Page>
    )
  }

  return (
    <Page user={user} pageTitle="Disbursement">
      <TimeEntryForm
        entryType={2}
        editable={false}
        isEdit
        buttonTitle="Save"
        initialValues={data.timeEntry}
      />
    </Page>
  )
}

export default withData(
  withAuth(
    graphql(getTimeEntry, { options: ({ url }) => ({ variables: { id: url.query.id } }) })(
      DisbursementPage,
    ),
  ),
)
