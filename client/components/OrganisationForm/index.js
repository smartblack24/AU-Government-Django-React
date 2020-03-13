import React, { Component } from 'react'
import { destroy } from 'redux-form'
import { connect } from 'react-redux'
import { gql, graphql, compose } from 'react-apollo'
import { get, pick } from 'lodash'
import { Tab } from 'utils'
import Emails from 'components/Emails'
import SafeStorage from 'components/SafeStorage'
import Details from './Details'
import Location from './Location'
import ContactsAndClients from './ContactsAndClients'

class OrganisationForm extends Component {
  static defaultProps = {
    availableTabs: [1, 2, 3, 4, 5],
    resetAfterSubmit: false,
  }
  constructor(props) {
    super(props)

    this.state = {
      form: 1,
      availableForms: props.wizard ? [] : [1, 2, 3, 4, 5],
    }
  }

  componentWillUnmount = () => {
    this.props.dispatch(destroy('organisationForm'))
  }

  getButtonTitle = (formNumber) => {
    const { availableTabs, buttonTitle, wizard } = this.props
    if (availableTabs[availableTabs.length - 1] === formNumber) {
      return buttonTitle
    } else if (wizard) {
      return 'Next'
    }

    return buttonTitle
  }

  getComposedInitialValues = () => {
    const { initialValues } = this.props
    const { location, postalLocation, groupStatus, groupParent, industry, contacts } = initialValues

    return {
      ...location,
      ...postalLocation,
      ...initialValues,
      groupParent: parseInt(groupStatus, 10) === 1 && !groupParent ? initialValues : groupParent,
      industryId: industry && industry.id,
      contacts: contacts ? contacts.edges : [],
    }
  }

  getOnSubmitFunc = (formNumber) => {
    const { availableTabs, wizard, onSubmitFunc } = this.props
    if (availableTabs.includes(formNumber + 1) && wizard) {
      return this.selectForm(formNumber + 1)
    }

    return onSubmitFunc
  }

  stumb = () => ({})

  selectForm = form => () => {
    const { availableForms } = this.state
    this.setState({ form, availableForms: availableForms.concat(form) })
  }

  render() {
    const { availableTabs, buttonTitle, initialValues, user, wizard, onSubmitFunc, resetAfterSubmit } = this.props
    const { id: organisationId, linkMails } = initialValues
    const { form, availableForms } = this.state
    const composedInitialValues = this.getComposedInitialValues()
    const { mailEnabled, canLinkMails, canDeleteMails } = pick(get(user, 'me'), ['mailEnabled', 'canLinkMails', 'canDeleteMails'])

    return (
      <div className="card">
        <ul className="nav nav-tabs profile-tab" role="tablist">
          {availableTabs.includes(1) && (
            <Tab number={1} currentNumber={form} onClick={this.selectForm(1)}>
              Details
            </Tab>
          )}
          {availableTabs.includes(2) && (
            <Tab
              number={2}
              currentNumber={form}
              onClick={availableForms.includes(2) ? this.selectForm(2) : this.stub}
              disabled={!availableForms.includes(2)}
            >
              Location
            </Tab>
          )}
          {availableTabs.includes(3) && (
            <Tab
              number={3}
              currentNumber={form}
              onClick={availableForms.includes(3) ? this.selectForm(3) : this.stub}
              disabled={!availableForms.includes(3)}
            >
              Associated Contacts & Client
            </Tab>
          )}
          {!wizard && mailEnabled && linkMails && (
            <Tab
              number={4}
              currentNumber={form}
              onClick={availableForms.includes(4) ? this.selectForm(4) : this.stub}
              disabled={!availableForms.includes(4)}
            >
              Emails
            </Tab>
          )}
          {availableTabs.includes(5) && (
            <Tab
              number={5}
              currentNumber={form}
              onClick={availableForms.includes(5) ? this.selectForm(5) : this.stub}
              disabled={!availableForms.includes(5)}
            >
              Safe Storage
            </Tab>
          )}
        </ul>
        <div className="card-body">
          {form === 1 && (
            <Details
              formNumber={1}
              wizard={wizard}
              buttonTitle={wizard ? 'Next' : buttonTitle}
              initialValues={composedInitialValues}
              canLinkMails={canLinkMails}
              onSubmitFunc={wizard ? this.selectForm(2) : onSubmitFunc}
            />
          )}
          {form === 2 && (
            <Location
              formNumber={2}
              wizard={wizard}
              buttonTitle={this.getButtonTitle(2)}
              initialValues={composedInitialValues}
              onSubmitFunc={this.getOnSubmitFunc(2)}
            />
          )}
          {form === 3 && (
            <ContactsAndClients
              resetAfterSubmit={resetAfterSubmit}
              wizard={wizard}
              buttonTitle={buttonTitle}
              initialValues={composedInitialValues}
              onSubmitFunc={onSubmitFunc}
            />
          )}
          {form === 4 && mailEnabled && linkMails && <Emails organisationId={organisationId} canDeleteMails={canDeleteMails} />}
          {form === 5 && <SafeStorage organisationId={organisationId} />}
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
)(OrganisationForm)
