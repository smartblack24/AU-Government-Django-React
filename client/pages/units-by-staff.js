import React from 'react'
import { graphql, gql, compose } from 'react-apollo'
import Head from 'next/head'
import { Async } from 'react-select'
import 'react-dates/initialize'
import { DateRangePicker } from 'react-dates'

import Page from 'components/Page'
import UnitsByStaffChart from 'components/Reporting/UnitsByStaffChart'
import withData from 'lib/withData'
import withAuth from 'lib/withAuth'

const getBillableUnitsByStaff = gql`
  query unitsByStaffReports(
    $billed: Boolean
    $staffMembers: [ID]
    $fromDate: String
    $toDate: String
    $skip: Boolean!
  ) {
    unitsByStaffReports(
      billed: $billed
      staffMembers: $staffMembers
      fromDate: $fromDate
      toDate: $toDate
    ) @skip(if: $skip) {
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

class BillableUnitsByStaff extends React.Component {
  state = {}
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
  handleRefetchData = async () => {
    let staffMembers = []
    let fromDate = null
    let toDate = null

    if (this.state.staffMembers) {
      staffMembers = this.state.staffMembers.map(staff => staff.value)
    }

    if (this.state.fromDate) {
      fromDate = this.state.fromDate.format('YYYY-MM-DD')
    }

    if (this.state.toDate) {
      toDate = this.state.toDate.format('YYYY-MM-DD')
    }

    await this.props.billableUnitsData.refetch({
      staffMembers,
      fromDate,
      toDate,
      billed: false,
      skip: false,
    })
    this.props.billedUnitsData.refetch({
      staffMembers,
      fromDate,
      toDate,
      billed: true,
      skip: false,
    })
  }
  handleDatesChange = ({ startDate, endDate }) => {
    this.setState({ fromDate: startDate, toDate: endDate })
  }
  handleFocusChange = focusedInput => this.setState({ focusedInput })
  render() {
    const { billableUnitsData, billedUnitsData, user } = this.props
    return (
      <Page user={user} wrappedByCard={false} pageTitle="Units by staff report">
        <Head>
          <link rel="stylesheet" href="/static/css/react-select.min.css" />
          <link rel="stylesheet" href="/static/css/datepicker.css" />
        </Head>
        <div className="row">
          <div className="col-md-12">
            <div className="card">
              <div className="card-body">
                <div className="row justify-content-between">
                  <div className="col col-md-auto row justify-content-between">
                    <div className="col">
                      <Async
                        multi
                        autoload={false}
                        cache={false}
                        style={{ width: 300, height: '100%' }}
                        wrapperStyle={{ height: '100%' }}
                        onChange={this.handleSelectChange}
                        name="form-field-name"
                        placeholder="Select a Staff member"
                        value={this.state.staffMembers}
                        loadOptions={this.getUsers}
                      />
                    </div>
                    <div className="col col-md-auto">
                      <DateRangePicker
                        startDate={this.state.fromDate}
                        startDateId="1"
                        isOutsideRange={() => false}
                        endDateId="2"
                        endDate={this.state.toDate}
                        onDatesChange={this.handleDatesChange}
                        focusedInput={this.state.focusedInput}
                        onFocusChange={this.handleFocusChange}
                      />
                    </div>
                  </div>
                  <div className="col col-md-auto">
                    <button onClick={this.handleRefetchData} className="btn btn-info btn-md">
                      Update
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className="col-md-6">
            <div className="card">
              <div className="card-body">
                <h3 className="card-title">Billable units by staff</h3>
                {billableUnitsData.unitsByStaffReports && (
                  <UnitsByStaffChart data={billableUnitsData} loading={billedUnitsData.loading} />
                )}
              </div>
            </div>
          </div>
          <div className="col-md-6">
            <div className="card">
              <div className="card-body">
                <h3 className="card-title">Billed units by staff</h3>
                {billedUnitsData.unitsByStaffReports && (
                  <UnitsByStaffChart data={billedUnitsData} loading={billableUnitsData.loading} />
                )}
              </div>
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
      graphql(getBillableUnitsByStaff, {
        name: 'billableUnitsData',
        options: { variables: { billed: false, skip: true }, notifyOnNetworkStatusChange: true },
      }),
      graphql(getBillableUnitsByStaff, {
        name: 'billedUnitsData',
        options: { variables: { billed: true, skip: true } },
      }),
      graphql(getUsers, {
        name: 'staffData',
        options: { variables: { skip: true }, notifyOnNetworkStatusChange: true },
      }),
    )(BillableUnitsByStaff),
  ),
)
