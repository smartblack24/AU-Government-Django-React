import React from 'react'
import PropTypes from 'prop-types'

import withAuth from 'lib/withAuth'
import withData from 'lib/withData'
import Page from 'components/Page'
import ActiveMattersChart from 'components/Reporting/ActiveMattersChart'
import NewMattersChart from 'components/Reporting/NewMattersChart'
import NewEntities from 'components/Reporting/NewEntities'
import BillableUnitsChart from 'components/Reporting/BillableUnitsChart'
import OpenMattersChart from 'components/Reporting/OpenMattersChart'
import GaugesList from 'components/Gauges'

const renderRefetchButton = onClick => (
  <button onClick={onClick} className="btn btn-info">
    Update
  </button>
)

class Dashboard extends React.Component {
  state = { shouldRefetch: false }
  refetchData = () =>
    this.setState({ shouldRefetch: true }, () => this.setState({ shouldRefetch: false }))
  render() {
    return (
      <Page
        user={this.props.user}
        wrappedByCard={false}
        renderRight={renderRefetchButton(this.refetchData)}
      >
        <div>
          <div className="row page-titles justify-content-between">
            <div className="col-md-5 col-8 align-self-center">
              <h3 className="text-themecolor m-b-0 m-t-0">{'Who is busy?'}</h3>
            </div>
          </div>
          <GaugesList shouldRefetch={this.state.shouldRefetch} />
          <div className="row">
            <div className="col-md-6">
              <div className="card">
                <div className="card-body">
                  <h3 className="card-title">Active Matters</h3>
                  <ActiveMattersChart shouldRefetch={this.state.shouldRefetch} />
                </div>
              </div>
            </div>
            <div className="col-md-6">
              <div className="card">
                <div className="card-body">
                  <h3 className="card-title">New Matters</h3>
                  <NewMattersChart shouldRefetch={this.state.shouldRefetch} />
                </div>
              </div>
            </div>
            <div className="col-md-6">
              <div className="card">
                <div className="card-body">
                  <h3 className="card-title">New Entities</h3>
                  <NewEntities shouldRefetch={this.state.shouldRefetch} />
                </div>
              </div>
            </div>
            <div className="col-md-6">
              <div className="card">
                <div className="card-body">
                  <h3 className="card-title">Billable units</h3>
                  <BillableUnitsChart shouldRefetch={this.state.shouldRefetch} />
                </div>
              </div>
            </div>
            <div className="col-md-6">
              <div className="card">
                <div className="card-body">
                  <h3 className="card-title">Open matters</h3>
                  <OpenMattersChart shouldRefetch={this.state.shouldRefetch} />
                </div>
              </div>
            </div>
          </div>
        </div>
      </Page>
    )
  }
}

Dashboard.propTypes = {
  user: PropTypes.shape({
    id: PropTypes.string.isRequired,
    firstName: PropTypes.string.isRequired,
    lastName: PropTypes.string.isRequired,
    fullName: PropTypes.string.isRequired,
    email: PropTypes.string.isRequired,
  }).isRequired,
}

export default withData(withAuth(Dashboard))
