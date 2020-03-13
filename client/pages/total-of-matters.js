import React from 'react'
import { graphql, gql, compose } from 'react-apollo'
import Head from 'next/head'
import { Async } from 'react-select'

import Page from 'components/Page'
import LoadSpinner from 'components/LoadSpinner'
import TotalOfMattersByStaffChart from 'components/Reporting/TotalOfMattersByStaffChart'
import withData from 'lib/withData'
import withAuth from 'lib/withAuth'

const getTotalOfMatters = gql`
  query totalOfMattersByStaffReports($staffMembers: [ID], $matterStatus: Int, $skip: Boolean!) {
    totalOfMattersByStaffReports(staffMembers: $staffMembers, matterStatus: $matterStatus)
      @skip(if: $skip) {
      id
      date
      staffMembers {
        id
        name
        count
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

class TotalOfMattersByStaff extends React.Component {
  state = { matterStatus: 3 }
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
  handleSelectChange = staffMembers => this.setState({ staffMembers })
  handleStatusChange = (event) => {
    const { matterStatus } = this.state
    this.setState({ matterStatus: event.target.value })

    let staffMembers = []

    if (this.state.staffMembers) {
      staffMembers = this.state.staffMembers.map(staff => staff.value)
    }

    this.props.reportData.refetch({ staffMembers, matterStatus, skip: false })
  }
  handleRefetchData = () => {
    let staffMembers = []
    const { matterStatus } = this.state

    if (this.state.staffMembers) {
      staffMembers = this.state.staffMembers.map(staff => staff.value)
    }

    this.props.reportData.refetch({ staffMembers, matterStatus, skip: false })
  }
  render() {
    const { user, reportData } = this.props
    if (reportData.loading) {
      return (
        <Page user={user}>
          <LoadSpinner />
        </Page>
      )
    }

    return (
      <Page user={user} wrappedByCard={false} pageTitle="Total of Matters by Staff">
        <Head>
          <link rel="stylesheet" href="/static/css/react-select.min.css" />
        </Head>
        <div className="card">
          <div className="card-body">
            <div className="row justify-content-between">
              <div className="col col-md-auto">
                <div className="row">
                  <div className="col col-md-auto">
                    <Async
                      multi
                      autoload={false}
                      cache={false}
                      style={{ width: 400, height: '100%' }}
                      onChange={this.handleSelectChange}
                      name="form-field-name"
                      placeholder="Select a Staff member"
                      value={this.state.staffMembers}
                      loadOptions={this.getUsers}
                    />
                  </div>
                  <div className="col col-md-auto">
                    <div className="col col-md-auto">
                      <select
                        value={this.state.matterStatus}
                        onChange={this.handleStatusChange}
                        className="form-control"
                      >
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
                  </div>
                </div>
              </div>
              <div className="col col-md-auto">
                <button onClick={this.handleRefetchData} className="btn btn-info">
                  Update
                </button>
              </div>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="card-body">
            {reportData.totalOfMattersByStaffReports && (
              <TotalOfMattersByStaffChart data={reportData} />
            )}
          </div>
        </div>
      </Page>
    )
  }
}

export default withData(
  withAuth(
    compose(
      graphql(getTotalOfMatters, { name: 'reportData', options: { variables: { skip: true } } }),
      graphql(getUsers, { name: 'staffData', options: { variables: { skip: true } } }),
    )(TotalOfMattersByStaff),
  ),
)
