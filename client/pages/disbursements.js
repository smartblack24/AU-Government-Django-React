import React from 'react'
import { graphql, compose, gql } from 'react-apollo'
import swal from 'sweetalert'
import moment from 'moment'
import Link from 'next/link'
import { connect } from 'react-redux'

import { DISBURSEMENTS_LOADING_STATUS } from 'constants/page'
import { formatCurrency } from 'utils'
import Page from 'components/Page'
import withData from 'lib/withData'
import withAuth from 'lib/withAuth'
import LineLoader from 'components/LineLoader'
import RemoveIcon from 'components/RemoveIcon'
import Searchable from 'components/Searchable'
import PaginateTable from 'components/PaginateTable'

const getDisbursements = gql`
  query disbursements(
    $after: String
    $clientName: String
    $matterName: String
    $rate: Float
    $date: String
  ) {
    timeEntries(
      first: 15
      entryType: "2"
      after: $after
      clientName: $clientName
      matter_Name_Icontains: $matterName
      rate: $rate
      date: $date
    ) {
      totalPages
      edges {
        cursor
        node {
          id
          date
          client {
            id
            name
          }
          matter {
            id
            name
          }
          description
          units
          rate
        }
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
`

const removeDisbursement = gql`
  mutation removeContact($instanceId: ID!, $instanceType: Int!) {
    removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
      errors
    }
  }
`

const Disbursement = ({ user, mutate, data, dataLoading }) => {
  const handleRemoveDisbursement = disbursementId =>
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
      const { variables } = data
      if (willDelete) {
        mutate({
          variables: {
            instanceId: disbursementId,
            instanceType: 6,
          },
          update: (store, { data: { removeInstance } }) => {
            if (removeInstance.errors.length === 0) {
              const cache = store.readQuery({ query: getDisbursements, variables })

              const index = cache.timeEntries.edges.findIndex(t => t.node.id === disbursementId)

              if (index > -1) {
                cache.timeEntries.edges = cache.timeEntries.edges
                  .slice(0, index)
                  .concat(cache.timeEntries.edges.slice(index + 1, cache.timeEntries.edges.length))
              }

              store.writeQuery({ query: getDisbursements, data: cache, variables })
            }
          },
        }).then((response) => {
          if (response.data.removeInstance.errors.length > 0) {
            const msg = response.data.removeInstance.errors.join('\n')
            swal({ text: msg, icon: 'error' })
          } else {
            swal({
              icon: 'success',
              text: 'The disbursement has been removed successfully',
            })
          }
        })
      }
    })
  return (
    <Page user={user} pageTitle="Disbursements">
      <Searchable
        searchableFields={[
          { name: 'clientName', type: 'string' },
          { name: 'matterName', type: 'string' },
          { name: 'rate', type: 'number' },
          { name: 'date', type: 'date' },
        ]}
        data={data}
        dataKey="timeEntries"
        filterInputPlaceholders={[
          'Filter by client',
          'Filter by matter name',
          'Filter by rate',
          'Filter by date',
        ]}
      >
        {({ filterComponents }) => (
          <div>
            <div style={{ marginRight: 0 }} className="row mb-3 justify-content-between">
              {filterComponents.map(filterComponent => (
                <div key={filterComponent.id} className="col col-md-auto">
                  {filterComponent.getComponent()}
                </div>
              ))}

              <div className="col-md-auto" style={{ marginLeft: 'auto' }}>
                <Link href="/adddisbursement" as="/disbursements/add" prefetch>
                  <a className="btn btn-info">
                    <span>Add</span>
                  </a>
                </Link>
              </div>
            </div>
            {dataLoading && <LineLoader />}
            <PaginateTable
              detailPageAccessor="disbursement"
              columns={[
                {
                  Header: 'Date entered',
                  id: 'startDate',
                  accessor: original => moment(original.date).format('DD/MM/YYYY'),
                  maxWidth: 150,
                },
                {
                  Header: 'Client',
                  id: 'clientName',
                  accessor: original => original.client && original.client.name,
                },
                {
                  Header: 'Matter',
                  id: 'matterName',
                  accessor: original => original.matter && original.matter.name,
                },
                {
                  Header: 'Description',
                  accessor: 'description',
                },
                {
                  Header: 'Units',
                  accessor: 'units',
                  maxWidth: 100,
                },
                {
                  Header: 'Rate',
                  id: 'rate',
                  accessor: original => formatCurrency(original.rate),
                  maxWidth: 100,
                },
                {
                  sortable: false,
                  resizable: false,
                  minWidth: 10,
                  className: 'text-center',
                  Cell: ({ original }) => (
                    <RemoveIcon value={original.id} onClick={handleRemoveDisbursement} />
                  ),
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
      graphql(getDisbursements, { options: { notifyOnNetworkStatusChange: true } }),
      graphql(removeDisbursement),
      connect(state => ({ dataLoading: state.page.get(DISBURSEMENTS_LOADING_STATUS) })),
    )(Disbursement),
  ),
)
