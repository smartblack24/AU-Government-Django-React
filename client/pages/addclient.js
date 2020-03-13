import React from 'react'
import { gql, graphql } from 'react-apollo'
import { filter } from 'graphql-anywhere'
import Router from 'next/router'

import { getClients } from 'pages/clients'
import { clientFragment } from 'fragments'
import Page from 'components/Page'
import withData from 'lib/withData'
import withAuth from 'lib/withAuth'
import ClientForm from 'components/ClientForm'
import doc from 'components/ClientForm/doc'

class AddClient extends React.Component {
  handleCreateClient = data =>
    new Promise((resolve, reject) => {
      this.props
        .mutate({
          variables: {
            clientData: filter(doc, data),
          },
          update: (store, { data: { createClient } }) => {
            try {
              const cache = store.readQuery({ query: getClients })

              cache.clients.edges.push({
                node: createClient.client,
                cursor: '',
                __typename: 'ClientType',
              })

              store.writeQuery({ query: getClients, data: cache })
            } catch (e) {} // eslint-disable-line
          },
        })
        .then((response) => {
          if (response.data.createClient.errors.length > 0) {
            console.log(response.data.createClient.errors)
            reject()
          } else {
            Router.push(
              `/client?id=${response.data.createClient.client.id}&created=true`,
              `/client/${response.data.createClient.client.id}`,
            )
            resolve()
          }
        })
    })
  render() {
    const { user } = this.props
    return (
      <Page user={user} wrappedByCard={false} pageTitle="Add a client">
        <ClientForm
          addingMode
          onSubmit={this.handleCreateClient}
          initialValues={{ isActive: 1 }}
          buttonTitle={'Save'}
        />
      </Page>
    )
  }
}

const createClient = gql`
  mutation createClient($clientData: ClientInput!) {
    createClient(clientData: $clientData) {
      errors
      client {
        ...Client
      }
    }
  }
  ${clientFragment}
`

export default withData(withAuth(graphql(createClient)(AddClient)))
