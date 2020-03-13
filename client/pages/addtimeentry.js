import React from 'react'
import moment from 'moment'

import Page from 'components/Page'
import withData from 'lib/withData'
import withAuth from 'lib/withAuth'
import { Tab } from 'utils'
import TimeEntryForm from 'components/TimeEntryForm'


class AddTimeEntry extends React.Component {
  state = {
    tab: 1,
    availableForms: [1, 2],
    lead: false,
    status: 1,
  }
  selectForm = (tab) => {
    console.log(tab)
    let status = 1
    let lead = false
    if (tab === 2) {
      lead = true
      status = 2
    }
    this.setState({ tab, lead, status })
  }
  render() {
    return (
      <Page user={this.props.user} pageTitle="Add a time entry">
        <div className="card">
          <ul className="nav nav-tabs profile-tab" role="tablist">
            <Tab
              number={1}
              currentNumber={this.state.tab}
              onClick={this.selectForm}
            >
              Matter Time Entry
            </Tab>
            <Tab
              number={2}
              currentNumber={this.state.tab}
              onClick={this.selectForm}
            >
              Lead Time Entry
            </Tab>
          </ul>
        </div>
        <div className="card-body">
          <TimeEntryForm
            buttonTitle="Add"
            initialValues={{
              date: moment().format('YYYY-MM-DD'),
              status: this.state.status,
              gstStatus: 1,
              staffMember: this.props.user,
              staffMemberId: this.props.user.id,
              rate: this.props.user.rate,
            }}
            lead={this.state.lead}
          />
        </div>
      </Page>
    )
  }
}


export default withData(withAuth(AddTimeEntry))
