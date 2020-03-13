import React, { PureComponent } from 'react'
import { get } from 'lodash'
import moment from 'moment'
import { Tab } from 'utils'
import Emails from 'components/Emails'
import Notes from 'components/Note/Notes'
import Details from './Details'
import UnbilledTime from './UnbilledTime'
import Invoices from './Invoices'

class MatterForm extends PureComponent {
  constructor(props) {
    super(props)

    this.state = {
      availableTabs: props.wizard ? [] : [1, 2, 3],
      tab: 1,
    }
  }

  selectTab = tab => this.setState({ tab, availableTabs: this.state.availableTabs.concat(tab) })

  render() {
    const { buttonTitle, user, wizard, onSubmit } = this.props
    const { id: matterId, notes, invoices } = this.props.initialValues
    const { availableTabs, tab } = this.state
    const mailEnabled = get(user, 'mailEnabled', false)
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
    }
    return (
      <div className="card">
        <ul className="nav nav-tabs profile-tab" role="tablist">
          <Tab number={1} currentNumber={tab} onClick={this.selectTab}>
            Details
          </Tab>
          <Tab
            number={2}
            currentNumber={tab}
            onClick={this.selectTab}
            disabled={!availableTabs.includes(2)}
          >
            Notes
          </Tab>
          <Tab
            number={3}
            currentNumber={tab}
            onClick={this.selectTab}
            disabled={!availableTabs.includes(3)}
          >
            Unbilled Time
          </Tab>
          <Tab
            number={4}
            currentNumber={tab}
            onClick={this.selectTab}
            disabled={wizard}
          >
            Invoices
          </Tab>
          {!wizard && mailEnabled &&
            <Tab
              number={5}
              currentNumber={tab}
              onClick={this.selectTab}
            >
              Emails
            </Tab>
          }
        </ul>
        <div className="card-body">
          {tab === 1 && (
            <Details
              wizard={wizard}
              initialValues={initialValues}
              buttonTitle={buttonTitle}
              onSubmit={onSubmit}
            />
          )}
          {tab === 2 && (
            <Notes
              matterId={matterId}
              user={user}
              notes={notes}
            />
          )}
          {tab === 3 && (
            <UnbilledTime
              user={user}
              initialValues={initialValues}
              buttonTitle={buttonTitle}
              onSubmit={onSubmit}
            />
          )}
          {tab === 4 && (
            <Invoices
              matterId={matterId}
              invoices={invoices}
            />
          )}
          {tab === 5 && mailEnabled && <Emails matterId={matterId} />}
        </div>
      </div>
    )
  }
}

export default MatterForm
