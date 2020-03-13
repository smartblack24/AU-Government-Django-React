import React from 'react'
import { graphql, withApollo } from 'react-apollo'

import Page from 'components/Page'
import withData from 'lib/withData'
import withAuth from 'lib/withAuth'
import OrganisationForm from 'components/OrganisationForm'
import { getOrganisation } from 'queries'
import LoadSpinner from 'components/LoadSpinner'

const Organisation = ({ data, user }) => {
  if (data.loading) {
    return (
      <Page user={user} wrappedByCard={false} pageTitle=" ">
        <LoadSpinner />
      </Page>
    )
  }

  return (
    <Page user={user} wrappedByCard={false} pageTitle={data.organisation.name}>
      <OrganisationForm buttonTitle="Save" initialValues={data.organisation} />
    </Page>
  )
}

export default withData(
  withAuth(
    withApollo(
      graphql(getOrganisation, {
        options: ({ url }) => ({
          variables: { id: url.query.id },
          fetchPolicy: 'cache-first',
        }),
      })(Organisation),
    ),
  ),
)
