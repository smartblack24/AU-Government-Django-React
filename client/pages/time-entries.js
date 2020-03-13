import React from 'react'
import { graphql, compose, gql } from 'react-apollo'
import moment from 'moment'
import swal from 'sweetalert'
import Link from 'next/link'
import { connect } from 'react-redux'
import Select from 'react-select'
// import { toGlobalId, fromGlobalId } from 'graphql-relay'

import { TIME_ENTRIES_LOADING_STATUS } from 'constants/page'
import AsyncAutocomplete from 'components/AsyncAutocomplete'
import CustomDatePicker from 'components/DatePicker'
import Page from 'components/Page'
import withData from 'lib/withData'
import withAuth from 'lib/withAuth'
import LineLoader from 'components/LineLoader'
import RemoveIcon from 'components/RemoveIcon'
import Searchable from 'components/Searchable'
import PaginateTable from 'components/PaginateTable'
import UnitsCounter from 'components/UnitsCounter'

const getTimeEntries = gql`
  query timeEntries(
    $after: String
    $staffName: String
    $isBilled: Boolean
    $clientName: String
    $matterName: String
    $date: String
    $fromDate: String
    $toDate: String
    $clientId: String
    $timeEntryType: String
  ) {
    timeEntries(
      first: 15
      entryType: "1"
      after: $after
      staffName: $staffName
      isBilled: $isBilled
      clientName: $clientName
      matter_Name_Icontains: $matterName
      date: $date
      fromDate: $fromDate
      toDate: $toDate
      clientId: $clientId
      timeEntryType: $timeEntryType
    ) {
      totalPages
      edges {
        cursor
        node {
          id
          description
          units
          statusDisplay
          date
          recordType
          matter {
            id
            name
          }
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

const getUsers = gql`
  query staff($fullName: String, $skip: Boolean!) {
    users(fullName: $fullName) @skip(if: $skip) {
      edges {
        cursor
        node {
          id
          fullName
        }
      }
    }
  }
`

const getClients = gql`
  query timeEntryClients($name: String, $skip: Boolean!) {
    clients(first: 5, name: $name) @skip(if: $skip) {
      edges {
        cursor
        node {
          id
          name
        }
      }
    }
  }
`

const getMatters = gql`
  query timeEntryMatters($name: String, $clientId: ID, $skip: Boolean!) {
    matters(name_Icontains: $name, client_Id: $clientId) @skip(if: $skip) {
      edges {
        cursor
        node {
          id
          name
        }
      }
    }
  }
`

const Cell = ({ original, children }) => {
  if (!original.isBilled) {
    return (
      <Link
        key={original.id}
        href={`/time-entry?id=${original.id}`}
        as={`/time-entry/${original.id}`}
      >
        {children}
      </Link>
    )
  }

  return children
}

class TimeEntry extends React.Component {
  state = {
    page: 0,
    fetchedPages: [0],
    user: this.props.user && this.props.user,
    options: [],
    date: moment(),
    fromDate: null,
    toDate: null,
    TimeEntryType: null,
    // pageJump: 0,
    focus: false,
    matter: {
      name: '',
      id: '',
      label: '',
      value: '',
    },
  }
  getUsers = async (input, callback) => {
    const { staffData } = this.props
    if (input.length > 2) {
      const response = await staffData.refetch({ skip: false, fullName: input })
      if (response.data.users.edges.length) {
        // transform to react-select format
        const options = response.data.users.edges.map(({ node }) => ({
          staff: node,
          value: node.id,
          label: node.fullName,
        }))

        // callback with fetched data
        callback(null, { options })
      }
    }
  }
  getClients = async (input, callback) => {
    const { clientsData } = this.props
    if (input.length > 2) {
      const response = await clientsData.refetch({ skip: false, name: input })
      if (response.data.clients.edges.length) {
        // transform to react-select format
        const options = response.data.clients.edges.map(({ node }) => ({
          value: node.id,
          label: node.name,
        }))
        // callback with fetched data
        callback(null, { options })
      }
    }
  }
  getMatters = async (input, callback) => {
    const { mattersData } = this.props
    if (input.length > 2) {
      const response = await mattersData.refetch({
        skip: false,
        name: input,
        clientId: null,
      })
      if (response.data.matters.edges.length) {
        // transform to react-select format
        const options = response.data.matters.edges.map(({ node }) => ({
          value: node.id,
          label: node.name,
        }))
        callback(null, { options })
      }
    }
  }
  handleOnAutocompleteUserEdit = () => {
    this.setState({ user: {}, pageJump: '' })
    this.props.data.refetch({
      after: '',
      staffName: '',
    })
  }
  handleOnAutocompleteClientEdit = () => {
    this.setState({
      client: null,
      matter: {
        name: '',
        id: '',
        label: '',
        value: '',
      },
      focus: false,
      options: [],
      pageJump: '',
    })
    this.props.data.refetch({
      staffName: this.state.user.fullName,
      after: '',
      clientId: null,
    })
  }
  handleOnAutocompleteMatterEdit = () => {
    this.setState({ matter: {
      label: '',
      value: '',
      id: '',
      name: '',
    },
    pageJump: '',
    })
    this.props.data.refetch({
      staffName: this.state.user.fullName,
      after: '',
      matterName: null,
    })
  }
  handleOnStaffSelect = ({ staff }) => {
    this.setState({ user: staff, pageJump: '' })

    this.props.data.refetch({
      after: '',
      staffName: staff.fullName,
    })
  }
  handleOnClientSelect = ({ value, label }) => {
    this.setState({
      client: { name: label, id: value },
      focus: true,
      matter: {
        label: '',
        value: '',
        id: '',
        name: '',
      },
      pageJump: '',
    })

    this.props.data.refetch({
      staffName: this.state.user.fullName,
      after: '',
      clientId: value,
    })
  }
  handleOnMatterSelect = ({ value, label }) => {
    this.setState({ matter: {
      name: label,
      id: value,
      value,
      label,
    },
    pageJump: '',
    })

    this.props.data.refetch({
      staffName: this.state.user.fullName,
      after: '',
      matterName: label,
    })
  }
  handleOnFocus = async () => {
    const { mattersData } = this.props
    const response = await mattersData.refetch({
      skip: false,
      clientId: this.state.client.id,
    })
    if (response.data.matters.edges.length) {
      const options = response.data.matters.edges.map(({ node }) => ({
        value: node.id,
        label: node.name,
      }))
      this.setState({ options })
    }
  }
  removeTimeEntry = timeEntryId =>
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
              instanceId: timeEntryId,
              instanceType: 5,
            },
            update: (store, { data: { removeInstance } }) => {
              if (removeInstance.errors.length === 0) {
                const cache = store.readQuery({
                  query: getTimeEntries,
                  variables,
                })

                const index = cache.timeEntries.edges.findIndex(t => t.node.id === timeEntryId)

                if (index > -1) {
                  cache.timeEntries.edges = cache.timeEntries.edges
                    .slice(0, index)
                    .concat(
                      cache.timeEntries.edges.slice(index + 1, cache.timeEntries.edges.length),
                    )
                }

                store.writeQuery({
                  query: getTimeEntries,
                  data: cache,
                  variables,
                })
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
                text: 'The time entry has been removed successfully',
              })
            }
          })
      }
    })
  handleBilledStatusChange = (event) => {
    const { value } = event.target

    let isBilled = null

    if (value === 'true') {
      isBilled = true
    } else if (value === 'false') {
      isBilled = false
    }

    this.resetPages()

    this.props.data.refetch({ staffName: this.state.user.fullName, after: '', isBilled })
  }
  handleEntryTypeChange = (event) => {
    const { value } = event.target

    this.resetPages()

    if (value === '1') {
      this.props.data.refetch({ staffName: this.state.user.fullName, after: '', timeEntryType: value })
    } else if (value === '2') {
      this.props.data.refetch({ staffName: this.state.user.fullName, after: '', timeEntryType: value })
    } else {
      this.props.data.refetch({ staffName: this.state.user.fullName, after: '', timeEntryType: null })
    }
  }
  resetPages = () => this.setState({ page: 0, fetchedPages: [0] })
  changePage = (page) => {
    this.setState({ page, fetchedPages: this.state.fetchedPages.concat(page) })
  }
  handleDateChange = (value) => {
    if (value) {
      this.props.data.refetch({
        ...this.state,
        staffName: this.state.user.fullName,
        date: value.format('DD/MM/YYYY'),
      })
    } else {
      this.props.data.refetch({
        ...this.state,
        staffName: this.state.user.fullName,
        date: null,
      })
    }
    this.setState({ date: value })
  }
  handleFromDateChange = (value) => {
    const toDate = this.state.toDate && this.state.toDate.format('DD/MM/YYYY')
    if (value) {
      this.props.data.refetch({
        ...this.state,
        staffName: this.state.user.fullName,
        fromDate: value.format('DD/MM/YYYY'),
        toDate,
      })
    } else {
      this.props.data.refetch({
        ...this.state,
        staffName: this.state.user.fullName,
        fromDate: null,
        toDate,
      })
    }
    this.setState({ fromDate: value })
  }
  handleToDateChange = (value) => {
    const fromDate = this.state.fromDate && this.state.fromDate.format('DD/MM/YYYY')
    if (value) {
      this.props.data.refetch({
        ...this.state,
        staffName: this.state.user.fullName,
        toDate: value.format('DD/MM/YYYY'),
        fromDate,
      })
    } else {
      this.props.data.refetch({
        ...this.state,
        staffName: this.state.user.fullName,
        toDate: null,
        fromDate,
      })
    }
    this.setState({ toDate: value })
  }
  // heanlePageJump = (event) => {
  //   console.log(event.target.value)
  //   let value = parseInt(event.target.value, 10)
  //   if (value > this.props.data.timeEntries.totalPages) {
  //     value = this.props.data.timeEntries.totalPages
  //     const index = toGlobalId('arrayconnection', ((value - 2) * 15) + 14)
  //     this.setState({ pageJump: value + 2, fetchedPages: [value] })
  //     this.props.data.refetch({ ...this.state, after: index })
  //   } else if (value <= 0) {
  //     value = 1
  //   } else if (value === null) {
  //     value = 1
  //   }
  //
  //   if (value === 1) {
  //     this.setState({ pageJump: 1, page: 0, fetchedPages: [0] })
  //     this.props.data.refetch({ ...this.state, after: '' })
  //   } else if (value === 2) {
  //     this.setState({ pageJump: 2, page: 1, fetchedPages: [0, 1] })
  //     this.props.data.refetch({ ...this.state, after: toGlobalId('arrayconnection', 14) })
  //   } else {
  //     const index = toGlobalId('arrayconnection', ((value - 2) * 15) + 14)
  //     this.setState({ pageJump: value, page: value - 1 })
  //     this.props.data.refetch({ ...this.state, after: index })
  //   }
  // }
  render() {
    const { data } = this.props
    // console.log(data.timeEntries && data.timeEntries.pageInfo.endCursor)
    // console.log(this.state)
    // console.log(data.timeEntries && fromGlobalId(data.timeEntries.pageInfo.endCursor))
    // console.log(data.timeEntries && toGlobalId('arrayconnection', fromGlobalId(data.timeEntries.pageInfo.endCursor).id))
    data.variables.staffName = this.state.user !== null ? this.state.user.fullName : ''
    return (
      <Page user={this.props.user} pageTitle="Time Entry">
        <div style={{ marginRight: 0 }} className="row mb-3 justify-content-between">
          <div className="col">
            <AsyncAutocomplete
              fieldName="staffMember"
              link="profile"
              onSelect={this.handleOnStaffSelect}
              onEdit={this.handleOnAutocompleteUserEdit}
              value={this.state.user && this.state.user}
              accessor="fullName"
              placeholder="Filter by staff"
              getOptions={this.getUsers}
            />
          </div>
          <div className="col">
            <AsyncAutocomplete
              fieldName="clientName"
              link="client"
              onSelect={this.handleOnClientSelect}
              onChange={this.handleOnClientSelect}
              onEdit={this.handleOnAutocompleteClientEdit}
              value={this.state.client && this.state.client}
              accessor="name"
              placeholder="Filter by Client"
              getOptions={this.getClients}
            />
          </div>
          <div className="col">
            {this.state.focus && this.state.client.name && !this.state.matter.name ? (
              <Select
                clearable={false}
                placeholder="Choose matter"
                onChange={this.handleOnMatterSelect}
                onFocus={this.handleOnFocus}
                options={this.state.options}
              />
            ) : (
              <AsyncAutocomplete
                fieldName="matterName"
                link="matter"
                onSelect={this.handleOnMatterSelect}
                onEdit={this.handleOnAutocompleteMatterEdit}
                value={this.state.matter && this.state.matter}
                accessor="name"
                placeholder="Filter by Matter"
                getOptions={this.getMatters}
              />
            )}
          </div>
        </div>
        <Searchable
          manual
          fetchedPages={this.state.fetchedPages}
          changePage={this.changePage}
          resetPages={this.resetPages}
          onPageChange={this.changePage}
          data={data}
          dataKey="timeEntries"
        >
          {() => (
            <div>
              <div style={{ marginRight: 0 }} className="row mb-3 justify-content-between">
                <div className="col col-md-auto form-inline">
                  <CustomDatePicker
                    id="date"
                    placeholderText="Date"
                    selected={this.state.date}
                    onChange={this.handleDateChange}
                    isClearable
                  />
                </div>
                <div className="col col-md-auto form-inline">
                  <CustomDatePicker
                    id="fromDate"
                    placeholderText="From Date"
                    selected={this.state.fromDate}
                    onChange={this.handleFromDateChange}
                    isClearable
                  />
                </div>
                <div className="col col-md-auto form-inline">
                  <CustomDatePicker
                    id="ToDate"
                    placeholderText="To Date"
                    selected={this.state.toDate}
                    onChange={this.handleToDateChange}
                    isClearable
                  />
                </div>
                <div className="col col-md-auto form-inline">
                  <label htmlFor="billedStatus" className="mr-sm-1">
                    Billed Status
                  </label>
                  <select
                    id="billedStatus"
                    onChange={this.handleBilledStatusChange}
                    className="form-control"
                    defaultValue="false"
                  >
                    <option value="">All</option>
                    <option value="true">Billed</option>
                    <option value="false">Unbilled</option>
                  </select>
                </div>
                <div className="col col-md-auto form-inline">
                  <label htmlFor="entryType" className="mr-sm-1">
                    Entry Type
                  </label>
                  <select
                    id="entryType"
                    onChange={this.handleEntryTypeChange}
                    className="form-control"
                    defaultValue="false"
                  >
                    <option value="0">All</option>
                    <option value="1">Matter</option>
                    <option value="2">Sales</option>
                  </select>
                </div>
                <div className="col-md-auto" style={{ marginLeft: 'auto', marginTop: 3 }}>
                  <Link href="/addtimeentry" as="/time-entries/add" prefetch>
                    <a className="btn btn-info">
                      <span>Add</span>
                    </a>
                  </Link>
                </div>
              </div>
              <UnitsCounter user={this.props.user} />
              {this.props.dataLoading && <LineLoader />}
              <PaginateTable
                detailPageAccessor="time-entry"
                page={this.state.page}
                pageNumber={this.state.page}
                pages={this.props.data.timeEntries && this.props.data.timeEntries.totalPages}
                columns={[
                  {
                    Header: 'Date entered',
                    maxWidth: 150,
                    id: 'date',
                    Cell: ({ original }) => (
                      <Cell original={original}>
                        <div>
                          {moment(original.date).format('DD/MM/YYYY')}
                          {original.recordType === 2 && <span style={{ marginLeft: '5px' }} className="badge badge-info">sales</span>}
                        </div>
                      </Cell>
                    ),
                  },
                  {
                    Header: 'Client',
                    id: 'clientName',
                    Cell: ({ original }) => (
                      <Cell original={original}>
                        <div>{original.client && original.client.name}</div>
                      </Cell>
                    ),
                  },
                  {
                    Header: 'Matter',
                    id: 'matterName',
                    Cell: ({ original }) => (
                      <Cell original={original}>
                        <div>{original.matter && original.matter.name}</div>
                      </Cell>
                    ),
                  },
                  {
                    Header: 'Description',
                    Cell: ({ original }) => (
                      <Cell original={original}>
                        <div>{original.description}</div>
                      </Cell>
                    ),
                  },
                  {
                    Header: 'Units',
                    maxWidth: 100,
                    Cell: ({ original }) => (
                      <Cell original={original}>
                        <div>{original.units}</div>
                      </Cell>
                    ),
                  },
                  {
                    Header: 'Billable Status',
                    maxWidth: 150,
                    Cell: ({ original }) => (
                      <Cell original={original}>
                        <div>{original.statusDisplay}</div>
                      </Cell>
                    ),
                  },
                  {
                    sortable: false,
                    minWidth: 10,
                    className: 'text-center',
                    Cell: ({ original }) => {
                      if (original.isBilled) {
                        return null
                      }
                      return <RemoveIcon value={original.id} onClick={this.removeTimeEntry} />
                    },
                  },
                ]}
              />
            </div>
          )}
        </Searchable>
        {/* <input type="text" onChange={this.heanlePageJump} name="pageJump" /> */}
      </Page>
    )
  }
}

const removeTimeEntry = gql`
  mutation removeClient($instanceId: ID!, $instanceType: Int!) {
    removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
      errors
    }
  }
`

export default withData(
  withAuth(
    compose(
      graphql(getTimeEntries, {
        options: user => ({
          variables: {
            isBilled: false,
            date: moment().format('DD/MM/YYYY'),
            staffName: user.id,
          },
          fetchPolicy: 'cache-and-network',
          notifyOnNetworkStatusChange: true,
        }),
      }),
      graphql(removeTimeEntry),
      graphql(getUsers, {
        name: 'staffData',
        options: { variables: { skip: true } },
      }),
      graphql(getClients, {
        name: 'clientsData',
        options: { variables: { skip: true } },
      }),
      graphql(getMatters, {
        name: 'mattersData',
        options: {
          variables: { skip: true },
        },
      }),
      connect(state => ({ dataLoading: state.page.get(TIME_ENTRIES_LOADING_STATUS) })),
    )(TimeEntry),
  ),
)
