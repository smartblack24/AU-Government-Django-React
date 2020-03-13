import React from 'react'
import { reduxForm, Field, change, reset } from 'redux-form'
import { gql, graphql, compose } from 'react-apollo'
import { connect } from 'react-redux'
import moment from 'moment'
import Router from 'next/router'
import { filter } from 'graphql-anywhere'
import { toast } from 'react-toastify'
import { createNumberMask } from 'redux-form-input-masks'

import { renderInput, renderTextarea, parseCurrency } from 'utils'
import Button from 'components/Button'
import { timeEntryFragment } from 'fragments'
import { getMatter, getStandartDisbursements } from 'queries'
import CustomDatePicker from 'components/DatePicker'
import AsyncAutocompleteField from 'utils/AsyncAutocompleteField'
import doc from './doc'

const currencyMask = createNumberMask({
  prefix: '$',
  decimalPlaces: 2,
  locale: 'en-US',
})

const getClients = gql`
  query timeEntryClients($name: String, $skip: Boolean!, $withOpenMatter: Boolean!) {
    clients(name: $name, withOpenMatter: $withOpenMatter) @skip(if: $skip) {
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

const getMatters = gql`
  query timeEntryMatters($name: String, $clientId: ID!, $leadType: Boolean,
      $activeLeads: Boolean, $skip: Boolean!) {
    matters(billableStatus: "1", name_Icontains: $name, client_Id: $clientId,
      leadType: $leadType, activeLeads: $activeLeads) @skip(if: $skip) {
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
  query timeEntryStaff($fullName: String, $skip: Boolean!, $isActive: Boolean!) {
    users(fullName: $fullName, isActive: $isActive) @skip(if: $skip) {
      edges {
        cursor
        node {
          id
          fullName
          rate
        }
      }
    }
  }
`

const createTimeEntry = gql`
  mutation createTimeEntry($timeEntryData: TimeEntryInput!, $entryType: Int!) {
    createTimeEntry(timeEntryData: $timeEntryData, entryType: $entryType) {
      errors
      timeEntry {
        ...TimeEntry
      }
    }
  }
  ${timeEntryFragment}
`

const updateTimeEntry = gql`
  mutation updateTimeEntry($timeEntryId: ID!, $timeEntryData: TimeEntryInput!) {
    updateTimeEntry(timeEntryId: $timeEntryId, timeEntryData: $timeEntryData) {
      errors
      timeEntry {
        ...TimeEntry
      }
    }
  }
  ${timeEntryFragment}
`

class TimeEntryForm extends React.Component {
  static defaultProps = {
    entryType: 1,
    editable: true,
    status: 1,
  }
  constructor(props) {
    super(props)

    this.state = {
      loading: false,
      date: moment(props.initialValues.date) || moment(),
      redirectLink: props.entryType === 1 ? '/time-entries' : '/disbursements',
      closeAfterSave: false,
      status: 1,
      time: moment().format('h:mm a'),
    }
  }
  onSubmit = (data) => {
    if (this.props.isEdit) {
      this.handleUpdateTimeEntry(data)
    } else {
      this.handleCreateTimeEntry(data)
    }
  }
  getClients = async (input, callback) => {
    const { clientsData } = this.props
    if (input.length > 2) {
      const response = await clientsData.refetch({
        skip: false,
        name: input,
      })
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
  getMatters = async (input, callback) => {
    const { form, mattersData } = this.props
    const response = await mattersData.refetch({
      skip: false,
      name: input,
      clientId: form.client.id,
      leadType: this.props.lead,
      activeLeads: this.props.lead,
    })
    if (response.data.matters.edges.length) {
      // transform to react-select format
      const options = response.data.matters.edges.map(({ node }) => ({
        value: node.id,
        label: node.name,
      }))

      // callback with fetched data
      callback(null, { options })
    }
  }
  getUsers = async (input, callback) => {
    const { staffData } = this.props
    if (input.length > 2) {
      const response = await staffData.refetch({ skip: false, fullName: input, isActive: true })
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
  getStandartDisbursements = async (input, callback) => {
    const { standartDisbursementsData } = this.props
    if (input.length > 2) {
      const response = await standartDisbursementsData.refetch({ skip: false, fullName: input })
      if (response.data.standartDisbursements.edges.length) {
        // transform to react-select format
        const options = response.data.standartDisbursements.edges.map(({ node }) => ({
          value: node.id,
          label: node.name,
        }))

        // callback with fetched data
        callback(null, { options })
      }
    }
  }
  handleUpdateTimeEntry = async (values) => {
    this.setState({ loading: true })

    const { data } = await this.props.updateTimeEntry({
      variables: {
        timeEntryId: this.props.initialValues.id,
        timeEntryData: filter(doc, {
          ...values,
          rate: parseCurrency(values.rate),
          recordType: this.props.lead ? 2 : 1,
          time: this.state.time,
        }),
      },
      refetchQueries: [{ query: getMatter, variables: { id: values.matter.id } }],
    })

    if (data.updateTimeEntry.errors.length > 0) {
      console.log(data.updateTimeEntry.errors)
    } else if (this.state.closeAfterSave) {
      if (this.props.afterCloseCallBack) {
        this.props.afterCloseCallBack()
      } else {
        Router.push(this.state.redirectLink)
      }
    }

    toast.success('The changes have been saved!')

    this.setState({ loading: false })
  }
  handleCreateTimeEntry = async (data) => {
    this.setState({ loading: true })

    const result = await this.props.createTimeEntry({
      variables: {
        entryType: this.props.entryType,
        timeEntryData: filter(doc, {
          ...data,
          rate: parseCurrency(data.rate),
          recordType: this.props.lead ? 2 : 1,
          time: this.state.time,
        }),
      },
      refetchQueries: [{ query: getMatter, variables: { id: data.matter.id } }],
    })

    if (result.data.createTimeEntry.errors.length > 0) {
      console.log(result.data.createTimeEntry.errors) // eslint-disable-line
    } else {
      this.props.dispatch(reset('timeEntryForm'))
      this.props.dispatch(change('timeEntryForm', 'date', data.date))
      if (this.state.closeAfterSave) {
        if (this.props.afterCloseCallBack) {
          this.props.afterCloseCallBack()
        } else {
          Router.push(this.state.redirectLink)
        }
      }
    }

    this.setState({ loading: false })
  }
  handleDateChange = (value) => {
    this.setState({ date: value })

    this.props.dispatch(change('timeEntryForm', 'date', value.format('YYYY-MM-DD')))
  }
  handleEndDateChange = (value) => {
    this.setState({ endDate: value })

    this.props.dispatch(change('timeEntryForm', 'endDate', value.format('YYYY-MM-DD')))
  }
  handleOnAutocompleteEdit = (fieldName) => {
    if (fieldName === 'client') {
      // if client unselected then unselect the matter
      this.props.dispatch(change('timeEntryForm', 'matter', null))
    }
    this.props.dispatch(change('timeEntryForm', fieldName, null))
  }
  handleOnClientSelect = ({ value, label }) => {
    this.props.dispatch(change('timeEntryForm', 'client', { id: value, name: label }))
  }
  handleOnMatterSelect = ({ value, label }) => {
    this.props.dispatch(change('timeEntryForm', 'matter', { id: value, name: label }))
  }
  handleOnStandartDisbursementSelect = ({ value, label }) => {
    const { standartDisbursementsData, dispatch } = this.props

    const standartDisbursement = standartDisbursementsData.standartDisbursements.edges.find(
      ({ node }) => node.id === value,
    )

    if (standartDisbursement) {
      dispatch(change('timeEntryForm', 'rate', standartDisbursement.node.cost))
      dispatch(change('timeEntryForm', 'description', standartDisbursement.node.description))
      dispatch(change('timeEntryForm', 'gstStatus', standartDisbursement.node.gstStatus))
    }
    dispatch(change('timeEntryForm', 'standartDisbursement', { id: value, name: label }))
  }
  handleOnStaffMemberSelect = ({ value, label }) => {
    const { staffData, dispatch } = this.props
    const staff = staffData.users.edges.find(({ node }) => node.id === value)
    if (staff) {
      dispatch(change('timeEntryForm', 'rate', staff.node.rate))
    }
    dispatch(change('timeEntryForm', 'staffMember', { id: value, fullName: label }))
  }
  closeAfterSave = () => this.setState({ closeAfterSave: true })
  notCloseAfterSave = () => this.setState({ closeAfterSave: false })
  render() {
    const { form, entryType, lead } = this.props
    return (
      <form className="form-control-line" onSubmit={this.props.handleSubmit(this.onSubmit)}>
        <div className="form-row p-3">
          {entryType === 2 && (
            <div className="col">
              <Field
                name="standartDisbursement.name"
                component={AsyncAutocompleteField}
                label="Disbursement list"
                fieldName="standartDisbursement"
                className="is-borderless"
                onSelect={this.handleOnStandartDisbursementSelect}
                onEdit={this.handleOnAutocompleteEdit}
                autocompleteValue={form.standartDisbursement}
                accessor="name"
                placeholder="Search for standard disbursement"
                getOptions={this.getStandartDisbursements}
              />
            </div>
          )}
          <div className="col">
            <Field
              name="client.name"
              component={AsyncAutocompleteField}
              label={lead ? 'Prospect' : 'Client'}
              editable={this.props.editable}
              fieldName="client"
              link="client"
              className="is-borderless"
              onSelect={this.handleOnClientSelect}
              onEdit={this.handleOnAutocompleteEdit}
              autocompleteValue={form.client}
              accessor="name"
              placeholder={lead ? 'Search for prospect' : 'Search for client'}
              getOptions={this.getClients}
            />
          </div>
          <div className="col">
            <Field
              name="matter.name"
              component={AsyncAutocompleteField}
              editable={this.props.editable}
              label={lead ? 'Lead' : 'Matter'}
              fieldName="matter"
              link={lead ? 'lead' : 'matter'}
              disabled={!form.client}
              className="is-borderless"
              onSelect={this.handleOnMatterSelect}
              onEdit={this.handleOnAutocompleteEdit}
              autocompleteValue={form.matter}
              accessor="name"
              placeholder={lead ? 'Search for lead' : 'Search for matter'}
              getOptions={this.getMatters}
            />
          </div>
          <div className="col">
            <Field
              name="staffMember.fullName"
              component={AsyncAutocompleteField}
              label="Staff member"
              fieldName="staffMember"
              link="profile"
              className="is-borderless"
              onSelect={this.handleOnStaffMemberSelect}
              onEdit={this.handleOnAutocompleteEdit}
              autocompleteValue={form.staffMember}
              placeholder="Search for Staff"
              accessor="fullName"
              getOptions={this.getUsers}
            />
          </div>
        </div>
        <div className="col-md-12">
          <label htmlFor="description">Description</label>
          <Field id="description" component={renderTextarea} name="description" />
        </div>
        <div className="col-md-12">
          <div className="form-row">
            <div className="col">
              <label htmlFor="date">Date</label>
              <CustomDatePicker selected={this.state.date} onChange={this.handleDateChange} />
            </div>
            <div className="col">
              <label htmlFor="units">Units</label>
              <Field
                id="units"
                component={renderInput}
                name="units"
                type="text"
                disabled={this.props.initialValues.isBilled}
                autocomplete="off"
              />
            </div>
            <div className="col">
              <label htmlFor="rate">Rate</label>
              <Field {...currencyMask} component={renderInput} name="rate" id="rate" />
            </div>
            <div className="col">
              <label htmlFor="status">Status</label>
              <Field
                id="status"
                component="select"
                className="form-control"
                name="status"
              >
                {!lead && <option value={1}>Billable</option>}
                <option value={2}>Non billable</option>
              </Field>
            </div>
            <div className="col">
              <label htmlFor="gstStatus">GST Status</label>
              <Field component="select" className="form-control" name="gstStatus" id="gstStatus">
                <option value={1}>GST (10%)</option>
                <option value={2}>GST Export (0%)</option>
                <option value={3}>BAS Excluded (0%)</option>
              </Field>
            </div>
          </div>
        </div>
        <div className="col-md-12">
          {this.props.initialValues.isBilled ? (
            <a href={`/invoice/${this.props.initialValues.invoice.id}`} target="_blank">
              Invoiced
            </a>
          ) : (
            <div>
              <Button
                title={this.props.buttonTitle}
                loading={this.state.loading}
                onClick={this.notCloseAfterSave}
                className="btn btn-success mr-3"
                type="submit"
                style={{ width: 70 }}
              />
              <Button
                title={`${this.props.buttonTitle} and close`}
                onClick={this.closeAfterSave}
                loading={this.state.loading}
                className="btn btn-warning"
                type="submit"
                style={{ width: 130 }}
              />
            </div>
          )}
        </div>
      </form>
    )
  }
}

const validate = (values) => {
  const errors = {
    client: {},
    matter: {},
    staffMember: {},
  }

  const client = values.client || {}
  const matter = values.matter || {}
  const staffMember = values.staffMember || {}

  if (!client.name) {
    errors.client.name = 'This field is requried!'
  }
  if (!matter.name) {
    errors.matter.name = 'This field is requried!'
  }
  if (!staffMember.fullName) {
    errors.staffMember.fullName = 'This field is requried!'
  }
  if (!values.date) {
    errors.date = 'This field is required!'
  }
  if (!values.description) {
    errors.description = 'This field is required!'
  }
  if (!values.units) {
    errors.units = 'This field is required!'
  } else if (isNaN(values.units)) {
    errors.units = 'Please enter a number'
  }
  if (!values.rate) {
    errors.rate = 'This field is required!'
  } else if (isNaN(parseCurrency(values.rate))) {
    errors.rate = 'Please enter a number'
  }

  return errors
}

export default compose(
  reduxForm({
    form: 'timeEntryForm',
    enableReinitialize: true,
    validate,
  }),
  graphql(createTimeEntry, { name: 'createTimeEntry' }),
  graphql(updateTimeEntry, { name: 'updateTimeEntry' }),
  graphql(getClients, { name: 'clientsData',
    options: { variables: { skip: true, withOpenMatter: true } } }),
  graphql(getMatters, { name: 'mattersData', options: { variables: { skip: true } } }),
  graphql(getUsers, { name: 'staffData', options: { variables: { skip: true } } }),
  graphql(getStandartDisbursements, {
    name: 'standartDisbursementsData',
    options: { variables: { skip: true } },
  }),
  connect(state => ({ form: state.form.timeEntryForm.values })),
)(TimeEntryForm)
