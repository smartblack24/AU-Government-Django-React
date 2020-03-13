import React from 'react'
import PropTypes from 'prop-types'
import { gql, graphql, compose } from 'react-apollo'
import Link from 'next/link'
import swal from 'sweetalert'

import withData from 'lib/withData'
import withAuth from 'lib/withAuth'
import Page from 'components/Page'
import PaginateTable from 'components/PaginateTable'
import RemoveIcon from 'components/RemoveIcon'
import Searchable from 'components/Searchable'

export const getContacts = gql`
  query getContacts($after: String, $fullName: String) {
    contacts(first: 15, after: $after, fullName: $fullName) {
      totalPages
      edges {
        node {
          id
          fullName
          email
          mobile
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

const removeContact = gql`
  mutation removeContact($instanceId: ID!, $instanceType: Int!) {
    removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
      errors
    }
  }
`

const Contacts = ({ user, data, mutate }) => {
  const handleRemoveContact = contactId =>
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
        mutate({
          variables: {
            instanceId: contactId,
            instanceType: 1,
          },
          update: (store, { data: { removeInstance } }) => {
            if (removeInstance.errors.length === 0) {
              const cache = store.readQuery({
                query: getContacts,
                variables,
              })

              const index = cache.contacts.edges.findIndex(contact => contact.node.id === contactId)

              if (index > -1) {
                cache.contacts.edges = cache.contacts.edges
                  .slice(0, index)
                  .concat(cache.contacts.edges.slice(index + 1, cache.contacts.edges.length))
              }

              store.writeQuery({
                query: getContacts,
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
              text: 'The contact has been removed successfully',
            })
          }
        })
      }
    })

  return (
    <Page user={user} pageTitle="Contacts">
      <Searchable
        searchableField="fullName"
        data={data}
        dataKey="contacts"
        filterInputPlaceholder="Filter contacts"
      >
        {({ filterComponent }) => (
          <div>
            <div className="row justify-content-between mb-3">
              <div className="col col-md-3">{filterComponent}</div>
              <div className="col col-md-auto">
                <Link href="/addcontact" as="/contacts/add" prefetch>
                  <a className="btn btn-info">
                    <span>Add</span>
                  </a>
                </Link>
              </div>
            </div>
            <PaginateTable
              detailPageAccessor="contact"
              columns={[
                {
                  Header: 'Name',
                  accessor: 'fullName',
                },
                {
                  Header: 'Email',
                  accessor: 'email',
                },
                {
                  Header: 'Mobile',
                  accessor: 'mobile',
                  className: 'text-center',
                  headerClassName: 'text-center',
                  maxWidth: 150,
                },
                {
                  sortable: false,
                  resizable: false,
                  minWidth: 10,
                  className: 'text-center',
                  Cell: ({ original }) => (
                    <RemoveIcon value={original.id} onClick={handleRemoveContact} />
                  ),
                },
              ]}
              defaultSorted={[
                {
                  id: 'fullName',
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

Contacts.propTypes = {
  user: PropTypes.shape({
    id: PropTypes.string,
    photo: PropTypes.string,
    fullName: PropTypes.string,
    firstName: PropTypes.string,
    lastName: PropTypes.string,
  }).isRequired,
  data: PropTypes.shape({
    loading: PropTypes.bool.isRequired,
  }),
}

Contacts.defaultProps = {
  data: {
    loading: true,
    contacts: [],
  },
}

export default withData(
  withAuth(
    compose(
      graphql(getContacts, {
        options: {
          notifyOnNetworkStatusChange: true,
        },
      }),
      graphql(removeContact),
    )(Contacts),
  ),
)
