import React, { Component } from 'react'
import { connect } from 'react-redux'
import { reduxForm, Field, change } from 'redux-form'
import Router from 'next/router'
import axios from 'axios'
import { compose, gql, graphql } from 'react-apollo'
import { filter } from 'graphql-anywhere'
import { get, pick } from 'lodash'
import moment from 'moment'
import swal from 'sweetalert'
import CustomDatePicker from 'components/DatePicker'
import LocationForms from 'components/Location'
import Slider from 'components/Slider'
import Button from 'components/Button'
import { CID, CSE, CLIENT_URI } from 'constants/page'
import withData from 'lib/withData'
import { userFragment } from 'fragments'
import { getUser } from 'queries'
import { renderInput, deserializeParams, swalCreator } from 'utils'
import doc from './doc'

const salutations = [
  { id: 1, title: 'Mr' },
  { id: 2, title: 'Mrs' },
  { id: 3, title: 'Ms' },
  { id: 4, title: 'Miss' },
  { id: 5, title: 'Dr' },
  { id: 6, title: 'Mr and Mrs' },
  { id: 7, title: 'Mr and Mr' },
]

const requiredAddressFields = [
  'address1',
  'postalAddress1',
  'suburb',
  'postalSuburb',
  'postCode',
  'postalPostCode',
]

const getBase64 = file =>
  new Promise((resolve) => {
    try {
      const reader = new FileReader() // eslint-disable-line
      reader.readAsDataURL(file)
      reader.onload = function () { // eslint-disable-line
        resolve(reader.result)
      }
      reader.onerror = function (error) { // eslint-disable-line
        console.log('Error: ', error)
      }
    } catch (e) {
      resolve(null)
    } // eslint-disable-line
  })

class ProfileForm extends Component {
  constructor(props) {
    super(props)

    this.state = {
      loading: false,
      activatingGmail: false,
      deactivatingGmail: false,
      admissionDate: props.initialValues.admissionDate
        ? moment(props.initialValues.admissionDate)
        : null,
    }
  }

  componentWillMount() {
    const { router } = Router

    const params = deserializeParams(get(router, 'asPath'))

    if (params && params.code) {
      const REDIRECT_URI = `${CLIENT_URI}${router.pathname}`

      const body = {
        code: params.code,
        client_id: CID,
        client_secret: CSE,
        grant_type: 'authorization_code',
        redirect_uri: REDIRECT_URI,
      }

      const options = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        data: JSON.stringify(body),
        url: 'https://www.googleapis.com/oauth2/v4/token',
      };

      axios(options)
        .then(async (codeRes) => {
          const activationData = JSON.stringify(codeRes.data)

          this.setState({ activatingGmail: true })

          const res = await this.props.activateGmailAccount({
            variables: { activationData },
            refetchQueries: [{ query: getUser }],
          })

          const { success, errors } = res.data.activateGmailAccount

          this.setState({ activatingGmail: false })
          swalCreator({
            success,
            errors,
            successMsg: 'Gmail account is activated successfully',
            errorMsg: 'Failed to activate gmail',
          }).then(() => { Router.push('/my-profile') })
        })
        .catch((error) => {
          console.log(error);
          this.setState({ activatingGmail: false })
          Router.push('/my-profile')
        })
    }
  }

  handleAdmissionDateChange = (admissionDate) => {
    const admissionDateValue = admissionDate ? admissionDate.format('YYYY-MM-DD') : null
    this.props.dispatch(change('profileForm', 'admissionDate', admissionDateValue))
    this.setState({ admissionDate })
  }

  handleActivateGmail = () => {
    const currentURL = `${CLIENT_URI}${Router.router.route}`
    const requestURL = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${CID}&response_type=code&scope=https://www.googleapis.com/auth/gmail.readonly&redirect_uri=${currentURL}&access_type=offline&prompt=consent`

    window.location.href = requestURL
  }

  handleDeactivateGmail = async () => {
    const willDeactivate = await swal({ text: 'Deactivate gmail account?', icon: 'info', buttons: true })

    if (!willDeactivate) {
      return
    }

    this.setState({ deactivateGmailAccount: true })

    const res = await this.props.deactivateGmailAccount({ refetchQueries: [{ query: getUser }] })
    const { errors } = res.data.deactivateGmailAccount

    this.setState({ deactivateGmailAccount: false })

    swalCreator({ success: !errors.length, errors, successMsg: 'Gmail account is deactivated successfully', errorMsg: 'Failed to deactivate gmail' })
  }

  handleImageChange = () => this.props.dispatch(change('profileForm', 'image', this.file.files[0]))

  handleSubmit = (data) => {
    this.setState({ loading: true })

    if (data.image) {
      getBase64(data.image).then((image) => {
        this.updateUser({ ...data, photo: image })
      })
    } else {
      this.updateUser({ ...data, photo: null })
    }
  }

  updateUser = async (data) => {
    const location = pick(data, ['address1', 'address2', 'suburb', 'state', 'postCode', 'country'])
    const postalLocation = pick(data, ['postalAddress1', 'postalAddress2', 'postalSuburb', 'postalState', 'postalPostCode', 'postalCountry'])

    const res = await this.props
      .updateUser({
        variables: {
          userId: data.id,
          userData: filter(doc, { ...data, location, postalLocation }),
        },
        update: (store, { data: { updateUser } }) => {
          const { isStrange } = this.props
          if (isStrange) {
            const storeData = store.readQuery({ query: getUser })

            storeData.me = updateUser.user
            store.writeQuery({ query: getUser, data: storeData })
          }
        },
      })

    const { errors } = res.data.updateUser

    this.setState({ loading: false })

    swalCreator({ success: errors.length === 0, errors, successMsg: 'Profile is updated successfully', errorMsg: 'Failed to update profile' })
  }

  render() {
    const { form: { profileForm }, initialValues, anyTouched, isStrange } = this.props
    const { gmail } = initialValues
    const { admissionDate, loading, activatingGmail, deactivatingGmail } = this.state
    const salutation = salutations.find(
      salut => salut.id === parseInt(profileForm.values.salutation, 10),
    ).title

    return (
      <form
        className="form-horizontal form-control-line"
        onSubmit={this.props.handleSubmit(this.handleSubmit)}
      >
        <Field component="input" type="hidden" name="id" />
        <Field component="input" type="hidden" name="image" />
        <Field component="input" type="hidden" name="admissionDate" />
        <div className="col-md-12">
          <div className="form-row">
            <div className="col">
              <label htmlFor="salutation">Salutation</label>
              <Field component="select" id="salutation" name="salutation" className="form-control">
                {salutations.map(({ id, title }) => <option key={id} value={id}>{title}</option>)}
              </Field>
            </div>
            <div className="col">
              <label htmlFor="firstName">First name</label>
              <Field id="firstName" component={renderInput} name="firstName" type="text" />
            </div>
            <div className="col">
              <label htmlFor="lastName">Last name</label>
              <Field id="lastName" component={renderInput} name="lastName" type="text" />
            </div>
          </div>
        </div>
        <div className="col-md-12">
          <div className="form-group">
            <h4>
              <strong>Full name:</strong>{' '}
              {`${salutation}. ${profileForm.values.firstName || ''} ${profileForm.values
                .lastName || ''}`}
            </h4>
          </div>
        </div>
        <div className="row col-md-12">
          <div className="col">
            <label htmlFor="email">Email</label>
            <Field id="email" component={renderInput} name="email" type="text" />
          </div>
          <div className="col">
            <label htmlFor="secondEmail">Second email</label>
            <Field id="secondEmail" component={renderInput} name="secondEmail" type="text" />
          </div>
          <div className="col">
            <label htmlFor="mobile">Mobile</label>
            <Field id="mobile" component={renderInput} name="mobile" type="text" />
          </div>
        </div>
        <div className="row col-md-12">
          <div className="col">
            <label htmlFor="rate">Rate</label>
            <Field id="rate" component={renderInput} name="rate" type="text" />
          </div>
          <div className="col">
            <label htmlFor="admissionDate">Admission date</label>
            <CustomDatePicker
              id="admissionDate"
              isClearable
              selected={admissionDate}
              onChange={this.handleAdmissionDateChange}
            />
          </div>
          <div className="col">
            <label htmlFor="photo">Photo</label>
            <input
              id="photo"
              type="file"
              ref={ref => (this.file = ref)} // eslint-disable-line
              onChange={this.handleImageChange}
              className="form-control-file"
            />
          </div>
        </div>
        <div className="row col-md-12">
          <div className="col-md-4">
            <label htmlFor="isActive">
              Active status
            </label>
            <div className="switch">
              <label>
                <Field component="input" type="checkbox" name="isActive" />
                <span className="lever switch-col-light-blue mx-0" />
              </label>
            </div>
          </div>
          {!isStrange && <div className="col-md-8">
            <Button
              loading={activatingGmail}
              className={`btn ${gmail ? 'btn-success' : 'btn-danger'}`}
              title="Activate Gmail"
              onClick={this.handleActivateGmail}
            />
            {gmail &&
              <Button
                loading={deactivatingGmail}
                className="btn btn-danger ml-2"
                title="Deactivate Gmail"
                onClick={this.handleDeactivateGmail}
              />
            }
          </div>}
        </div>
        <div className="form-group mt-5">
          <Slider
            id="location-slider"
            title="LOCATION"
            hasError={Boolean(
              anyTouched &&
                Object.keys(profileForm.syncErrors || {}).filter(key =>
                  requiredAddressFields.includes(key),
                ).length,
            )}
          >
            <LocationForms
              formName="profileForm"
              initialValues={initialValues}
              formState={profileForm}
            />
          </Slider>
        </div>
        <div className="col-sm-12">
          <div className="form-group">
            <Button
              loading={loading}
              className="btn btn-success"
              type="submit"
              style={{ width: 120 }}
              title="Save"
            />
          </div>
        </div>
        <style jsx>{`
          .slider-trigger {
            width: 100%;
            text-align: left;
          }
        `}</style>
      </form>
    )
  }
}

const updateUser = gql`
  mutation updateUser($userId: ID!, $userData: UserInput!) {
    updateUser(userId: $userId, userData: $userData) {
      errors
      user {
        ...User
      }
    }
  }
  ${userFragment}
`

const activateGmailAccount = gql`
  mutation activateGmailAccount($activationData: String!) {
    activateGmailAccount(activationData: $activationData) {
      success
      errors
    }
  }
`

const deactivateGmailAccount = gql`
  mutation deactivateGmailAccount {
    deactivateGmailAccount {
      success
      errors
    }
  }
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
    errors.email = 'Email is required'
  } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(values.email)) {
    errors.email = 'Invalid email address'
  }
  if (values.secondEmail && !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(values.secondEmail)) {
    errors.secondEmail = 'Invalid email address'
  }
  if (!values.mobile) {
    errors.mobile = 'Phone number is required'
  }
  if (!values.rate) {
    errors.rate = 'Rate is required'
  }

  return errors
}

export default withData(
  compose(
    reduxForm({
      form: 'profileForm',
      validate,
    }),
    connect(state => ({ form: state.form })),
    graphql(updateUser, { name: 'updateUser' }),
    graphql(activateGmailAccount, { name: 'activateGmailAccount' }),
    graphql(deactivateGmailAccount, { name: 'deactivateGmailAccount' }),
  )(ProfileForm),
)
