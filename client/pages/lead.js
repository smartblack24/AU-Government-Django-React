import React from 'react'
import { graphql, gql } from 'react-apollo'

import Page from 'components/Page'
import withData from 'lib/withData'
import withAuth from 'lib/withAuth'
import LeadForm from 'components/LeadForm'
import LoadSpinner from 'components/LoadSpinner'
import { matterFragment } from 'fragments'

export const getMatter = gql`
  query matter($id: ID!) {
    matter(id: $id) {
      ...Matter
      leadStatus
      leadDate
      leadDate
    }
  }
  ${matterFragment}
`

class Lead extends React.PureComponent {
  render() {
    if (this.props.data.loading) {
      return (
        <Page user={this.props.user} wrappedByCard={false} pageTitle="Lead">
          <LoadSpinner />
        </Page>
      )
    }

    return (
      <Page user={this.props.user} wrappedByCard={false} pageTitle="Lead">
        <LeadForm
          initialValues={this.props.data.matter}
          user={this.props.user}
          buttonTitle="Save"
        />
      </Page>
    )
  }
}

export default withData(
  withAuth(
    graphql(getMatter, {
      options: ({ url }) => ({
        variables: { id: url.query.id },
      }),
    })(Lead),
  ),
)
