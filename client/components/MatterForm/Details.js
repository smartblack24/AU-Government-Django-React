import React, { Fragment } from 'react'
import { gql, graphql, compose } from 'react-apollo'
import { reduxForm, Field, change } from 'redux-form'
import { connect } from 'react-redux'
import moment from 'moment'
import { filter } from 'graphql-anywhere'
import { toast } from 'react-toastify'
import { createNumberMask } from 'redux-form-input-masks'

import { getMatterTypes, getNewMatterReports } from 'queries'
import CustomDatePicker from 'components/DatePicker'
import { matterFragment } from 'fragments'
import {
  renderInput,
  renderTextarea,
  formatCurrency,
  parseCurrency,
  renderSelect,
  formatDate,
} from 'utils'
import Button from 'components/Button'
import AsyncAutocompleteField from 'utils/AsyncAutocompleteField'
import doc from './doc'

const currencyMask = createNumberMask({
  prefix: '$',
  decimalPlaces: 2,
  locale: 'en-US',
})

const getClients = gql`
  query matterClients($name: String, $skip: Boolean!) {
    clients(name: $name) @skip(if: $skip) {
      edges {
        cursor
        node {
          id
          name
        }
      }
    }
  }
`

const getUsers = gql`
  query matterStaff($fullName: String, $skip: Boolean!) {
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

const updateMatter = gql`
  mutation updateMatter($matterId: ID!, $matterData: MatterInput!) {
    updateMatter(matterId: $matterId, matterData: $matterData) {
      errors
      matter {
        ...Matter
      }
    }
  }
  ${matterFragment}
`

class Details extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      loading: false,
      createdDate: moment(props.initialValues.createdDate),
      closedDate: props.initialValues.closedDate ? moment(props.initialValues.closedDate) : null,
      errors: [],
    }
  }
  onSubmit = (data) => {
    this.setState({ loading: true })

    if (this.props.onSubmit) {
      this.props.onSubmit(data).then(() => toast.success('The changes have been saved!'))
    } else {
      this.updateMatter(data).then(() => toast.success('The changes have been saved!'))
    }

    this.setState({ loading: false })
  }
  getClients = async (input, callback) => {
    const { clientsData } = this.props
    if (input.length > 2) {
      const response = await clientsData.refetch({ skip: false, name: input })
      if (response.data.clients.edges.length) {
        // transform to react-select format
        const options = response.data.clients.edges.map(({ node }) => ({
          value: node.id,
          label: node.name,
        }))

        // callback with fetched data
        callback(null, { options })
      }
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
  updateMatter = data =>
    new Promise((resolve, reject) => {
      this.props
        .mutate({
          variables: {
            matterData: filter(doc, {
              ...data,
              budget: parseCurrency(data.budget) ? parseCurrency(data.budget) : 0,
            }),
            matterId: data.id,
          },
          refetchQueries: [{ query: getNewMatterReports }],
        })
        .then((response) => {
          if (response.data.updateMatter.errors.length > 0) {
            this.setState({ errors: response.data.updateMatter.errors })
            reject()
          } else {
            resolve()
          }
        })
    })
  handleBillableStatusChange = (event) => {
    const value = parseInt(event.target.value, 10)

    if (value === 1) {
      this.setState({ closedDate: null })
      this.props.dispatch(change('matterForm', 'closedDate', null))
    } else {
      this.setState({ closedDate: moment() })
    }
  }
  handleCheckBoxChange = (checkboxName, fieldName) => (event) => {
    if (event.target.checked) {
      this.props.dispatch(change('matterForm', fieldName, moment().format('DD/MM/YYYY')))
    } else {
      this.props.dispatch(change('matterForm', fieldName, null))
    }
    this.props.dispatch(change('matterForm', checkboxName, event.target.checked))
  }
  handleOnAutocompleteEdit = (fieldName) => {
    this.props.dispatch(change('matterForm', fieldName, null))
  }
  handleOnClientSelect = ({ value, label }) => {
    this.props.dispatch(change('matterForm', 'client', { id: value, name: label }))
  }
  handleOnPrincipalSelect = ({ value, label }) => {
    this.props.dispatch(change('matterForm', 'principal', { id: value, fullName: label }))
  }
  handleOnManagerSelect = ({ value, label }) => {
    this.props.dispatch(change('matterForm', 'manager', { id: value, fullName: label }))
  }
  handleOnAssistantSelect = ({ value, label }) => {
    this.props.dispatch(change('matterForm', 'assistant', { id: value, fullName: label }))
  }
  handleCreatedDateChange = (createdDate) => {
    this.props.dispatch(change('matterForm', 'createdDate', createdDate.format('YYYY-MM-DD')))
    this.setState({ createdDate })
  }
  handleClosedDateChange = (closedDate) => {
    this.props.dispatch(change('matterForm', 'closedDate', closedDate.format('YYYY-MM-DD')))
    this.setState({ closedDate })
  }
  render() {
    const { form, matterTypesData } = this.props
    let matterType = null

    if (!matterTypesData.loading && form.matterType) {
      matterType = matterTypesData.matterTypes.find(m => m.id === form.matterType.id)
    }
    return (
      <form
        className="form-horizontal form-control-line"
        onSubmit={this.props.handleSubmit(this.onSubmit)}
      >
        <Field component="input" type="hidden" name="createdDate" />
        <Field component="input" type="hidden" name="closedDate" />
        <div className="row col-12">
          <div className="col">
            <Field
              name="client.name"
              component={AsyncAutocompleteField}
              label="Client"
              fieldName="client"
              link="client"
              className="is-borderless"
              onSelect={this.handleOnClientSelect}
              onEdit={this.handleOnAutocompleteEdit}
              autocompleteValue={form.client}
              accessor="name"
              placeholder="Search for client"
              getOptions={this.getClients}
            />
          </div>
          <div className="col">
            <label htmlFor="name">Matter name</label>
            <Field id="name" component={renderInput} name="name" type="text" />
          </div>
          <div className="col">
            <label htmlFor="id">Matter ID</label>
            <div className="m-t-10 text-themecolor"><strong>{form.matterId}</strong></div>
          </div>
        </div>
        <label className="col-md-12" htmlFor="description">
          Matter description
        </label>
        <div className="col-md-12">
          <Field id="description" component={renderTextarea} name="description" />
        </div>
        <div className="row col-12 form-group">
          <div className="col">
            <label htmlFor="matterType">Matter type</label>
            <Field
              component={renderSelect}
              name="matterType.id"
              id="matterType"
              className="form-control"
            >
              {matterTypesData.loading ? (
                <option>Loading...</option>
              ) : (
                <Fragment>
                  <option value={null}>--------</option>
                  {matterTypesData.matterTypes.map(m => (
                    <option key={m.id} value={m.id}>
                      {m.name}
                    </option>
                  ))}
                </Fragment>
              )}
            </Field>
          </div>
          <div className="col">
            <label htmlFor="matterSubType">Matter sub type</label>
            <Field
              component="select"
              name="matterSubType.id"
              id="matterSubType"
              className="form-control"
            >
              {matterTypesData.loading ? (
                <option>Loading...</option>
              ) : (
                matterType &&
                matterType.subtypes.map(subType => (
                  <option key={subType.id} value={subType.id}>
                    {subType.name}
                  </option>
                ))
              )}
            </Field>
          </div>
          <div className="col">
            <label htmlFor="budget">Budget (ex GST)</label>
            <Field
              {...currencyMask}
              component={renderInput}
              id="budget"
              name="budget"
              type="text"
            />
          </div>
          <div className="col">
            <label htmlFor="billingMethod">Billing method</label>
            <Field
              component="select"
              name="billingMethod"
              id="billingMethod"
              className="form-control"
            >
              <option value={1}>Fixed price</option>
              <option value={2}>Time entry</option>
            </Field>
          </div>
        </div>
        <div className="row col-12 form-group" style={{ overflow: 'visible' }}>
          <div className="col">
            <Field
              name="principal.fullName"
              component={AsyncAutocompleteField}
              label="Principal"
              fieldName="principal"
              link="profile"
              className="is-borderless"
              onSelect={this.handleOnPrincipalSelect}
              onEdit={this.handleOnAutocompleteEdit}
              autocompleteValue={form.principal}
              accessor="fullName"
              placeholder="Search for staff member"
              getOptions={this.getUsers}
            />
          </div>
          <div className="col">
            <Field
              name="manager.fullName"
              component={AsyncAutocompleteField}
              label="Manager"
              fieldName="manager"
              link="profile"
              className="is-borderless"
              onSelect={this.handleOnManagerSelect}
              onEdit={this.handleOnAutocompleteEdit}
              autocompleteValue={form.manager}
              accessor="fullName"
              placeholder="Search for staff member"
              getOptions={this.getUsers}
            />
          </div>
          <div className="col">
            <Field
              name="assistant.fullName"
              component={AsyncAutocompleteField}
              label="Assistant"
              fieldName="assistant"
              link="profile"
              className="is-borderless"
              onSelect={this.handleOnAssistantSelect}
              onEdit={this.handleOnAutocompleteEdit}
              autocompleteValue={form.assistant}
              accessor="fullName"
              placeholder="Search for staff member"
              getOptions={this.getUsers}
            />
          </div>
        </div>
        <div className="form-group">
          <label className="col-md-12" htmlFor="conflictStatus">
            Conflict status
          </label>
          <div className="col-md-12">
            <Field
              component="select"
              name="conflictStatus"
              id="conflictStatus"
              className="form-control"
            >
              <option value={1}>Outstanding</option>
              <option value={2}>No other parties</option>
              <option value={3}>Complete</option>
            </Field>
          </div>
        </div>
        <label className="col-md-12" htmlFor="conflictParties">
          Conflict parties
        </label>
        <div className="col-md-12">
          <div className="form-group">
            <Field
              id="conflictParties"
              component="textarea"
              className="form-control"
              name="conflictParties"
              type="text"
            />
          </div>
        </div>
        <label className="col-md-12" htmlFor="filePath">
          Client Folder Name
        </label>
        <div className="col-md-12">
          <div className="form-group">
            <Field
              id="filePath"
              component={renderInput}
              className="form-control"
              name="filePath"
              type="text"
            />
          </div>
        </div>
        <div className="row col-12 form-group" style={{ overflow: 'visible' }}>
          <div className="col">
            <label htmlFor="createdDate">Date created</label>
            <CustomDatePicker
              id="createdDate"
              selected={this.state.createdDate}
              onChange={this.handleCreatedDateChange}
            />
          </div>
          <div className="col">
            <label htmlFor="closedDate">Date closed</label>
            <CustomDatePicker
              id="closedDate"
              selected={this.state.closedDate}
              onChange={this.handleClosedDateChange}
            />
          </div>
          <div className="col">
            <label htmlFor="billableStatus">Billable status</label>
            <Field
              component={renderSelect}
              name="billableStatus"
              id="billableStatus"
              className="form-control"
              onChange={this.handleBillableStatusChange}
            >
              <option value={1}>Open</option>
              <option value={2}>Suspended</option>
              <option value={3}>Closed</option>
            </Field>
          </div>
        </div>
        <div className="row col-12 form-group">
          <div className="col">
            <label htmlFor="matterStatus">Matter status</label>
            <Field
              component={renderSelect}
              name="matterStatus"
              id="matterStatus"
              className="form-control"
            >
              <option value={0}>----------------</option>
              <option value={1}>Active - High (70+ units)</option>
              <option value={2}>Active - Moderate (30-70 units)</option>
              <option value={3}>Active - Low (0-30 units)</option>
              <option value={4}>Waiting for Internal review</option>
              <option value={5}>Waiting for AA review</option>
              <option value={6}>Waiting for external party to respond</option>
              <option value={7}>Ad hoc Work</option>
              <option value={8}>Need to be billed</option>
              <option value={9}>Matter Closed</option>
              <option value={10}>Business Building</option>
            </Field>
          </div>
          <div className="col">
            <label>Funds in Trust for Invoices?</label>
            <div className="switch" style={{ height: 30 }}>
              <label>
                <Field
                  component="input"
                  type="checkbox"
                  name="fundsInTrust"
                  onChange={this.handleCheckBoxChange('fundsInTrust')}
                />
                <span className="lever switch-col-light-blue" />
              </label>
            </div>
          </div>
        </div>
        <div className="row form-group">
          <div className="col">
            <label htmlFor="conflictCheckSent">Conflict Check Sent</label>
            <Field
              format={formatDate}
              component="input"
              name="conflictCheckSent"
              type="text"
              id="conflictCheckSent"
              className="form-control"
            />
          </div>
          <div className="col-auto" style={{ marginTop: 30 }}>
            <div className="switch">
              <label>
                <Field
                  component="input"
                  type="checkbox"
                  onChange={this.handleCheckBoxChange('isConflictCheckSent', 'conflictCheckSent')}
                  name="isConflictCheckSent"
                />
                <span className="lever switch-col-light-blue" />
              </label>
            </div>
          </div>
          <div className="col">
            <label htmlFor="standardTermsSent">Standard Terms Sent</label>
            <Field
              format={formatDate}
              component={renderInput}
              name="standardTermsSent"
              type="text"
              id="standardTermsSent"
              className="form-control"
            />
          </div>
          <div className="col-auto" style={{ marginTop: 30 }}>
            <div className="switch">
              <label>
                <Field
                  component="input"
                  type="checkbox"
                  name="isStandardTermsSent"
                  onChange={this.handleCheckBoxChange('isStandardTermsSent', 'standardTermsSent')}
                />
                <span className="lever switch-col-light-blue" />
              </label>
            </div>
          </div>
          <div className="col">
            <label htmlFor="referrerThanked">Referrer Thanked</label>
            <Field
              format={formatDate}
              component="input"
              name="referrerThanked"
              type="text"
              id="referrerThanked"
              className="form-control"
            />
          </div>
          <div className="col-auto" style={{ marginTop: 30 }}>
            <div className="switch">
              <label>
                <Field
                  component="input"
                  type="checkbox"
                  name="isReferrerThanked"
                  onChange={this.handleCheckBoxChange('isReferrerThanked', 'referrerThanked')}
                />
                <span className="lever switch-col-light-blue" />
              </label>
            </div>
          </div>
        </div>
        {!this.props.wizard && (
          <div className="row col-12 form-group">
            <div className="col">
              <span>
                Total time value:{' '}
                <strong>{formatCurrency(this.props.initialValues.totalTimeValue)}</strong>
              </span>
            </div>
            <div className="col">
              <span>
                Total time invoiced:{' '}
                <strong>{formatCurrency(this.props.initialValues.totalTimeInvoiced)}</strong>
              </span>
            </div>
            <div className="col-auto">
              <span>
                WIP: <strong>{formatCurrency(this.props.initialValues.wip)}</strong>
              </span>
            </div>
            <div className="col">
              <span>
                Total Invoice Value (ex GST):{' '}
                <strong>{formatCurrency(this.props.initialValues.totalInvoicedValue)}</strong>
              </span>
            </div>
            <div className="col">
              <span>
                Amount outstanding:{' '}
                <strong>{formatCurrency(this.props.initialValues.amountOutstanding)}</strong>
              </span>
            </div>
          </div>
        )}
        <div className="form-group">
          {this.state.errors.map(error => (
            <span key={error} className="text-danger">
              {error}
            </span>
          ))}
        </div>
        <Button
          title={this.props.buttonTitle}
          loading={this.state.loading}
          className="btn btn-success"
          type="submit"
          style={{ width: 120 }}
        />
      </form>
    )
  }
}

const validate = (values, { initialValues: { wip } }) => {
  const errors = {
    client: {},
    principal: {},
    manager: {},
    assistant: {},
    matterType: {},
  }

  const client = values.client || {}
  const principal = values.principal || {}
  const manager = values.manager || {}
  const assistant = values.assistant || {}
  const matterType = values.matterType || {}

  if (!values.isStandardTermsSent) {
    errors.standardTermsSent = 'Please, confirm Standard Terms Sent!'
  }
  if (!values.name) {
    errors.name = 'This field is required!'
  }
  if (!matterType.id) {
    errors.matterType.id = 'This field is required!'
  }
  if (!values.description) {
    errors.description = 'This field is required!'
  }
  if (values.billingMethod === '1' && !values.budget) {
    errors.budget = 'This field is required!'
  } else if (values.billingMethod === '1' && isNaN(parseCurrency(values.budget))) {
    errors.budget = 'Please enter a number'
  }
  if (!client.name) {
    errors.client.name = 'This field is required!'
  }
  if (!principal.fullName) {
    errors.principal.fullName = 'This field is required!'
  } else if (principal.id === manager.id) {
    errors.principal.fullName = 'Staff member can not be principal and manager simultaneously'
  } else if (principal.id === assistant.id) {
    errors.principal.fullName = 'Staff member can not be principal and assistant simultaneously'
  }
  if (!manager.fullName) {
    errors.manager.fullName = 'This field is required!'
  } else if (manager.id === assistant.id) {
    errors.manager.fullName = 'Staff member can not be manager and assistant simultaneously'
  }
  if (values.billableStatus === '3' && parseFloat(wip) > 0) {
    errors.billableStatus = 'The Matter cannot be closed because of unbilled wip!'
  }
  if (!values.matterStatus || values.matterStatus === '0') {
    errors.matterStatus = 'This field is required!'
  }
  if (values.filePath && values.filePath.length > 250) {
    errors.filePath = 'Folder path is too long!'
  }

  return errors
}

export default compose(
  reduxForm({
    form: 'matterForm',
    validate,
  }),
  connect(state => ({ form: state.form.matterForm.values })),
  graphql(updateMatter),
  graphql(getMatterTypes, { name: 'matterTypesData' }),
  graphql(getUsers, { name: 'staffData', options: { variables: { skip: true } } }),
  graphql(getClients, { name: 'clientsData', options: { variables: { skip: true } } }),
)(Details)
