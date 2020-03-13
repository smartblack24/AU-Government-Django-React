import React from 'react'
import { graphql } from 'react-apollo'

import Page from 'components/Page'
import withData from 'lib/withData'
import withAuth from 'lib/withAuth'
import MatterForm from 'components/MatterForm'
import LoadSpinner from 'components/LoadSpinner'
import { getMatter } from 'queries'

class Matter extends React.PureComponent {
  render() {
    if (this.props.data.loading) {
      return (
        <Page user={this.props.user} wrappedByCard={false} pageTitle="Matter">
          <LoadSpinner />
        </Page>
      )
    }

    return (
      <Page user={this.props.user} wrappedByCard={false} pageTitle="Matter">
        <MatterForm
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
        fetchPolicy: 'cache-and-network',
      }),
    })(Matter),
  ),
)
