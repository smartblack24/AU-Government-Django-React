import React from 'react'
import moment from 'moment'

import Page from 'components/Page'
import withData from 'lib/withData'
import withAuth from 'lib/withAuth'
import TimeEntryForm from 'components/TimeEntryForm'

export default withData(
  withAuth(({ user }) => (
    <Page user={user} pageTitle="Add a disbursement">
      <TimeEntryForm
        buttonTitle="Add"
        entryType={2}
        initialValues={{
          status: 1,
          gstStatus: 1,
          date: moment().format(),
          staffMember: user,
        }}
      />
    </Page>
  )),
)
