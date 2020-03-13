import React from 'react'
import { reduxForm, Field, change } from 'redux-form'
import moment from 'moment'
import { graphql, gql, compose } from 'react-apollo'
import { connect } from 'react-redux'
import { filter } from 'graphql-anywhere'
import { renderTextarea, formatCurrency, renderSelect, swalCreator } from 'utils'
import CustomDatePicker from 'components/DatePicker'
import Button from 'components/Button'
import { getInvoiceStatuses } from 'queries'
import { invoiceFragment } from 'fragments'
import { BACKEND_URL } from 'constants/page'
import AsyncAutocompleteField from 'utils/AsyncAutocompleteField'
import { invoiceInfoDoc } from './doc'

const getClients = gql`
  query invoiceClients($name: String, $skip: Boolean!) {
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
  query invoiceStaff($fullName: String, $skip: Boolean!) {
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

const getMatters = gql`
  query invoiceMatters($name: String, $clientName: String, $skip: Boolean!) {
    matters(name_Icontains: $name, clientName: $clientName) @skip(if: $skip) {
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

class Info extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      loading: false,
      createdDate: moment(props.initialValues.createdDate),
    }
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
  getMatters = async (input, callback) => {
    const {
      mattersData,
      form: { client },
    } = this.props
    if (input.length > 2) {
      const response = await mattersData.refetch({
        skip: false,
        name: input,
        clientName: client.name,
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
  }
  handleUpdateInfo = async (values) => {
    this.setState({ loading: true })

    const res = await this.props.mutate({
      variables: {
        invoiceId: this.props.initialValues.id,
        invoiceData: filter(invoiceInfoDoc, values),
      },
    })


    this.setState({ loading: false })

    const { errors } = res.data.updateInvoiceInfo
    swalCreator({ success: errors.length === 0, errors, successMsg: 'Invoice has updated successfully' })
  }
  handleOnClientSelect = ({ value, label }) => {
    this.props.dispatch(change('invoiceInfo', 'matter.client', { id: value, name: label }))
    this.props.dispatch(change('invoiceInfo', 'matter.name', null))
  }
  handleOnManagerSelect = ({ value, label }) => {
    this.props.dispatch(change('invoiceInfo', 'matter.manager', { id: value, fullName: label }))
  }
  handleOnMatterSelect = ({ value, label }) => {
    this.props.dispatch(change('invoiceInfo', 'matter.name', { id: value, name: label }))
  }
  handleCreatedDateChange = (value) => {
    this.setState({ createdDate: value })

    this.props.dispatch(change('invoiceInfo', 'createdDate', value.format('YYYY-MM-DD')))
  }
  handleOnAutocompleteEdit = (fieldName) => {
    this.props.dispatch(change('invoiceInfo', fieldName, null))
  }
  render() {
    const { form } = this.props
    const { isInXero } = this.props.initialValues
    const { canUseXero } = this.props.user

    return (
      <form className="form-control-line" onSubmit={this.props.handleSubmit(this.handleUpdateInfo)}>
        <div className="form-row form-group" style={{ overflow: 'visible' }}>
          <div className="col-xs-1">
            <label htmlFor="client">Invoice number</label>
            <input
              style={{ backgroundColor: 'white' }}
              name="id"
              type="number"
              className="form-control"
              value={this.props.initialValues.number}
              disabled
            />
          </div>
          <div className="col">
            <Field
              name="matter.client.name"
              component={AsyncAutocompleteField}
              label="Client"
              fieldName="client"
              link="client"
              editable={false}
              className="is-borderless"
              onSelect={this.handleOnClientSelect}
              onEdit={this.handleOnAutocompleteEdit}
              autocompleteValue={form.matter.client}
              accessor="name"
              placeholder="Search for client"
              getOptions={this.getClients}
            />
          </div>
          <div className="col">
            <Field
              name="matter.name"
              component={AsyncAutocompleteField}
              label="Matter"
              fieldName="matter"
              link="matter"
              editable={false}
              className="is-borderless"
              onSelect={this.handleOnMatterSelect}
              onEdit={this.handleOnAutocompleteEdit}
              autocompleteValue={form.matter}
              accessor="name"
              placeholder="Search for matter"
              getOptions={this.getMatters}
            />
          </div>
          <div className="col">
            <Field
              name="matter.manager.fullName"
              component={AsyncAutocompleteField}
              label="Manager"
              fieldName="manager"
              link="profile"
              className="is-borderless"
              onSelect={this.handleOnManagerSelect}
              onEdit={this.handleOnAutocompleteEdit}
              autocompleteValue={form.matter.manager}
              accessor="fullName"
              placeholder="Search for staff member"
              getOptions={this.getUsers}
            />
          </div>
        </div>
        <div className="form-row form-group">
          <div className="col">
            <label htmlFor="description">Description</label>
            <Field component={renderTextarea} name="matter.description" id="description" />
          </div>
        </div>
        <div className="form-row" style={{ overflow: 'visible' }}>
          <div className="col">
            <label htmlFor="qwe">Date created</label>
            <CustomDatePicker selected={this.state.createdDate} onChange={this.handleCreatedDateChange} />
          </div>
          <div className="col">
            <label htmlFor="dueDate">Due date</label>
            <input
              className="form-control"
              readOnly
              value={moment(this.props.initialValues.dueDate).format('DD/MM/YYYY')}
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
          <div className="col">
            <label htmlFor="status">Invoice status</label>
            {isInXero && <div className="text-primary pt-2">In Xero</div>}
            {!isInXero && (
              <Field component={renderSelect} name="status.id" id="status" className="form-control">
                {this.props.invoiceStatuses.loading ? (
                  <option>Loading...</option>
                ) : (
                  this.props.invoiceStatuses.invoiceStatuses.filter(status => status.name !== 'In Xero').map(status => (
                    <option key={status.id} value={status.id}>
                      {status.name}
                    </option>
                  ))
                )}
              </Field>)}
          </div>
        </div>
        <div className="row">
          <div className="col" />
          <div className="col">
            <div className="btn-group" role="group">
              {this.props.initialValues.friendlyReminder && (
                <a
                  href={`${BACKEND_URL}/pdf/reminder/${this.props.initialValues.id}/friendly/user/${
                    this.props.user.id
                  }`}
                  target="_blank"
                  className="btn btn-secondary btn-sm"
                >
                  FR
                </a>
              )}
              {this.props.initialValues.firstReminder && (
                <a
                  href={`${BACKEND_URL}/pdf/reminder/${this.props.initialValues.id}/first/user/${
                    this.props.user.id
                  }`}
                  target="_blank"
                  className="btn btn-secondary btn-sm"
                >
                  1st
                </a>
              )}
              {this.props.initialValues.secondReminder && (
                <a
                  href={`${BACKEND_URL}/pdf/reminder/${this.props.initialValues.id}/second/user/${
                    this.props.user.id
                  }`}
                  target="_blank"
                  className="btn btn-secondary btn-sm"
                >
                  2nd
                </a>
              )}
            </div>
          </div>
          <div className="col" />
          <div className="col" />
        </div>
        <div className="mt-3 form-group d-flex flex-column">
          <div className="col-lg-4 col-xl-3 p-0 d-flex justify-content-between">
            <strong>Invoice (Inc GST):</strong>
            {formatCurrency(this.props.initialValues.valueInclGst)}
          </div>
          <div className="col-lg-4 col-xl-3 p-0 d-flex justify-content-between">
            <strong>Payments (Inc GST):</strong>
            {formatCurrency(this.props.initialValues.receivedPayments)}
          </div>
          <div className="col-lg-4 col-xl-3 p-0 d-flex justify-content-between">
            <strong>Net Outstanding:</strong>
            {formatCurrency(this.props.initialValues.netOutstanding)}
          </div>
        </div>
        {(!isInXero || canUseXero) &&
          <Button
            title="Update"
            loading={this.state.loading}
            className="btn btn-success"
            type="submit"
            style={{ width: 80 }}
          />
        }
      </form>
    )
  }
}

const updateInfo = gql`
  mutation updateInfo($invoiceId: ID!, $invoiceData: InvoiceInfoInput) {
    updateInvoiceInfo(invoiceId: $invoiceId, invoiceData: $invoiceData) {
      errors
      invoice {
        ...Invoice
      }
    }
  }
  ${invoiceFragment}
`

const validate = (values) => {
  const errors = {
    client: {},
    matter: {},
    manager: {},
    status: {},
  }

  const client = values.client || {}
  const matter = values.matter || {}
  const manager = values.manager || {}

  if (!values.description) {
    errors.description = 'This field is required!'
  }
  if (!client.name) {
    errors.client.name = 'This field is required!'
  }
  if (!matter.name) {
    errors.matter.name = 'This field is required!'
  }
  if (!manager.fullName) {
    errors.manager.fullName = 'This field is required!'
  }

  return errors
}

export default reduxForm({ form: 'invoiceInfo', validate })(
  compose(
    connect(state => ({ form: state.form.invoiceInfo.values })),
    graphql(updateInfo),
    graphql(getInvoiceStatuses, { name: 'invoiceStatuses' }),
    graphql(getClients, { name: 'clientsData', options: { variables: { skip: true } } }),
    graphql(getMatters, { name: 'mattersData', options: { variables: { skip: true } } }),
    graphql(getUsers, { name: 'staffData', options: { variables: { skip: true } } }),
  )(Info),
)
