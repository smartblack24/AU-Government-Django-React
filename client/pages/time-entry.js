import React from 'react'
import { graphql } from 'react-apollo'

import { getTimeEntry } from 'queries'
import withData from 'lib/withData'
import withAuth from 'lib/withAuth'
import Page from 'components/Page'
import TimeEntryForm from 'components/TimeEntryForm'
import LoadSpinner from 'components/LoadSpinner'

const TimeEntryPage = ({ data, user }) => {
  if (data.loading) {
    return (
      <Page user={user} wrappedByCard={false} pageTitle="Time Entry">
        <LoadSpinner />
      </Page>
    )
  }

  return (
    <Page user={user} pageTitle="Time Entry">
      <TimeEntryForm isEdit buttonTitle="Save" initialValues={data.timeEntry} lead={data.timeEntry.matter.entryType === 2} />
    </Page>
  )
}

export default withData(
  withAuth(
    graphql(getTimeEntry, { options: ({ url }) => ({ variables: { id: url.query.id } }) })(
      TimeEntryPage,
    ),
  ),
)
