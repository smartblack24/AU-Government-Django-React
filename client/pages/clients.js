import React, { Component } from 'react'
import Link from 'next/link'
import { graphql, gql, compose } from 'react-apollo'
import swal from 'sweetalert'
import { connect } from 'react-redux'
import { CLIENTS_LOADING_STATUS } from 'constants/page'
import Page from 'components/Page'
import withData from 'lib/withData'
import withAuth from 'lib/withAuth'
import Button from 'components/Button'
import PaginateTable from 'components/PaginateTable'
import Searchable from 'components/Searchable'
import LineLoader from 'components/LineLoader'
import RemoveIcon from 'components/RemoveIcon'
import { swalCreator } from 'utils'
import { getOrganisations } from './organisations'
import { getContacts } from './contacts'

const removeClient = gql`
  mutation removeClient($instanceId: ID!, $instanceType: Int!) {
    removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
      errors
    }
  }
`

export const getClients = gql`
  query getClients($after: String, $name: String) {
    clients(first: 15, after: $after, name: $name) {
      totalPages
      edges {
        node {
          id
          mattersCount
          name
          organisation {
            id
            name
            mainLine
          }
          secondContact {
            id
            fullName
            mobile
          }
          contact {
            id
            fullName
            mobile
          }
        }
        cursor
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
`

const createAllContactsInXero = gql`
  mutation createAllContactsInXero {
    createAllContactsInXero {
      success
      errors
    }
  }
`

class Clients extends Component {
  state = {
    creatingAllContacts: false,
  }

  handleRemoveClient = (clientId) => {
    const { data } = this.props

    swal({
      title: 'Confirmation',
      text: 'Are you sure?',
      icon: 'warning',
      buttons: {
        cancel: true,
        confirm: {
          closeModal: false,
        },
      },
    }).then((willDelete) => {
      if (willDelete) {
        const { variables } = data
        this.props.mutate({
          variables: {
            instanceId: clientId,
            instanceType: 3,
          },
          refetchQueries: [
            { query: getContacts, options: { fetchPolicy: 'network-only' } },
            { query: getOrganisations, options: { fetchPolicy: 'network-only' } },
          ],
          update: (store, { data: { removeInstance } }) => {
            if (removeInstance.errors.length === 0) {
              const cache = store.readQuery({
                query: getClients,
                variables,
              })

              const index = cache.clients.edges.findIndex(client => client.node.id === clientId)

              if (index > -1) {
                cache.clients.edges = cache.clients.edges
                  .slice(0, index)
                  .concat(cache.clients.edges.slice(index + 1, cache.clients.edges.length))
              }

              store.writeQuery({
                query: getClients,
                data: cache,
                variables,
              })
            }
          },
        }).then((response) => {
          if (response.data.removeInstance.errors.length > 0) {
            const msg = response.data.removeInstance.errors.join('\n')
            swal({ text: msg, icon: 'error' })
          } else {
            swal({
              icon: 'success',
              text: 'The client has been removed successfully',
            })
          }
        })
      }
    })
  }

  handleCreateAllContactsInXero = async () => {
    this.setState({ creatingAllContacts: true })

    const res = await this.props.createAllContactsInXero()

    this.setState({ creatingAllContacts: false })

    const { success, errors } = res.data.createAllContactsInXero

    swalCreator({ success, errors, successMsg: 'Creating contacts in Xero is in progress...' })
  }

  render() {
    const { user, data, dataLoading } = this.props
    const { creatingAllContacts } = this.state

    const { canUseXero } = user

    return (
      <Page user={user} pageTitle="Clients">
        <Searchable
          searchableField="name"
          data={data}
          dataKey="clients"
          filterInputPlaceholder="Filter clients"
        >
          {({ filterComponent }) => (
            <div>
              <div className="row justify-content-between mb-3">
                <div className="col col-md-3">{filterComponent}</div>
                <div className="col col-md-auto">
                  {canUseXero && <Button
                    className="btn btn-primary mr-3"
                    icon="fa fa-address-book"
                    loading={creatingAllContacts}
                    title="Create all contacts In Xero"
                    onClick={this.handleCreateAllContactsInXero}
                  />}
                  <Link href="/addclient" as="/clients/add" prefetch>
                    <a className="btn btn-info">
                      <i className="fa fa-plus" /><span>Add</span>
                    </a>
                  </Link>
                </div>
              </div>
              {dataLoading && <LineLoader />}
              <PaginateTable
                detailPageAccessor="client"
                columns={[
                  {
                    Header: 'Client name',
                    id: 'clientName',
                    accessor: 'name',
                  },
                  {
                    Header: 'Org Main phone',
                    id: 'orgMainPhone',
                    maxWidth: 200,
                    className: 'text-center',
                    accessor: item => item.organisation.mainLine,
                  },
                  {
                    Header: 'Contact name',
                    id: 'contactName',
                    accessor: item => [item.contact && item.contact.fullName,
                      item.secondContact && ' and '.concat(item.secondContact.fullName)],
                  },
                  {
                    Header: 'Contact phone',
                    maxWidth: 150,
                    className: 'text-center',
                    id: 'contactPhone',
                    accessor: item => item.contact && item.contact.mobile,
                  },
                  {
                    Header: 'Matter',
                    id: 'hasMatter',
                    maxWidth: 80,
                    className: 'text-center',
                    accessor: item => item.mattersCount.length,
                    Cell: ({ original }) =>
                      (original.mattersCount > 0 ? (
                        <span className="success">Yes</span>
                      ) : (
                        <strong>
                          <span>No</span>
                        </strong>
                      )),
                  },
                  {
                    sortable: false,
                    resizable: false,
                    minWidth: 10,
                    className: 'text-center',
                    getProps: () => ({ onClick: null }),
                    Cell: ({ original }) => (
                      <RemoveIcon value={original.id} onClick={this.handleRemoveClient} />
                    ),
                  },
                ]}
                defaultSorted={[
                  {
                    id: 'clientName',
                    desc: false,
                  },
                ]}
              />
            </div>
          )}
        </Searchable>
      </Page>
    )
  }
}

export default withData(
  withAuth(
    compose(
      graphql(removeClient),
      graphql(createAllContactsInXero, { name: 'createAllContactsInXero' }),
      graphql(getClients, { options: { notifyOnNetworkStatusChange: true } }),
      connect(state => ({ dataLoading: state.page.get(CLIENTS_LOADING_STATUS) })),
    )(Clients),
  ),
)
