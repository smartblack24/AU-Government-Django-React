import React from 'react'
import { graphql, withApollo } from 'react-apollo'
import { toast } from 'react-toastify'

import Page from 'components/Page'
import withData from 'lib/withData'
import withAuth from 'lib/withAuth'
import { getClient } from 'queries'
import ClientForm from 'components/ClientForm'
import LoadSpinner from 'components/LoadSpinner'

class Client extends React.Component {
  componentDidMount = () => {
    if (this.props.url.query.created) {
      toast.success('The changes have been saved!')
    }
  }

  render() {
    const { data, user } = this.props
    if (data.loading) {
      return (
        <Page user={user}>
          <LoadSpinner />
        </Page>
      )
    }

    return (
      <Page user={user} wrappedByCard={false} pageTitle={data.client.name}>
        <ClientForm initialValues={data.client} editable={false} buttonTitle={'Save'} />
      </Page>
    )
  }
}

export default withData(
  withAuth(
    withApollo(
      graphql(getClient, {
        options: ({ url }) => ({
          variables: { id: url.query.id },
        }),
      })(Client),
    ),
  ),
)
