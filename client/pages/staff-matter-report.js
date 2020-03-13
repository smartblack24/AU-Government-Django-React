import React from 'react'
import { graphql, compose, gql } from 'react-apollo'
import Link from 'next/link'

import { formatCurrency } from 'utils'
import AsyncAutocomplete from 'components/AsyncAutocomplete'
import Page from 'components/Page'
import LoadSpinner from 'components/LoadSpinner'
import Button from 'components/Button'
import withData from 'lib/withData'
import withAuth from 'lib/withAuth'

const getMatters = gql`
  query staffMatterReportMatter(
    $after: String
    $staffName: String
    $billableStatus: String
    $billableStatusExclude: Float
  ) {
    matters(
      first: 15
      after: $after
      staffName: $staffName
      billableStatus: $billableStatus
      billableStatusExclude: $billableStatusExclude
    ) {
      edges {
        cursor
        node {
          id
          name
          totalTimeValue
          totalTimeInvoiced
          wip
          billableStatusDisplay
          daysOpen
          matterStatusDisplay
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

class StaffMatterReport extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      loading: false,
      billableStatus: 0,
      staff: props.user,
    }
  }
  getUsers = async (input, callback) => {
    const { staffData } = this.props
    if (input.length > 2) {
      const response = await staffData.refetch({ skip: false, fullName: input })
      if (response.data.users.edges.length) {
        // transform to react-select format
        const options = response.data.users.edges.map(({ node }) => ({
          value: node.id,
          label: node.fullName,
        }))

        // callback with fetched data
        callback(null, { options })
      }
    }
  }
  handleStatusChange = (event) => {
    const { value } = event.target
    const { staff } = this.state
    const { mattersData } = this.props

    let billableStatus = null

    if (value !== '0') {
      billableStatus = value
    }

    mattersData.refetch({
      billableStatus,
      staffName: staff && staff.fullName,
      billableStatusExclude: null,
    })

    this.setState({ billableStatus: parseInt(value, 10) })
  }
  handleOnStaffSelect = ({ value, label }) => {
    this.setState({ staff: { id: value, fullName: label } })

    this.props.mattersData.refetch({ staffName: label })
  }
  handleOnAutocompleteEdit = () => {
    this.setState({ staff: null })

    this.props.mattersData.refetch({ staffName: null })
  }
  handleLoadMore = () => {
    const { mattersData } = this.props

    this.setState({ loading: true })

    mattersData.fetchMore({
      variables: { after: mattersData.matters.pageInfo.endCursor },
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
  render() {
    const { mattersData, user } = this.props

    let totalTimeValue = 0
    let totalInvoiced = 0
    let totalWip = 0

    if (!mattersData.loading) {
      const { matters } = mattersData

      totalTimeValue = matters.edges.reduce((x, y) => x + parseFloat(y.node.totalTimeValue), 0)
      totalInvoiced = matters.edges.reduce((x, y) => x + parseFloat(y.node.totalTimeInvoiced), 0)
      totalWip = matters.edges.reduce((x, y) => x + parseFloat(y.node.wip), 0)
    }

    return (
      <Page user={user} pageTitle="Staff Matter report">
        <div className="table-responsive" style={{ minHeight: 300 }}>
          <div style={{ marginRight: 0 }} className="row mb-sm-3 justify-content-start">
            <div className="col col-md-3">
              <AsyncAutocomplete
                fieldName="staffMember"
                link="profile"
                onSelect={this.handleOnStaffSelect}
                onEdit={this.handleOnAutocompleteEdit}
                value={this.state.staff}
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
          </div>
          {mattersData.loading ? (
            <LoadSpinner />
          ) : (
            <div>
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
                  </tr>
                </thead>
                <tbody>
                  {mattersData.matters.edges.map(({ node }) => (
                    <Link key={node.id} href={`/matter?id=${node.id}`} as={`/matter/${node.id}`}>
                      <tr>
                        <td className="w-25">{node.client && node.client.name}</td>
                        <td>{node.name}</td>
                        <td>{node.matterStatusDisplay}</td>
                        <td>{node.daysOpen}</td>
                        <td>{formatCurrency(node.totalTimeValue)}</td>
                        <td>{formatCurrency(node.totalTimeInvoiced)}</td>
                        <td>{formatCurrency(node.wip)}</td>
                      </tr>
                    </Link>
                  ))}
                  <tr className="totals">
                    <td>Total:</td>
                    <td />
                    <td />
                    <td />
                    <td>{formatCurrency(totalTimeValue)}</td>
                    <td>{formatCurrency(totalInvoiced)}</td>
                    <td>{formatCurrency(totalWip)}</td>
                    <td />
                  </tr>
                </tbody>
              </table>
              <div className="text-center mt-3">
                <Button
                  title="More"
                  loading={this.state.loading}
                  onClick={this.handleLoadMore}
                  disabled={!mattersData.matters.pageInfo.hasNextPage}
                  className="btn btn-info mt-3"
                  type="button"
                  style={{ width: 70 }}
                />
              </div>
            </div>
          )}
          <style jsx>{`
            tr {
              cursor: pointer;
            }
            .totals td {
              background-color: #898b8d;
              color: #fff;
              border: 0;
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
      graphql(getMatters, {
        name: 'mattersData',
        options: ({ user }) => ({
          variables: { staffName: user.fullName, billableStatusExclude: 3 },
        }),
      }),
      graphql(getUsers, {
        name: 'staffData',
        options: { variables: { skip: true } },
      }),
    )(StaffMatterReport),
  ),
)
