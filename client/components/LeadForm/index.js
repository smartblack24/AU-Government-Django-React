import React from 'react'
import moment from 'moment'

import { Tab } from 'utils'
import Notes from 'components/Note/Notes'
import Details from './Details'
import UnbilledTime from './UnbilledTime'

class LeadForm extends React.PureComponent {
  constructor(props) {
    super(props)

    this.state = {
      availableTabs: props.wizard ? [] : [1, 2, 3],
      tab: 1,
    }
  }
  selectTab = tab => this.setState({ tab, availableTabs: this.state.availableTabs.concat(tab) })
  render() {
    const initialValues = {
      ...this.props.initialValues,
      conflictCheckSent: this.props.initialValues.conflictCheckSent
        ? moment(this.props.initialValues.conflictCheckSent).format('DD/MM/YYYY')
        : '',
      standardTermsSent: this.props.initialValues.standardTermsSent
        ? moment(this.props.initialValues.standardTermsSent).format('DD/MM/YYYY')
        : '',
      referrerThanked: this.props.initialValues.conflictCheckSent
        ? moment(this.props.initialValues.referrerThanked).format('DD/MM/YYYY')
        : '',
      leadDate: this.props.initialValues.leadDate
        ? moment(this.props.initialValues.leadDate).format('YYYY-MM-DD')
        : moment().format('YYYY-MM-DD'),
    }
    return (
      <div className="card">
        <ul className="nav nav-tabs profile-tab" role="tablist">
          <Tab number={1} currentNumber={this.state.tab} onClick={this.selectTab}>
            Details
          </Tab>
          <Tab
            number={2}
            currentNumber={this.state.tab}
            onClick={this.selectTab}
            disabled={!this.state.availableTabs.includes(2)}
          >
            Notes
          </Tab>
          <Tab
            number={3}
            currentNumber={this.state.tab}
            onClick={this.selectTab}
            disabled={!this.state.availableTabs.includes(3)}
          >
            Time
          </Tab>
        </ul>
        <div className="card-body">
          {this.state.tab === 1 && (
            <Details
              wizard={this.props.wizard}
              initialValues={initialValues}
              buttonTitle={this.props.buttonTitle}
              onSubmit={this.props.onSubmit}
            />
          )}
          {this.state.tab === 2 && (
            <Notes
              matterId={this.props.initialValues.id}
              user={this.props.user}
              notes={this.props.initialValues.notes}
            />
          )}
          {this.state.tab === 3 && (
            <UnbilledTime
              user={this.props.user}
              initialValues={this.props.initialValues}
              buttonTitle={this.props.buttonTitle}
              onSubmit={this.props.onSubmit}
            />
          )}
        </div>
      </div>
    )
  }
}

export default LeadForm
