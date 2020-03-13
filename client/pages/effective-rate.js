import React from 'react'
import { graphql, gql, compose } from 'react-apollo'
import Head from 'next/head'
import 'react-dates/initialize'
import { DateRangePicker } from 'react-dates'

import Page from 'components/Page'
import Button from 'components/Button'
import AsyncAutocomplete from 'components/AsyncAutocomplete'
import EffectiveRateChart from 'components/Reporting/EffectiveRateChart'
import withData from 'lib/withData'
import withAuth from 'lib/withAuth'

const getEffectiveRate = gql`
  query effectiveRateReports($staffMemberId: ID, $toDate: String, $fromDate: String) {
    effectiveRateReports(staffMemberId: $staffMemberId, toDate: $toDate, fromDate: $fromDate) {
      id
      date
      value
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

class EffectiveRate extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      staffMember: props.user,
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
  handleSelectChange = ({ value, label }) =>
    this.setState({ staffMember: { id: value, fullName: label } })
  handleRefetchData = () => {
    const { staffMember, fromDate, toDate } = this.state
    this.props.reports.refetch({ staffMemberId: staffMember.id, fromDate, toDate, skip: false })
  }
  handleDatesChange = ({ startDate, endDate }) => {
    this.setState({ fromDate: startDate, toDate: endDate })
  }
  handleOnAutocompleteEdit = () => this.setState({ staffMember: null })
  handleFocusChange = focusedInput => this.setState({ focusedInput })
  render() {
    return (
      <Page user={this.props.user} wrappedByCard={false} pageTitle="Effective Rate">
        <Head>
          <link rel="stylesheet" href="/static/css/datepicker.css" />
        </Head>
        <div className="row">
          <div className="col-12">
            <div className="card">
              <div className="card-body">
                <div className="row justify-content-between">
                  <div className="col col-md-auto row justify-content-between">
                    <div className="col">
                      <AsyncAutocomplete
                        style={{ width: 300, height: '100%' }}
                        wrapperStyle={{ height: '100%' }}
                        fieldName="staff"
                        onSelect={this.handleSelectChange}
                        onEdit={this.handleOnAutocompleteEdit}
                        name="form-field-name"
                        value={this.state.staffMember}
                        accessor="fullName"
                        placeholder="Select a Staff member"
                        getOptions={this.getUsers}
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
                    <Button
                      loading={this.props.reports.loading}
                      onClick={this.handleRefetchData}
                      className="btn btn-info btn-md"
                      title="Update"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col-12">
            <div className="card">
              <div className="card-body">
                <EffectiveRateChart user={this.props.user} data={this.props.reports} />
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
      graphql(getUsers, { name: 'staffData', options: { variables: { skip: true } } }),
      graphql(getEffectiveRate, { name: 'reports' }),
    )(EffectiveRate),
  ),
)
