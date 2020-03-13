import React, { PureComponent } from 'react'
import { destroy } from 'redux-form'
import { connect } from 'react-redux'
import { gql, graphql, compose } from 'react-apollo'
import { get, pick } from 'lodash'
import { Tab } from 'utils'
import Emails from 'components/Emails'
import Notes from 'components/Note/Notes'
import SafeStorage from 'components/SafeStorage'
import Details from './Details'
import Location from './Location'
import Organisations from './Organisations'
import Relationships from './Relationships'
import Clients from './Clients'

class ContactForm extends PureComponent {
  static defaultProps = {
    initialValues: {},
  }

  constructor(props) {
    super(props)

    this.state = {
      tabIndex: 1,
      availableTabs: props.wizard ? [] : [1, 2, 3, 4, 5, 6, 7, 8, 9],
    }
  }

  componentWillUnmount() {
    this.props.dispatch(destroy('contactForm'))
  }

  getComposedInitialValues = () => {
    const { initialValues } = this.props
    const { location, postalLocation, organisations, referrers } = initialValues

    return {
      ...location,
      ...postalLocation,
      ...initialValues,
      organisations: organisations ? organisations.edges : [],
      referrers: referrers ? referrers.edges : [],
    }
  }

  stub = () => ({})

  selectTab = tabIndex =>
    this.setState({ tabIndex, availableTabs: this.state.availableTabs.concat(tabIndex) })

  render() {
    const { buttonTitle, initialValues, user, wizard, onSubmitFunc } = this.props
    const { id: contactId, notes, linkMails } = initialValues
    const { tabIndex, availableTabs } = this.state
    const composedInitialValues = this.getComposedInitialValues()
    const { mailEnabled, canLinkMails, canDeleteMails } = pick(get(user, 'me'), ['mailEnabled', 'canLinkMails', 'canDeleteMails'])

    return (
      <div className="card">
        <ul className="nav nav-tabs profile-tab" role="tablist">
          <Tab number={1} currentNumber={tabIndex} onClick={this.selectTab}>
            Details
          </Tab>
          <Tab
            number={2}
            currentNumber={tabIndex}
            onClick={availableTabs.includes(2) ? this.selectTab : this.stub}
            disabled={!availableTabs.includes(2)}
          >
            Location
          </Tab>
          <Tab
            number={3}
            currentNumber={tabIndex}
            onClick={availableTabs.includes(3) ? this.selectTab : this.stub}
            disabled={!availableTabs.includes(3)}
          >
            Organisations
          </Tab>
          <Tab
            number={8}
            currentNumber={tabIndex}
            onClick={availableTabs.includes(8) ? this.selectTab : this.stub}
            disabled={!availableTabs.includes(8)}
          >
            Clients
          </Tab>
          <Tab
            number={4}
            currentNumber={tabIndex}
            onClick={availableTabs.includes(4) ? this.selectTab : this.stub}
            disabled={!availableTabs.includes(4)}
          >
            Relationships
          </Tab>
          <Tab
            number={5}
            currentNumber={tabIndex}
            onClick={availableTabs.includes(5) ? this.selectTab : this.stub}
            disabled={!availableTabs.includes(5)}
          >
            Marketing
          </Tab>
          {!wizard && mailEnabled && linkMails && (
            <Tab
              number={6}
              currentNumber={tabIndex}
              onClick={availableTabs.includes(6) ? this.selectTab : this.stub}
              disabled={!availableTabs.includes(6)}
            >
              Emails
            </Tab>
          )}
          <Tab
            number={7}
            currentNumber={tabIndex}
            onClick={availableTabs.includes(7) ? this.selectTab : this.stub}
            disabled={!availableTabs.includes(7)}
          >
            Safe Storage
          </Tab>
          <Tab
            number={9}
            currentNumber={tabIndex}
            onClick={availableTabs.includes(9) ? this.selectTab : this.stub}
            disabled={!availableTabs.includes(9)}
          >
            Notes
          </Tab>
        </ul>
        <div className="card-body">
          {tabIndex === 1 && (
            <Details
              formNumber={1}
              wizard={wizard}
              initialValues={composedInitialValues}
              canLinkMails={canLinkMails}
              onSubmitFunc={wizard ? this.selectTab : onSubmitFunc}
              buttonTitle={wizard ? 'Next' : buttonTitle}
            />
          )}
          {tabIndex === 2 && (
            <Location
              formNumber={2}
              wizard={wizard}
              initialValues={composedInitialValues}
              onSubmitFunc={wizard ? this.selectTab : onSubmitFunc}
              buttonTitle={wizard ? 'Next' : buttonTitle}
            />
          )}
          {tabIndex === 3 && (
            <Organisations
              formNumber={3}
              wizard={wizard}
              contactId={contactId}
              initialValues={composedInitialValues}
              onSubmitFunc={wizard ? this.selectTab : onSubmitFunc}
              buttonTitle={wizard ? 'Next' : buttonTitle}
            />
          )}
          {tabIndex === 4 && (
            <Relationships
              formNumber={4}
              initialValues={composedInitialValues}
              onSubmitFunc={onSubmitFunc}
            />
          )}
          {tabIndex === 5 && 'Marketing'}
          {tabIndex === 6 && mailEnabled && linkMails && <Emails contactId={contactId} canDeleteMails={canDeleteMails} />}
          {tabIndex === 7 && <SafeStorage contactId={contactId} />}
          {tabIndex === 8 && <Clients contactId={contactId} />}
          {tabIndex === 9 && <Notes contactId={contactId} user={user.me} notes={notes} />}
        </div>
      </div>
    )
  }
}

const getUser = gql`
  query me {
    me {
      id
      mailEnabled
      canLinkMails
      canDeleteMails
    }
  }
`

export default compose(
  graphql(getUser, { name: 'user' }),
  connect(),
)(ContactForm)
