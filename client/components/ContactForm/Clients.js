import React from 'react'
import { gql, graphql } from 'react-apollo'

import LoadSpinner from 'components/LoadSpinner'

const getClients = gql`
  query ContactClients($contactId: ID!) {
    contact(id: $contactId) {
      id
      clients {
        edges {
          cursor
          node {
            id
            name
          }
        }
      }
      secondClients {
        edges {
          cursor
          node {
            id
            name
          }
        }
      }
    }
  }
`
const Clients = ({ data }) => {
  if (data.loading) {
    return <LoadSpinner />
  }
  const contacts = data.contact.secondClients.edges.concat(data.contact.clients.edges)
  return (
    <div>
      <div className="table-responsive">
        <table className="table table-bordered">
          <thead>
            <tr>
              <th>Clients</th>
            </tr>
          </thead>
          <tbody>
            {contacts.length > 0 ? (
              contacts.map(({ node }) => (
                <tr key={node.id} className="org-item">
                  <td>
                    <a href={`/client/${node.id}`} target="_blank">
                      {node.name}
                    </a>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td>No clients</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default graphql(getClients)(Clients)
