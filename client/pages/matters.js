import React from 'react'
import Link from 'next/link'
import { graphql, compose, gql } from 'react-apollo'
import swal from 'sweetalert'
import { connect } from 'react-redux'

import { MATTERS_LOADING_STATUS } from 'constants/page'
import { clientFragment } from 'fragments'
import Page from 'components/Page'
import withData from 'lib/withData'
import withAuth from 'lib/withAuth'
import LineLoader from 'components/LineLoader'
import { formatCurrency } from 'utils'
import RemoveIcon from 'components/RemoveIcon'
import PaginateTable from 'components/PaginateTable'
import Searchable from 'components/Searchable'
import ClearableInput from 'components/ClearableInput'

const getMatters = gql`
  query getMatters(
    $matterName: String
    $clientName: String
    $after: String
    $principalName: String
    $managerName: String
    $assistantName: String
    $billableStatus: String
    $isPaid: Boolean
    $matterStatus: String
    $leadType: Boolean
  ) {
    matters(
      first: 15
      after: $after
      name_Icontains: $matterName
      clientName: $clientName
      principalName: $principalName
      managerName: $managerName
      assistantName: $assistantName
      billableStatus: $billableStatus
      isPaid: $isPaid
      matterStatus: $matterStatus
      leadType: $leadType
    ) {
      totalPages
      edges {
        cursor
        node {
          id
          name
          billableStatusDisplay
          totalTimeValue
          matterStatus
          totalTimeInvoiced
          wip
          client {
            id
            name
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

const removeMatter = gql`
  mutation removeMatter($instanceId: ID!, $instanceType: Int!) {
    removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
      errors
    }
  }
`

class Matters extends React.PureComponent {
  constructor(props) {
    super(props)

    this.state = {
      isPaid: '',
      billableStatus: '',
      principalName: '',
      managerName: '',
      assistantName: '',
      clientName: '',
      matterName: '',
      matterStatus: '',
      page: 0,
      fetchedPages: [0],
    }
  }
  handleClientClear = () => {
    this.setState({ clientName: '' })
    this.filterMatters({ ...this.state, clientName: null })
  }
  handleMatterClear = () => {
    this.setState({ matterName: '' })
    this.filterMatters({ ...this.state, matterName: null })
  }
  handlePrincipalClear = () => {
    this.setState({ principalName: '' })
    this.filterMatters({ ...this.state, principalName: null })
  }
  handleManagerClear = () => {
    this.setState({ managerName: '' })
    this.filterMatters({ ...this.state, managerName: null })
  }
  handleAssistantClear = () => {
    this.setState({ assistantName: '' })
    this.filterMatters({ ...this.state, assistantName: null })
  }
  handleMatterStatusClear = () => {
    this.setState({ matterStatus: '' })
    this.filterMatters({ ...this.state, matterStatus: null })
  }
  handleBillableStatusChange = (event) => {
    const { value } = event.target

    this.setState({ billableStatus: value })

    if (value !== '0') {
      this.filterMatters({ ...this.state, billableStatus: value })
    } else {
      this.filterMatters({ ...this.state, billableStatus: '' })
    }
  }
  handleMatterStatusChange = (event) => {
    const { value } = event.target
    this.setState({ matterStatus: value })
    if (value === '0') {
      this.filterMatters({ ...this.state, matterStatus: '' })
    } else {
      this.filterMatters({ ...this.state, matterStatus: value })
    }
  }
  handleIsPaidChange = (event) => {
    const { value } = event.target

    this.setState({ isPaid: value })

    this.filterMatters({ ...this.state, isPaid: value })
  }
  handleClientNameChange = (event) => {
    const { value } = event.target

    this.setState({ clientName: value })

    if (value.length > 2) {
      this.filterMatters({ ...this.state, clientName: value })
    } else if (!value.length) {
      this.filterMatters({ ...this.state, clientName: null })
    }
  }
  handleManagerNameChange = (event) => {
    const { value } = event.target

    this.setState({ managerName: value })

    if (value.length > 2) {
      this.filterMatters({ ...this.state, managerName: value })
    } else if (!value.length) {
      this.filterMatters({ ...this.state, managerName: null })
    }
  }
  handleMatterNameChange = (event) => {
    const { value } = event.target

    this.setState({ matterName: value })

    if (value.length > 2) {
      this.filterMatters({ ...this.state, matterName: value })
    } else if (!value.length) {
      this.filterMatters({ ...this.state, matterName: null })
    }
  }
  handlePrincipalNameChange = (event) => {
    const { value } = event.target

    this.setState({ principalName: value })

    if (value.length > 2) {
      this.filterMatters({ ...this.state, principalName: value })
    } else if (!value.length) {
      this.filterMatters({ ...this.state, principalName: null })
    }
  }
  handleAssistantNameChange = (event) => {
    const { value } = event.target

    this.setState({ assistantName: value })

    if (value.length > 2) {
      this.filterMatters({ ...this.state, assistantName: value })
    } else if (!value.length) {
      this.filterMatters({ ...this.state, assistantName: null })
    }
  }
  filterMatters = (values) => {
    const {
      clientName,
      matterName,
      principalName,
      managerName,
      assistantName,
      billableStatus,
      isPaid,
      matterStatus,
    } = values
    const { data } = this.props
    let isMatterPaid = null

    if (isPaid === 'true') {
      isMatterPaid = true
    } else if (isPaid === 'false') {
      isMatterPaid = false
    }

    this.changePage(0)
    this.setState({ fetchedPages: [0] })

    data.refetch({
      clientName,
      matterName,
      principalName,
      managerName,
      assistantName,
      billableStatus,
      matterStatus,
      isPaid: isMatterPaid,
      leadType: false,
    })
  }
  changePage = (page) => {
    this.setState({ page, fetchedPages: this.state.fetchedPages.concat(page) })
  }
  removeMatter = matterId =>
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
        const { variables } = this.props.data
        this.props
          .mutate({
            variables: {
              instanceId: matterId,
              instanceType: 4,
            },
            update: (store, { data: { removeInstance } }) => {
              if (removeInstance.errors.length === 0) {
                const data = store.readQuery({
                  query: getMatters,
                  variables,
                })

                const index = data.matters.edges.findIndex(matter => matter.node.id === matterId)
                const matter = data.matters.edges[index]

                if (index > -1) {
                  data.matters.edges = data.matters.edges
                    .slice(0, index)
                    .concat(data.matters.edges.slice(index + 1, data.matters.edges.length))
                }

                store.writeQuery({
                  query: getMatters,
                  data,
                  variables,
                })

                // Update the client to which the matter related
                try {
                  const client = store.readFragment({
                    id: 'ClientType-{matter.client.id}',
                    fragment: clientFragment,
                    fragmentName: 'Client',
                  })

                  client.mattersCount -= 1

                  store.writeFragment({
                    id: `ClientType-${matter.client.id}`,
                    fragment: clientFragment,
                    fragmentName: 'Client',
                    data: client,
                  })
                } catch (e) {} // eslint-disable-line
              }
            },
          })
          .then((response) => {
            if (response.data.removeInstance.errors.length > 0) {
              const msg = response.data.removeInstance.errors.join('\n')
              swal({ text: msg, icon: 'error' })
            } else {
              swal({
                icon: 'success',
                text: 'The matter has been removed successfully',
              })
            }
          })
      }
    })
  render() {
    const { user, data, dataLoading } = this.props
    console.log(data)
    return (
      <Page user={user} pageTitle="Matters">
        <div style={{ minHeight: 500 }}>
          <div className="contact-page-aside">
            <div className="left-aside">
              <ul className="list-style-none" style={{ position: 'relative' }}>
                <li className="box-label">
                  <h3>Filters</h3>
                </li>
                <li className="divider" />
                <li className="mb-3">
                  <ClearableInput
                    placeholder="Filter by Client"
                    className="form-control"
                    onClear={this.handleClientClear}
                    onChange={this.handleClientNameChange}
                    value={this.state.clientName}
                  />
                </li>
                <li className="mb-3">
                  <ClearableInput
                    placeholder="Filter by Principal"
                    className="form-control"
                    onClear={this.handlePrincipalClear}
                    onChange={this.handlePrincipalNameChange}
                    value={this.state.principalName}
                  />
                </li>
                <li className="mb-3">
                  <ClearableInput
                    placeholder="Filter by Manager"
                    className="form-control"
                    onClear={this.handleManagerClear}
                    onChange={this.handleManagerNameChange}
                    value={this.state.managerName}
                  />
                </li>
                <li className="mb-3">
                  <ClearableInput
                    placeholder="Filter by Assistant"
                    className="form-control"
                    onClear={this.handleAssistantClear}
                    onChange={this.handleAssistantNameChange}
                    value={this.state.assistantName}
                  />
                </li>
                <li className="mb-3">
                  <label htmlFor="billableStatus" className="mr-sm-2">
                    Billable Status
                  </label>
                  <select
                    id="billableStatus"
                    onChange={this.handleBillableStatusChange}
                    value={this.state.billableStatus}
                    className="form-control"
                  >
                    <option value="">All</option>
                    <option value={1}>Open</option>
                    <option value={2}>Suspended</option>
                    <option value={3}>Closed</option>
                  </select>
                </li>
                <li className="mb-3">
                  <label htmlFor="billableStatus" className="mr-sm-2">
                    Is Paid
                  </label>
                  <select
                    id="isPaid"
                    onChange={this.handleIsPaidChange}
                    value={this.state.isPaid}
                    className="form-control"
                  >
                    <option value="">All</option>
                    <option value="true">True</option>
                    <option value="false">False</option>
                  </select>
                </li>
                <li className="mb-3">
                  <label htmlFor="matterStatus" className="mr-sm-2">
                    Matter Status
                  </label>
                  <select
                    id="matterStatus"
                    onChange={this.handleMatterStatusChange}
                    value={this.state.matterStatus}
                    className="form-control"
                  >
                    <option value={0}>All</option>
                    <option value={1}>Active - High (70+ units)</option>
                    <option value={2}>Active - Moderate (30-70 units)</option>
                    <option value={3}>Active - Low (0-30 units)</option>
                    <option value={4}>Waiting for Internal review</option>
                    <option value={5}>Waiting for AA review</option>
                    <option value={6}>Waiting for external party to respond</option>
                    <option value={7}>Ad hoc Work</option>
                    <option value={8}>Need to be billed</option>
                    <option value={9}>Matter Closed</option>
                    <option value={10}>Business Building</option>
                  </select>
                </li>
              </ul>
            </div>
            <div className="right-aside">
              <Searchable
                manual
                fetchedPages={this.state.fetchedPages}
                searchableField="name"
                changePage={this.changePage}
                data={data}
                dataKey="matters"
                filterInputPlaceholder="Filter matters"
                onPageChange={this.changePage}
              >
                {() => (
                  <div>
                    <div className="row justify-content-between mb-3">
                      <div className="col col-md-3">
                        <ClearableInput
                          placeholder="Filter by Matter name"
                          className="form-control"
                          onChange={this.handleMatterNameChange}
                          value={this.state.matterName}
                          onClear={this.handleMatterClear}
                        />
                      </div>
                      <div className="col col-md-auto">
                        <Link href="/addmatter" as="/matters/add" prefetch>
                          <a className="btn btn-info">
                            <span>Add</span>
                          </a>
                        </Link>
                      </div>
                    </div>
                    {dataLoading && <LineLoader />}
                    <PaginateTable
                      detailPageAccessor="matter"
                      page={this.state.page}
                      columns={[
                        {
                          Header: 'Client',
                          id: 'clientName',
                          minWidth: 200,
                          accessor: item => item.client && item.client.name,
                          headerStyle: {
                            fontWeight: 500,
                            textAlign: 'left',
                            padding: '0.75rem',
                          },
                        },
                        {
                          Header: 'Matter',
                          accessor: 'name',
                          headerStyle: { fontWeight: 500, textAlign: 'left', padding: '0.75rem' },
                        },
                        {
                          Header: 'Status',
                          maxWidth: 200,
                          accessor: 'billableStatusDisplay',
                          headerStyle: { fontWeight: 500, textAlign: 'left', padding: '0.75rem' },
                        },
                        {
                          Header: 'Time value',
                          accessor: 'totalTimeValue',
                          headerStyle: { fontWeight: 500, textAlign: 'left', padding: '0.75rem' },
                          Cell: ({ original }) => formatCurrency(original.totalTimeValue),
                        },
                        {
                          Header: 'Invoiced',
                          accessor: 'totalTimeInvoiced',
                          headerStyle: { fontWeight: 500, textAlign: 'left', padding: '0.75rem' },
                          Cell: ({ original }) => formatCurrency(original.totalTimeInvoiced),
                        },
                        {
                          Header: 'WIP',
                          accessor: 'wip',
                          headerStyle: { fontWeight: 500, textAlign: 'left', padding: '0.75rem' },
                          Cell: ({ original }) => formatCurrency(original.wip),
                        },
                        {
                          sortable: false,
                          resizable: false,
                          minWidth: 25,
                          className: 'text-center',
                          headerStyle: { fontWeight: 500, padding: '0.75rem' },
                          Cell: ({ original }) => (
                            <RemoveIcon value={original.id} onClick={this.removeMatter} />
                          ),
                        },
                      ]}
                    />
                  </div>
                )}
              </Searchable>
            </div>
          </div>
        </div>
      </Page>
    )
  }
}

export default withData(
  withAuth(
    compose(
      graphql(getMatters, { options: {
        notifyOnNetworkStatusChange: true,
        variables: { leadType: false },
      } }),
      graphql(removeMatter),
      connect(state => ({ dataLoading: state.page.get(MATTERS_LOADING_STATUS) })),
    )(Matters),
  ),
)
