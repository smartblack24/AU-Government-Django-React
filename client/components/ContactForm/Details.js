import React, { Fragment } from 'react'
import PropTypes from 'prop-types'
import { reduxForm, Field, change } from 'redux-form'
import { gql, graphql, compose } from 'react-apollo'
import Cookies from 'js-cookie'
import { createApolloFetch } from 'apollo-fetch'
import { filter } from 'graphql-anywhere'
import moment from 'moment'
import swal from 'sweetalert'

import { BACKEND_URL } from 'constants/page'
import Button from 'components/Button'
import {
  renderInput,
  renderSelect,
  normalizePhone,
  Input,
  normalizeCurrency,
  // formatDate,
} from 'utils'
import { contactFragment } from 'fragments'
import CustomDatePicker from 'components/DatePicker'
import { getMails } from 'queries'
import doc from './doc'

const getOccupations = gql`
  query occupations {
    occupations {
      id
      name
    }
  }
`

export class Details extends React.Component {
  state = {
    loading: false,
    dateOfDeath: this.props.initialValues && this.props.initialValues.dateOfDeath
      ? moment(this.props.initialValues.dateOfDeath, 'DD-MM-YYYY')
      : null,
    dateOfBirth: this.props.initialValues && this.props.initialValues.dateOfBirth
      ? moment(this.props.initialValues.dateOfBirth, 'DD-MM-YYYY')
      : null,
  }


  onSubmitFunc = (data) => {
    this.setState({ loading: true })

    if (this.props.onSubmitFunc) {
      if (this.props.wizard) {
        this.props.onSubmitFunc(this.props.formNumber + 1)
      } else {
        this.props
          .onSubmitFunc(data)
          .then(() => {
            swal({ text: 'The changes have been saved!', icon: 'success' })
          })
          .catch(() => {
            swal({ text: 'Something went wrong!', icon: 'error' })
          })
      }
    } else {
      this.handleUpdateProfile(data)
        .then(() => {
          swal({ text: 'The changes have been saved!', icon: 'success' })
        })
        .catch(() => {
          swal({ text: 'Something went wrong!', icon: 'error' })
        })

      this.setState({ loading: false })
    }
  }
  handleValueChange = (value, fieldName) => this.setState({ [fieldName]: value })
  handleUpdateProfile = data =>
    new Promise((resolve, reject) => {
      this.props
        .mutate({
          variables: {
            contactData: {
              ...filter(doc, data),
              dateOfBirth:
                data.dateOfBirth && moment(data.dateOfBirth).format('YYYY-MM-DD'),
              dateOfDeath:
                data.dateOfDeath && moment(data.dateOfDeath).format('YYYY-MM-DD'),
              organisations: data.organisations.map(o => o.node.id),
            },
            contactId: data.id,
          },
          refetchQueries: [{ query: getMails, variables: { contactId: data.id } }],
        })
        .then((response) => {
          if (response.data.updateContact.errors.length > 0) {
            console.error(response.data.updateContact.errors)
            reject()
          } else {
            resolve()
          }
        })
    })
  handleEstimatedWealthDateChange = (value) => {
    this.setState({ estimatedWealthDate: value })

    this.props.dispatch(change('contactForm', 'estimatedWealthDate', value.format('YYYY-MM-DD')))
  }
  handleDateOfBirthChange = (value) => {
    this.setState({ dateOfBirth: value })

    this.props.dispatch(change('contactForm', 'dateOfBirth', value.format('YYYY-MM-DD')))
  }
  handleDateOfDeathChange = (value) => {
    this.setState({ dateOfDeath: value })

    this.props.dispatch(change('contactForm', 'dateOfDeath', value.format('YYYY-MM-DD')))
  }
  render() {
    return (
      <form
        className="form-horizontal form-control-line"
        onSubmit={this.props.handleSubmit(this.onSubmitFunc)}
      >
        <Field component="input" type="hidden" name="id" />
        <Field component="input" type="hidden" name="estimatedWealthDate" />
        <div className="row">
          <div className="col col-md-auto">
            <label htmlFor="salutation">Salutation</label>
            <Field
              component={renderSelect}
              name="salutation"
              id="salutation"
              className="form-control"
            >
              <option value={0}>--------</option>
              <option value={1}>Mr</option>
              <option value={2}>Mrs</option>
              <option value={3}>Ms</option>
              <option value={4}>Miss</option>
              <option value={5}>Dr</option>
            </Field>
          </div>
          <div className="col">
            <label className="col-md-12" htmlFor="firstName">
              First name (Preferred)
            </label>
            <div className="col-md-12">
              <Field id="firstName" component={renderInput} name="firstName" type="text" />
            </div>
          </div>
          <div className="col">
            <label className="col-md-12" htmlFor="middleName">
              Middle name
            </label>
            <div className="col-md-12">
              <Field id="middleName" component={renderInput} name="middleName" type="text" />
            </div>
          </div>
          <div className="col">
            <label className="col-md-12" htmlFor="lastName">
              Last name
            </label>
            <div className="col-md-12">
              <Field id="lastName" component={renderInput} name="lastName" type="text" />
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col">
            <label htmlFor="mobile">Mobile</label>
            <Field
              id="mobile"
              component={renderInput}
              normalize={normalizePhone}
              name="mobile"
              type="text"
            />
          </div>
          <div className="col">
            <label htmlFor="directLine">Direct line</label>
            <Field id="directLine" component={renderInput} name="directLine" type="text" />
          </div>
        </div>
        <div className="row">
          <div className="col">
            <label htmlFor="email">Main email</label>
            <Field id="email" component={renderInput} name="email" type="text" />
          </div>
          <div className="col">
            <label htmlFor="secondaryEmail">Secondary email</label>
            <Field id="secondaryEmail" component={renderInput} name="secondaryEmail" type="text" />
          </div>
        </div>
        <div className="row">
          <div className="col">
            <label htmlFor="occupation">Occupation</label>
            <Field
              component={renderSelect}
              name="occupation"
              id="occupation"
              className="form-control"
            >
              {this.props.data.occupations === undefined ? (
                <option>Loading...</option>
              ) : (
                <Fragment>
                  {this.props.data.occupations.map(occupation => (
                    <option key={occupation.id} value={occupation.id}>
                      {occupation.name}
                    </option>
                  ))}
                </Fragment>
              )}
            </Field>
          </div>
          <div className="col">
            <label htmlFor="skype">Skype</label>
            <Field id="skype" component={renderInput} name="skype" type="text" />
          </div>
          <div className="col">
            <label htmlFor="beverage">Preferred Beverage</label>
            <Field id="beverage" component={renderInput} name="beverage" type="text" />
          </div>
        </div>
        <div className="row">
          <div className="col">
            <label htmlFor="preferredFirstName">Full name (Legal)</label>
            <Field
              id="preferredFirstName"
              component={renderInput}
              name="preferredFirstName"
              type="text"
            />
          </div>
        </div>
        <div className="row form-group" style={{ overflow: 'visible' }}>
          <div className="col">
            <label htmlFor="dateOfBirth">Date of birth</label>
            {/* <Field component={renderInput} format={formatDate} name="dateOfBirth" /> */}
            <CustomDatePicker
              id="dateOfBirth"
              name="dateOfBirth"
              selected={this.state.dateOfBirth}
              onChange={this.handleDateOfBirthChange}
            />
          </div>
          <div className="col">
            <label htmlFor="placeOfBirth">Place Of Birth</label>
            <Field component={renderInput} name="placeOfBirth" id="placeOfBirth" />
          </div>
          <div className="col">
            <label htmlFor="dateOfDeath">Date of death</label>
            {/* <Field component={renderInput} format={formatDate} name="dateOfDeath" /> */}
            <CustomDatePicker
              id="dateOfDeath"
              name="dateOfDeath"
              selected={this.state.dateOfDeath}
              onChange={this.handleDateOfDeathChange}
            />
          </div>
        </div>
        <div className="row form-group" style={{ overflow: 'visible' }}>
          <div className="col">
            <label htmlFor="estimatedWealth">Estimated wealth</label>
            <Input
              type="text"
              name="estimatedWealth"
              id="estimatedWealth"
              normalize={normalizeCurrency}
              value={this.state.estimatedWealth === 0 ? '' : this.state.estimatedWealth}
              className="form-control"
              onChange={this.handleValueChange}
            />
          </div>
          <div className="col">
            <label htmlFor="estimatedWealthDate">Estimated wealth date</label>
            <CustomDatePicker
              selected={this.state.estimatedWealthDate}
              onChange={this.handleEstimatedWealthDateChange}
            />
          </div>
        </div>
        <div className="row form-group">
          <div className="col-auto">
            <label style={{ display: 'inline-block' }} htmlFor="isActive">
              Active status
            </label>
            <div className="switch" style={{ display: 'inline-block', height: 30 }}>
              <label>
                <Field component="input" type="checkbox" name="isActive" />
                <span className="lever switch-col-light-blue" />
              </label>
            </div>
          </div>
          <div className="col-auto">
            <label style={{ display: 'inline-block' }} htmlFor="voi">
              VOI
            </label>
            <div className="switch" style={{ display: 'inline-block', height: 30 }}>
              <label>
                <Field component="input" type="checkbox" name="voi" />
                <span className="lever switch-col-light-blue" />
              </label>
            </div>
          </div>
          {this.props.canLinkMails && <div className="col-auto">
            <label style={{ display: 'inline-block' }} htmlFor="linkMails">
              Link emails?
            </label>
            <div className="switch" style={{ display: 'inline-block', height: 30 }}>
              <label>
                <Field component="input" type="checkbox" name="linkMails" />
                <span className="lever switch-col-light-blue" />
              </label>
            </div>
          </div>}
        </div>
        <Button
          loading={this.state.loading}
          className="btn btn-success"
          type="submit"
          style={{ width: 120 }}
          title={this.props.buttonTitle}
        />
      </form>
    )
  }
}

Details.propTypes = {
  mutate: PropTypes.func.isRequired,
  handleSubmit: PropTypes.func.isRequired,
  buttonTitle: PropTypes.string,
  onSubmitFunc: PropTypes.oneOfType([PropTypes.func, PropTypes.bool]),
}

Details.defaultProps = {
  buttonTitle: 'Update profile',
  onSubmitFunc: false,
  afterSubmitFunc: () => ({}),
}

const updateContact = gql`
  mutation updateContact($contactId: ID!, $contactData: ContactInput!) {
    updateContact(contactId: $contactId, contactData: $contactData) {
      errors
      contact {
        ...Contact
      }
    }
  }
  ${contactFragment}
`

const validate = (values) => {
  const errors = {}

  if (!values.firstName) {
    errors.firstName = 'First name is required'
  }
  if (!values.lastName) {
    errors.lastName = 'Last name is required'
  }
  if (!values.email) {
    // errors.email = 'Email is required'
  } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(values.email)) {
    errors.email = 'Invalid email address'
  }
  // if (!values.mobile) {
  //   errors.mobile = 'Phone number is required'
  // }
  if (!values.salutation || values.salutation === '0') {
    errors.salutation = 'Salutation field is requried'
  }
  if (values.dateOfDeath && !/^[\d]{2}\/[\d]{2}\/[\d]{4}/i.test(values.dateOfDeath)) {
    errors.dateOfDeath = 'Invalid date'
  } else if (values.dateOfDeath) {
    if (!moment(values.dateOfDeath, 'DD/MM/YYYY').isValid()) {
      errors.dateOfDeath = 'Invalid date'
    }
  }
  if (values.dateOfBirth) {
    if (!moment(values.dateOfBirth, 'DD/MM/YYYY').isValid()) {
      errors.dateOfBirth = 'Invalid date'
    }
  }

  return errors
}

const asyncValidate = async ({ id, email, mobile }) => {
  const fetch = createApolloFetch({
    uri: `${BACKEND_URL}/graphql/`,
  })

  fetch.use(({ options }, next) => {
    if (!options.headers) {
      options.headers = {} // Create the headers object if needed.
    }
    options.headers.authorization = `Bearer ${Cookies.get('token')}`

    next()
  })

  if (email) {
    const { data } = await fetch({
      query: `
      query asyncEmailValidation($email: String!) {
        contacts(email: $email) {
          edges {
            node {
              id
            }
          }
        }
      }
      `,
      variables: { email },
    })
    if (data.contacts.edges.length) {
      if (data.contacts.edges.filter(contact => contact.node.id !== id).length) {
        throw { email: 'The email already taken!' } /* eslint no-throw-literal: 0 */
      }
    }
  }
  if (mobile) {
    const { data } = await fetch({
      query: `
      query asyncMobileValidation($mobile: String!) {
        contacts(mobile: $mobile) {
          edges {
            node {
              id
            }
          }
        }
      }
      `,
      variables: { mobile },
    })
    if (data.contacts.edges.length) {
      if (data.contacts.edges.filter(contact => contact.node.id !== id).length) {
        throw { mobile: 'The mobile already taken!' } /* eslint no-throw-literal: 0 */
      }
    }
  }
}

export default compose(
  reduxForm({
    form: 'contactForm',
    validate,
    asyncValidate,
    asyncBlurFields: ['email', 'mobile'],
    destroyOnUnmount: false,
    enableReinitialize: true,
    keepDirtyOnReinitialize: true,
  }),
  graphql(updateContact),
  graphql(getOccupations),
)(Details)
