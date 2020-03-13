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
    $leadStatus: String
    $leadType: Boolean
    $billableStatus: String
  ) {
    matters(
      first: 15
      after: $after
      name_Icontains: $matterName
      clientName: $clientName
      principalName: $principalName
      managerName: $managerName
      assistantName: $assistantName
      leadStatus: $leadStatus
      leadType: $leadType
      billableStatus: $billableStatus
    ) {
      totalPages
      edges {
        cursor
        node {
          id
          name
          billableStatusDisplay
          totalTimeValue
          leadStatusDisplay
          totalTimeInvoiced
          wip
          entryType
          entryTypeDisplay
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

class Leads extends React.PureComponent {
  constructor(props) {
    super(props)

    this.state = {
      principalName: '',
      managerName: '',
      assistantName: '',
      prospectName: '',
      leadName: '',
      leadStatus: '',
      page: 0,
      fetchedPages: [0],
    }
  }
  componentDidMount = () => {
    this.setState({ page: 0 })
  }
  handleProspectClear = () => {
    this.setState({ clientName: '' })
    this.filterMatters({ ...this.state, clientName: null })
  }
  handleLeadClear = () => {
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
  handleLeadClear = () => {
    this.setState({ leadStatus: '' })
    this.filterMatters({ ...this.state, leadStatus: '' })
  }
  handleProspectChange = (event) => {
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
  handleLeadChange = (event) => {
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
  handleLeadStatusChange = (event) => {
    const { value } = event.target

    this.setState({ leadStatus: value })
    if (value !== '0') {
      this.filterMatters({ ...this.state, leadStatus: value })
    } else {
      this.filterMatters({ ...this.state, leadStatus: '' })
    }
  }
  filterMatters = (values) => {
    const {
      clientName,
      matterName,
      principalName,
      managerName,
      assistantName,
      leadStatus,
    } = values
    const { data } = this.props

    this.changePage(0)
    this.setState({ fetchedPages: [0] })

    if (leadStatus === '5') {
      data.refetch({
        billableStatus: '3',
        leadStatus,
        clientName,
        matterName,
        principalName,
        managerName,
        assistantName,
        leadType: null,
      })
    } else {
      data.refetch({
        billableStatus: '1',
        clientName,
        matterName,
        principalName,
        managerName,
        assistantName,
        leadStatus,
        leadType: true,
      })
    }
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
                text: 'The lead has been removed successfully',
              })
            }
          })
      }
    })
  render() {
    const { user, data, dataLoading } = this.props
    console.log(this.props);
    return (
      <Page user={user} pageTitle="Leads">
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
                    placeholder="Filter by Prospect"
                    className="form-control"
                    onClear={this.handleProspectClear}
                    onChange={this.handleProspectChange}
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
                  <label htmlFor="matterStatus" className="mr-sm-2">
                    Lead Status
                  </label>
                  <select
                    id="leadStatus"
                    onChange={this.handleLeadStatusChange}
                    value={this.state.leadStatus}
                    className="form-control"
                  >
                    <option value={0}>All</option>
                    <option value={1}>To be contacted</option>
                    <option value={2}>Nurturing</option>
                    <option value={3}>Quoting</option>
                    <option value={4}>Waiting for response</option>
                    <option value={5}>Lost</option>
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
                filterInputPlaceholder="Filter by Matter"
                onPageChange={this.changePage}
              >
                {() => (
                  <div>
                    <div className="row justify-content-between mb-3">
                      <div className="col col-md-3">
                        <ClearableInput
                          placeholder="Filter by Lead name"
                          className="form-control"
                          onChange={this.handleLeadChange}
                          value={this.state.matterName}
                          onClear={this.handleLeadClear}
                        />
                      </div>
                      <div className="col col-md-auto">
                        <Link href="/addlead" as="leads/add" prefetch>
                          <a className="btn btn-info">
                            <span>Add</span>
                          </a>
                        </Link>
                      </div>
                    </div>
                    {dataLoading && <LineLoader />}
                    <PaginateTable
                      detailPageAccessor="lead"
                      page={this.state.page}
                      columns={[
                        {
                          Header: 'Prospect',
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
                          Header: 'Lead',
                          accessor: 'name',
                          headerStyle: { fontWeight: 500, textAlign: 'left', padding: '0.75rem' },
                        },
                        {
                          Header: 'Lead status',
                          maxWidth: 200,
                          accessor: 'leadStatusDisplay',
                          headerStyle: { fontWeight: 500, textAlign: 'left', padding: '0.75rem' },
                        },
                        {
                          Header: 'Time value',
                          accessor: 'totalTimeValue',
                          headerStyle: { fontWeight: 500, textAlign: 'left', padding: '0.75rem' },
                          Cell: ({ original }) => formatCurrency(original.totalTimeValue),
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
        fetchPolicy: 'cache-and-network',
        variables: { leadType: true },
      } }),
      graphql(removeMatter),
      connect(state => ({ dataLoading: state.page.get(MATTERS_LOADING_STATUS) })),
    )(Leads),
  ),
)
