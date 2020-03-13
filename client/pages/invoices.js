import React, { Fragment } from 'react'
import { graphql, compose } from 'react-apollo'
import gql from 'graphql-tag'
import moment from 'moment'
import swal from 'sweetalert'
import { connect } from 'react-redux'
import { getMatter, getInvoiceStatuses } from 'queries'
import { setLoadingStatus } from 'actions/page'
import {
  TIME_ENTRIES_LOADING_STATUS,
  MATTERS_LOADING_STATUS,
  DISBURSEMENTS_LOADING_STATUS,
} from 'constants/page'
import Page from 'components/Page'
import Button from 'components/Button'
import RemoveIcon from 'components/RemoveIcon'
import Searchable from 'components/Searchable'
import ClearableInput from 'components/ClearableInput'
import PaginateTable from 'components/PaginateTable'
import { swalCreator, formatCurrency } from 'utils'
import withData from 'lib/withData'
import withAuth from 'lib/withAuth'

const removeInvoice = gql`
  mutation removeInvoice($instanceId: ID!, $instanceType: Int!) {
    removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
      errors
    }
  }
`

export const getInvoices = gql`
  query invoices($after: String, $numberOrClientName: String, $isPaid: Boolean, $status: Float) {
    invoices(
      first: 15
      after: $after
      numberOrClientName: $numberOrClientName
      isPaid: $isPaid
      status: $status
    ) {
      totalPages
      edges {
        cursor
        node {
          id
          createdDate
          statusDisplay
          number
          isPaid
          valueInclGst
          netOutstanding
          matter {
            id
            description
            client {
              id
              name
            }
          }
        }
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
`

const fetchAllPaymentsFromXero = gql`
  mutation fetchAllPaymentsFromXero {
    fetchAllPaymentsFromXero {
      success
      errors
    }
  }
`

class InvoiceList extends React.Component {
  state = {
    numberOrClientName: '',
    isPaid: '',
    status: 0,
    page: 0,
    fetchedPages: [0],
    fetchAllPayments: false,
  }
  handleNumberORClientNameClear = () => {
    this.setState({ numberOrClientName: '' })
    this.filterInvoices({ ...this.state, numberOrClientName: null })
  }
  handlerIsPaidClear = () => {
    this.setState({ isPaid: '' })
    this.filterInvoices({ ...this.this.state, isPaid: null })
  }
  handleStatusClear = () => {
    this.setState({ status: '' })
    this.filterInvoices({ ...this.state, status: null })
  }
  handleNumberORClientNameChange = (event) => {
    const { value } = event.target
    this.setState({ numberOrClientName: value })
    if (value.length > 2) {
      this.filterInvoices({ ...this.state, numberOrClientName: value })
      this.setState({ numberOrClientName: value })
    } else if (!value.length) {
      this.filterInvoices({ ...this.state, numberOrClientName: null })
      this.setState({ numberOrClientName: value })
    }
  }
  handleIsPaidChange = (event) => {
    const { value } = event.target
    let paid = null

    if (value === 'true') {
      paid = true
    } else if (value === 'false') {
      paid = false
    }
    this.setState({ isPaid: paid })
    this.filterInvoices({ ...this.state, isPaid: paid })
  }
  handleStatusChange = (event) => {
    const { value } = event.target
    this.setState({ status: value })
    if (value !== '0') {
      this.filterInvoices({ ...this.state, status: value })
    } else {
      this.filterInvoices({ ...this.state, status: 0 })
    }
  }

  filterInvoices = (values) => {
    const {
      isPaid,
      numberOrClientName,
      status,
    } = values

    this.changePage(0)
    this.setState({ fetchedPages: [0] })

    this.props.data.refetch({
      isPaid,
      numberOrClientName,
      status,
    })
  }
  changePage = (page) => {
    this.setState({ page, fetchedPages: this.state.fetchedPages.concat(page) })
  }

  handleRemoveInvoice = async (values) => {
    const { invoiceId, matterId } = values
    const willDelete = await swal({
      title: 'Confirmation',
      text: 'Are you sure?',
      icon: 'warning',
      buttons: {
        cancel: true,
        confirm: {
          closeModal: false,
        },
      },
    })
    if (willDelete) {
      const { variables } = this.props.data
      const response = await this.props.mutate({
        variables: {
          instanceId: invoiceId,
          instanceType: 8,
        },
        refetchQueries: [{ query: getMatter, variables: { id: matterId } }],
        update: (store, { data: { removeInstance } }) => {
          if (removeInstance.errors.length === 0) {
            const cache = store.readQuery({ query: getInvoices, variables })

            const index = cache.invoices.edges.findIndex(invoice => invoice.node.id === invoiceId)

            if (index > -1) {
              cache.invoices.edges = cache.invoices.edges
                .slice(0, index)
                .concat(cache.invoices.edges.slice(index + 1, cache.invoices.edges.length))
            }

            store.writeQuery({ query: getInvoices, data: cache, variables })
          }
        },
      })

      if (response.data.removeInstance.errors.length > 0) {
        const msg = response.data.removeInstance.errors.join('\n')
        swal({ text: msg, icon: 'error' })
      } else {
        this.props.dispatch(setLoadingStatus(TIME_ENTRIES_LOADING_STATUS, true))
        this.props.dispatch(setLoadingStatus(DISBURSEMENTS_LOADING_STATUS, true))
        this.props.dispatch(setLoadingStatus(MATTERS_LOADING_STATUS, true))

        swal({
          icon: 'success',
          text: 'The invoice has been removed successfully',
        })
      }
    }
  }

  handleFetchAllPayments = async () => {
    this.setState({ fetchingAllPayments: true })

    const res = await this.props.fetchAllPaymentsFromXero()

    this.setState({ fetchingAllPayments: false })

    const { success, errors } = res.data.fetchAllPaymentsFromXero

    swalCreator({ success, errors, successMsg: 'Fetching payments from Xero is in progress...' })
  }

  resetPages = () => {
    this.setState({ page: 0, fetchedPages: [0] })
  }

  render() {
    const { data, user } = this.props
    const { fetchingAllPayments } = this.state

    const { canUseXero } = user

    return (
      <Page user={user} pageTitle="Invoice list">
        {canUseXero && <div className="col-12 pr-0 mb-3 text-right">
          <Button
            className="btn btn-primary"
            icon="fa fa-credit-card"
            loading={fetchingAllPayments}
            title="Fetch payments from Xero"
            onClick={this.handleFetchAllPayments}
          />
        </div>}
        <Searchable
          manual
          fetchedPages={this.state.fetchedPages}
          changePage={this.changePage}
          resetPages={this.resetPages}
          data={data}
          dataKey="invoices"
          filterInputPlaceholder="Filter invoives"
          onPageChange={this.changePage}
        >
          {() => (
            <div>
              <div className="row justify-content-between mb-3">
                <div className="col col-md-3">
                  <ClearableInput
                    placeholder="Filter be number or Client name"
                    className="form-control"
                    onChange={this.handleNumberORClientNameChange}
                    value={this.state.numberOrClientName}
                    onClear={this.handleNumberORClientNameClear}
                  />
                </div>
                <div className="col col-auto form-inline">
                  <label htmlFor="status" className="mr-2">
                    Status
                  </label>
                  <select
                    id="status"
                    onChange={this.handleStatusChange}
                    className="form-control mr-3"
                  >
                    {this.props.invoiceStatusesData.loading ? (
                      <option>Loading...</option>
                    ) : (
                      <Fragment>
                        <option value="0">All</option>
                        {this.props.invoiceStatusesData.invoiceStatuses.map(status => (
                          <option key={status.id} value={status.id}>
                            {status.name}
                          </option>
                        ))}
                      </Fragment>
                    )}
                  </select>
                  <label htmlFor="billableStatus" className="mr-sm-2">
                    Is Paid
                  </label>
                  <select
                    id="isPaid"
                    className="form-control"
                    onChange={this.handleIsPaidChange}
                  >
                    <option value="0">All</option>
                    <option value="true">True</option>
                    <option value="false">False</option>
                  </select>
                </div>
              </div>
              <PaginateTable
                detailPageAccessor="invoice"
                page={this.state.page}
                columns={[
                  {
                    Header: '#',
                    accessor: 'number',
                    maxWidth: 100,
                    headerStyle: { fontWeight: 500, textAlign: 'left', padding: '0.75rem' },
                  },
                  {
                    Header: 'Date created',
                    accessor: original =>
                      original.createdDate && moment(original.createdDate).format('MMM Do YY'),
                    id: 'createdDate',
                    maxWidth: 150,
                    headerStyle: { fontWeight: 500, textAlign: 'left', padding: '0.75rem' },
                  },
                  {
                    Header: 'Client',
                    id: 'clientName',
                    accessor: (item) => {
                      if (item.matter) {
                        if (item.matter.client) {
                          return item.matter.client.name
                        }
                      }

                      return null
                    },
                    headerStyle: { fontWeight: 500, textAlign: 'left', padding: '0.75rem' },
                  },
                  {
                    Header: 'Status',
                    accessor: 'statusDisplay',
                    maxWidth: 200,
                    headerStyle: { fontWeight: 500, textAlign: 'left', padding: '0.75rem' },
                  },
                  {
                    Header: 'Description',
                    id: 'description',
                    accessor: item => item.matter && item.matter.description,
                    headerStyle: { fontWeight: 500, textAlign: 'left', padding: '0.75rem' },
                  },
                  {
                    Header: 'Invoice (incl GST)',
                    id: 'valueInclGST',
                    accessor: item => formatCurrency(item.valueInclGst),
                    headerStyle: { fontWeight: 500, textAlign: 'left', padding: '0.75rem' },
                  },
                  {
                    Header: 'Net Outstanding',
                    id: 'netOutstanding',
                    accessor: item => formatCurrency(item.netOutstanding),
                    headerStyle: { fontWeight: 500, textAlign: 'left', padding: '0.75rem' },
                  },
                  {
                    sortable: false,
                    resizable: false,
                    minWidth: 10,
                    className: 'text-center',
                    Cell: ({ original }) => (
                      <RemoveIcon
                        value={{ invoiceId: original.id, matterId: original.matter.id }}
                        onClick={this.handleRemoveInvoice}
                      />
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
}

export default withData(
  withAuth(
    compose(
      graphql(getInvoices, {
        options: { notifyOnNetworkStatusChange: true },
        variables: {
          numberOrClientName: '',
          isPaid: '',
          status: 0,
          page: 0,
          fetchedPages: [0],
        },
      }),
      graphql(removeInvoice),
      graphql(getInvoiceStatuses, { name: 'invoiceStatusesData' }),
      graphql(fetchAllPaymentsFromXero, { name: 'fetchAllPaymentsFromXero' }),
      connect(),
    )(InvoiceList),
  ),
)
