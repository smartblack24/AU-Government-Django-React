import React, { Fragment } from 'react'
import { gql, graphql, compose } from 'react-apollo'
import { reduxForm, Field, change } from 'redux-form'
import { connect } from 'react-redux'
import moment from 'moment'
import { filter } from 'graphql-anywhere'
import { toast } from 'react-toastify'
import { createNumberMask } from 'redux-form-input-masks'
import Router from 'next/router'

import { getMatterTypes, getNewMatterReports } from 'queries'
import CustomDatePicker from 'components/DatePicker'
import { matterFragment } from 'fragments'
import {
  renderInput,
  renderTextarea,
  parseCurrency,
  renderSelect,
  formatCurrency,
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
        leadStatus
        leadDate
      }
    }
  }
  ${matterFragment}
`

const lostMatter = gql`
  mutation lostMatter($matterId: ID!) {
    lostMatter(matterId: $matterId) {
      errors
    }
  }
`

const winMatter = gql`
  mutation winMatter($matterId: ID!) {
    winMatter(matterId: $matterId) {
      errors
    }
  }
`

class Details extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      loading: false,
      leadDate: props.initialValues.leadDate ? moment(props.initialValues.leadDate) : null,
      closedDate: props.initialValues.closedDate ? moment(props.initialValues.closedDate) : null,
      errors: [],
    }
  }
  onSubmit = (data) => {
    this.setState({ loading: true })

    if (this.props.onSubmit) {
      this.props.onSubmit(data).then(() => toast.success('The changes have been saved!'))
    } else {
      console.log(data);
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
              leadDate: data.leadDate,
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
  lostLead = () => {
    this.props.lostMatter({
      variables: { matterId: this.props.form.id } })
      .then((response) => {
        if (response.data.lostMatter.errors > 0) {
          console.log(response.data.lostMatter.errors)
        } else {
          Router.push('/leads', '/leads')
        }
      })
  }
  wonLead = () => {
    this.props.winMatter({ variables: { matterId: this.props.form.id } })
      .then((response) => {
        if (response.data.winMatter.errors > 0) {
          console.log(response.data.winMatter.errors)
        } else {
          Router.push(`/matter?id=${this.props.form.id}`, `/matter/${this.props.form.id}`, { shallow: true })
        }
      })
  }
  handleOnAutocompleteEdit = (fieldName) => {
    this.props.dispatch(change('leadForm', fieldName, null))
  }
  handleOnClientSelect = ({ value, label }) => {
    this.props.dispatch(change('leadForm', 'client', { id: value, name: label }))
  }
  handleOnPrincipalSelect = ({ value, label }) => {
    this.props.dispatch(change('leadForm', 'principal', { id: value, fullName: label }))
  }
  handleOnManagerSelect = ({ value, label }) => {
    this.props.dispatch(change('leadForm', 'manager', { id: value, fullName: label }))
  }
  handleOnAssistantSelect = ({ value, label }) => {
    this.props.dispatch(change('leadForm', 'assistant', { id: value, fullName: label }))
  }
  handleLeadDateChange = (leadDate) => {
    this.props.dispatch(change('leadForm', 'leadDate', leadDate.format('YYYY-MM-DD')))
    this.setState({ leadDate })
  }
  handleClosedDateChange = (closedDate) => {
    this.props.dispatch(change('leadForm', 'closedDate', closedDate.format('YYYY-MM-DD')))
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
              label="Prospect"
              fieldName="client"
              link="client"
              className="is-borderless"
              onSelect={this.handleOnClientSelect}
              onEdit={this.handleOnAutocompleteEdit}
              autocompleteValue={form.client}
              accessor="name"
              placeholder="Search for Prospect"
              getOptions={this.getClients}
            />
          </div>
          <div className="col">
            <label htmlFor="name">Lead</label>
            <Field id="name" component={renderInput} name="name" type="text" />
          </div>
        </div>
        <label className="col-md-12" htmlFor="description">
          Lead description
        </label>
        <div className="col-md-12">
          <Field id="description" component={renderTextarea} name="description" />
        </div>
        <div className="row col-12 form-group">
          <div className="col">
            <label htmlFor="matterType">Lead type</label>
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
            <label htmlFor="matterSubType">Lead sub type</label>
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
            <label htmlFor="budget">Estimate</label>
            <Field
              {...currencyMask}
              component={renderInput}
              id="budget"
              name="budget"
              type="text"
            />
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
        <div className="row col-12 form-group" style={{ overflow: 'visible' }}>
          <div className="col">
            <label htmlFor="leadDate">Lead created</label>
            <CustomDatePicker
              id="leadDate"
              selected={this.state.leadDate}
              onChange={this.handleLeadDateChange}
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
        </div>
        <div className="row col-12 form-group">
          <div className="col">
            <label htmlFor="leadStatus">Lead status</label>
            <Field
              component={renderSelect}
              name="leadStatus"
              id="leadStatus"
              className="form-control"
            >
              <option value={0}>----------------</option>
              <option value={1}>To be contacted</option>
              <option value={2}>Nurturing</option>
              <option value={3}>Quoting</option>
              <option value={4}>Waiting for response</option>
              {this.props.initialValues.leadStatus === 5 && <option value={5}>Lost</option>}
            </Field>
          </div>
          {!this.props.wizard && this.props.initialValues.leadStatus !== 5 && (
            <div className="col" style={{ marginTop: 20 }}>
              <Button
                className="btn btn-success"
                title="Won"
                style={{ width: 120, fontSize: 22, marginRight: 15 }}
                onClick={this.wonLead}
              />
              <Button
                className="btn btn-danger"
                title="Lost"
                style={{ width: 120, fontSize: 20 }}
                onClick={this.lostLead}
              />
            </div>
          )}
        </div>
        {!this.props.wizard && (
          <div className="row col-12 form-group">
            <div className="col">
              <span>
                Total time value:{' '}
                <strong>{formatCurrency(this.props.initialValues.totalTimeValue)}</strong>
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

const validate = (values) => {
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


  if (!values.name) {
    errors.name = 'This field is required!'
  }
  if (!matterType.id) {
    errors.matterType.id = 'This field is required!'
  }
  if (!values.description) {
    errors.description = 'This field is required!'
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
  if (values.leadStatus === '0') {
    errors.leadStatus = 'This field is required!'
  }
  return errors
}

export default compose(
  reduxForm({
    form: 'leadForm',
    validate,
  }),
  connect(state => ({ form: state.form.leadForm.values })),
  graphql(updateMatter),
  graphql(lostMatter, { name: 'lostMatter' }),
  graphql(winMatter, { name: 'winMatter' }),
  graphql(getMatterTypes, { name: 'matterTypesData' }),
  graphql(getUsers, { name: 'staffData', options: { variables: { skip: true } } }),
  graphql(getClients, { name: 'clientsData', options: { variables: { skip: true } } }),
)(Details)
