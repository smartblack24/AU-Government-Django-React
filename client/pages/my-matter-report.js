import React from 'react'
import { graphql, compose, gql } from 'react-apollo'
import { toast } from 'react-toastify'

import moment from 'moment'
import { formatCurrency } from 'utils'
import { BACKEND_URL } from 'constants/page'
import Page from 'components/Page'
import LoadSpinner from 'components/LoadSpinner'
import { matterFragment } from 'fragments'
import Button from 'components/Button'
import Modal from 'components/Modal'
import AsyncAutocomplete from 'components/AsyncAutocomplete'
import NoteForm from 'components/Note/NoteForm'
import Icon from 'components/Icon'
import withData from 'lib/withData'
import withAuth from 'lib/withAuth'

const getMatters = gql`
  query myMatterReportMatter(
    $after: String, $matterReport: String,
    $billableStatus: String, $leadType: Boolean
  ) {
    matters(
      first: 15, after: $after, matterReport: $matterReport,
      billableStatus: $billableStatus, leadType: $leadType, activeLeads: false
    ) {
      edges {
        cursor
        node {
          id
          name
          totalTimeValue
          totalTimeInvoiced
          wip
          billableStatus
          billableStatusDisplay
          matterStatusDisplay
          daysOpen
          matterStatus
          budget
          description
          billingMethod
          entryType
          client {
            id
            name
          }
          principal {
            id
          }
          manager {
            id
          }
          matterType {
            id
          }
          matterSubType {
            id
          }
          lastNote {
            id
            text
            dateTime
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
const updateMatter = gql`
  mutation updateMatter($matterId: ID!, $matterData: MatterInput!) {
    updateMatter(matterId: $matterId, matterData: $matterData) {
      errors
      matter {
        ...Matter
      }
    }
  }
  ${matterFragment}
`

const getUsers = gql`
  query staffMatterReportStaff($fullName: String, $skip: Boolean!) {
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

class MatterReport extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      billableStatus: 1,
      loading: false,
      matterReport: props.user,
      leadType: 0,
      leadTypeValue: null,
    }
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
  handleMatterStatusChange = (event) => {
    const value = parseInt(event.target.value, 10)
    const matterId = event.target.id
    const data = this.props.data.matters.edges.find(({ node }) => node.id === matterId).node
    this.updateMatter(value, data).then(() => toast.success('The changes have been saved!'))
  }
  handleOnAutocompleteEdit = () => {
    this.setState({ matterReport: null })
  }
  handleOnStaffSelect = ({ staff }) => {
    this.setState({ ...this.state, matterReport: staff, billableStatus: 1 })

    this.props.data.refetch({
      matterReport: staff.fullName,
      billableStatus: 1,
      leadType: this.state.leadTypeValue,
    })
  }
  updateMatter = (value, data) =>
    new Promise((resolve, reject) => {
      this.props
        .mutate({
          variables: {
            matterData: {
              name: data.name,
              description: data.description,
              budget: data.budget,
              billableStatus: data.billableStatus,
              billingMethod: data.billingMethod,
              matterStatus: value,
              matterType: {
                id: data.matterType.id,
              },
              client: {
                id: data.client.id,
              },
              principal: {
                id: data.principal.id,
              },
              manager: {
                id: data.manager.id,
              },
            },
            matterId: data.id,
          },
          refetchQueries: [{ query: getMatters }],
        })
        .then((response) => {
          if (response.data.updateMatter.errors.length > 0) {
            this.setState({ errors: response.data.updateMatter.errors })
            reject()
          } else {
            resolve()
          }
        })
    })
  handleStatusChange = (event) => {
    const { value } = event.target
    const { data } = this.props

    let billableStatus = null

    if (value !== '0') {
      billableStatus = value
    }

    data.refetch({
      billableStatus,
      matterReport: this.state.matterReport.fullName,
      leadType: this.state.leadTypeValue,
    })

    this.setState({ ...this.state, billableStatus: parseInt(value, 10) })
  }
  handleLeadTypeChange = (event) => {
    const { value } = event.target
    let type = null

    if (value === '1') {
      type = null
    } else if (value === '2') {
      type = false
    } else {
      type = true
    }
    this.props.data.refetch({
      billableStatus: this.state.billableStatus === 0 ? null : this.state.billableStatus,
      matterReport: this.state.matterReport.fullName,
      leadType: type,
    })
    this.setState({ ...this.state, leadType: parseInt(value, 10), leadTypeValue: type })
  }
  handleAddNoteClick = (id) => {
    this.setState({ matterId: id })
  }
  handleLoadMore = () => {
    const { data } = this.props

    this.setState({ loading: true })

    data.fetchMore({
      variables: { after: data.matters.pageInfo.endCursor },
      updateQuery: (previousResult, { fetchMoreResult }) => {
        if (!fetchMoreResult.matters) {
          return previousResult
        }

        const previousEdges = previousResult.matters.edges
        const newEdges = fetchMoreResult.matters.edges
        const newPageInfo = fetchMoreResult.matters.pageInfo
        const previousPageInfo = previousResult.matters.pageInfo

        this.setState({ loading: false })

        return {
          matters: {
            edges: [...previousEdges, ...newEdges],
            pageInfo: { ...previousPageInfo, ...newPageInfo },
            __typename: fetchMoreResult.matters.__typename,
          },
        }
      },
    })
  }
  renderPdfButton = () => (
    <a
      href={`${BACKEND_URL}/pdf/matter-report/${this.state.matterReport && this.state.matterReport.id}/${
        this.state.billableStatus !== 0 ? this.state.billableStatus : ''
      }`}
      target="_blank"
      className="btn btn-success"
    >
      <i className="fa fa-download" /> PDF
    </a>
  )
  render() {
    const { data, user } = this.props
    if (data.loading) {
      return (
        <Page pageTitle="My Matter report" user={user}>
          <LoadSpinner />
        </Page>
      )
    }

    const { matters } = data

    const totalTimeValue = matters.edges.reduce((x, y) => x + parseFloat(y.node.totalTimeValue), 0)
    const totalInvoiced = matters.edges.reduce(
      (x, y) => x + parseFloat(y.node.totalTimeInvoiced),
      0,
    )
    const totalWip = matters.edges.reduce((x, y) => x + parseFloat(y.node.wip), 0)
    return (
      <Page user={user} pageTitle="My Matter report" renderRight={this.renderPdfButton()}>
        <div className="table-responsive" style={{ minHeight: 300 }}>
          <div style={{ marginRight: 0 }} className="row mb-sm-3 justify-content-start">
            <div className="col col-md-auto mt-xs-3 mt-md-auto">
              <Modal id="addNoteModal" title="Add a note" key={1}>
                <NoteForm matterId={this.state.matterId} matters={matters} user={this.props.user} />
              </Modal>
            </div>
            <div className="col col-md-2">
              <AsyncAutocomplete
                fieldName="matterReport"
                link="profile"
                onSelect={this.handleOnStaffSelect}
                onEdit={this.handleOnAutocompleteEdit}
                value={this.state.matterReport}
                accessor="fullName"
                placeholder="Search for staff member"
                getOptions={this.getUsers}
              />
            </div>
            <div className="col col-md-auto form-inline mt-xs-3 mt-md-auto">
              <label htmlFor="billableStatus" className="mr-sm-2">
                Billable Status
              </label>
              <select
                id="billableStatus"
                onChange={this.handleStatusChange}
                value={this.state.billableStatus}
                className="form-control"
              >
                <option value={0}>All</option>
                <option value={1}>Open</option>
                <option value={2}>Suspended</option>
                <option value={3}>Closed</option>
              </select>
            </div>
            <div className="col col-md-auto form-inline mt-xs-3 mt-md-auto">
              <label htmlFor="matterType" className="mr-sm-2">
                Type
              </label>
              <select
                id="leadType"
                onChange={this.handleLeadTypeChange}
                value={this.state.leadType}
                className="form-control"
              >
                <option value={1}>All</option>
                <option value={2}>Matter</option>
                <option value={3}>Sales</option>
              </select>
            </div>
          </div>
          <table id="mainTable" className="table table-bordered table-striped m-b-0">
            <thead>
              <tr>
                <th>Client</th>
                <th>Matter</th>
                <th>Matter status</th>
                <th>Days open</th>
                <th>Time Value</th>
                <th>Invoiced</th>
                <th>WIP</th>
                <th>Date of last note</th>
                <th>Last Note details</th>
                <th>Add Note</th>
              </tr>
            </thead>
            <tbody>
              {matters.edges.map(({ node }) => (
                <tr key={node.id}>
                  <td className="w-25">{node.client && node.client.name}</td>
                  {node.entryType === 1
                    ? (
                      <td>
                        <a target="_blank" href={`/matter/${node.id}`} style={{ color: '#67757c' }}>
                          {node.name}
                          {node.entryType === 2 && <span style={{ marginLeft: '5px' }} className="badge badge-info">sales</span>}
                        </a>
                      </td>
                    )
                    : (
                      <td>
                        <a target="_blank" href={`/lead/${node.id}`}>
                          {node.name}
                          {node.entryType === 2 && <span style={{ marginLeft: '5px' }} className="badge badge-info">sales</span>}
                        </a>
                      </td>
                    )
                  }
                  <td>
                    <div className="col col-md-auto form-inline mt-xs-3 mt-md-auto">
                      <select
                        id={node.id}
                        onChange={this.handleMatterStatusChange}
                        value={node.matterStatus}
                        className="form-control"
                      >
                        <option value={0}>----------------</option>
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
                    </div>
                  </td>
                  <td>{node.daysOpen}</td>
                  <td>{formatCurrency(node.totalTimeValue)}</td>
                  <td>{formatCurrency(node.totalTimeInvoiced)}</td>
                  <td>{formatCurrency(node.wip)}</td>
                  <th id="date">
                    {node.lastNote && moment(node.lastNote.dateTime).format('DD/MM/YYYY')}
                  </th>
                  <td>{node.lastNote && node.lastNote.text}</td>
                  <td>
                    <Icon
                      name="plus"
                      value={node.id}
                      onClick={this.handleAddNoteClick}
                      dataToggle="modal"
                      dataTarget="#addNoteModal"
                    />
                  </td>
                </tr>
              ))}
              <tr className="totals">
                <td>TOTAL:</td>
                <td />
                <td />
                <td />
                <td>{formatCurrency(totalTimeValue)}</td>
                <td>{formatCurrency(totalInvoiced)}</td>
                <td>{formatCurrency(totalWip)}</td>
                <td />
                <td />
                <td />
              </tr>
            </tbody>
          </table>
          <div className="text-center mt-3">
            <Button
              title="More"
              loading={this.state.loading}
              onClick={this.handleLoadMore}
              disabled={!data.matters.pageInfo.hasNextPage}
              className="btn btn-info mt-3"
              type="button"
              style={{ width: 70 }}
            />
          </div>
          <style jsx>{`
            tr {
              cursor: pointer;
            }
            .totals td {
              background-color: #898b8d;
              color: #fff;
              border: 0;
            }
            #date {
              font-weight: 300;
            }
          `}</style>
        </div>
      </Page>
    )
  }
}

export default withData(
  withAuth(
    compose(
      graphql(updateMatter),
      graphql(getUsers, {
        name: 'staffData',
        options: { variables: { skip: true } },
      }),
      graphql(getMatters, { options: ({ user }) => (
        { variables: {
          billableStatus: 1,
          matterReport: user.fullName,
        } }) }),
    )(MatterReport),
  ),
)
