import React from 'react'
import Link from 'next/link'
import { graphql, gql, compose } from 'react-apollo'
import swal from 'sweetalert'

import Searchable from 'components/Searchable'
import Page from 'components/Page'
import withAuth from 'lib/withAuth'
import withData from 'lib/withData'
import PaginateTable from 'components/PaginateTable'
import RemoveIcon from 'components/RemoveIcon'

export const getOrganisations = gql`
  query getOrganisations($after: String, $name: String) {
    organisations(first: 15, after: $after, name_Icontains: $name) {
      totalPages
      edges {
        node {
          id
          name
          industry {
            id
            name
          }
          mainLine
          website
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

const removeOrganisation = gql`
  mutation removeOrganisation($instanceId: ID!, $instanceType: Int!) {
    removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
      errors
    }
  }
`

const Organisations = ({ user, data, mutate }) => {
  const handleRemoveOrganisation = organisationId =>
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
            instanceId: organisationId,
            instanceType: 2,
          },
          update: (store, { data: { removeInstance } }) => {
            if (removeInstance.errors.length === 0) {
              const cache = store.readQuery({
                query: getOrganisations,
                variables,
              })

              const index = cache.organisations.edges.findIndex(
                org => org.node.id === organisationId,
              )

              if (index > -1) {
                cache.organisations.edges = cache.organisations.edges
                  .slice(0, index)
                  .concat(
                    cache.organisations.edges.slice(index + 1, cache.organisations.edges.length),
                  )
              }

              store.writeQuery({
                query: getOrganisations,
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
              text: 'The organisation has been removed successfully',
            })
          }
        })
      }
    })
  return (
    <Page user={user} pageTitle="Organisations">
      <Searchable
        searchableField="name"
        data={data}
        dataKey="organisations"
        filterInputPlaceholder="Filter organisations"
      >
        {({ filterComponent }) => (
          <div>
            <div className="row justify-content-between mb-3">
              <div className="col col-md-3">{filterComponent}</div>
              <div className="col col-md-auto">
                <Link href="/addorganisation" as="/organisations/add" prefetch>
                  <a className="btn btn-info">
                    <span>Add</span>
                  </a>
                </Link>
              </div>
            </div>
            <PaginateTable
              detailPageAccessor="organisation"
              columns={[
                {
                  Header: 'Name',
                  accessor: 'name',
                  headerStyle: { fontWeight: 500, textAlign: 'left', padding: '0.75rem' },
                },
                {
                  Header: 'Main Phone',
                  accessor: 'mainLine',
                  maxWidth: 250,
                  headerStyle: { fontWeight: 500, textAlign: 'left', padding: '0.75rem' },
                },
                {
                  Header: 'Website',
                  accessor: 'website',
                  headerStyle: { fontWeight: 500, textAlign: 'left', padding: '0.75rem' },
                },
                {
                  Header: 'Industry',
                  id: 'industry',
                  maxWidth: 200,
                  accessor: item => item.industry && item.industry.name,
                  headerStyle: { fontWeight: 500, textAlign: 'left', padding: '0.75rem' },
                },
                {
                  sortable: false,
                  resizable: false,
                  minWidth: 10,
                  headerStyle: { fontWeight: 500, padding: '0.75rem' },
                  className: 'text-center',
                  Cell: ({ original }) => (
                    <RemoveIcon value={original.id} onClick={handleRemoveOrganisation} />
                  ),
                },
              ]}
              defaultSorted={[
                {
                  id: 'name',
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

export default withData(
  withAuth(
    compose(
      graphql(getOrganisations, { options: { notifyOnNetworkStatusChange: true } }),
      graphql(removeOrganisation),
    )(Organisations),
  ),
)
