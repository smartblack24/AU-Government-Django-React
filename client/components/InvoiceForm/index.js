import React from 'react'
import { reduxForm, Field, change } from 'redux-form'
import { graphql, compose } from 'react-apollo'
import gql from 'graphql-tag'
import Router from 'next/router'
import { connect } from 'react-redux'
import { filter } from 'graphql-anywhere'
import { createNumberMask } from 'redux-form-input-masks'

import { renderInput, renderTextarea, Tab } from 'utils'
import { getMatter } from 'queries'
import Button from 'components/Button'
import { invoiceFragment } from 'fragments'
import { getInvoices } from 'pages/invoices'
import UnbilledTime from './UnbilledTime'
import FixedPriceItemList from './FixedPriceItemList'
import FixedPriceItemForm from './FixedPriceItemForm'
import doc from './doc'

class InvoiceForm extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      modal: false,
      form: 1,
      selectedTimes: [],
      loading: false,
      unbilledTime: props.initialValues.matter.unbilledTime,
    }
  }
  toggleTimeEntry = key =>
    this.setState((state) => {
      if (state.selectedTimes.map(time => time.id).includes(key)) {
        const selectedTimes = state.selectedTimes.filter(time => time.id !== key)
        return { selectedTimes }
      }

      const timeEntry = state.unbilledTime.find(time => time.id === key)
      return {
        selectedTimes: state.selectedTimes.concat({
          id: timeEntry.id,
          unitsToBill: timeEntry.unitsToBill,
        }),
      }
    })
  toggleSelectAll = () => {
    this.setState((state) => {
      if (state.selectedTimes.length > 0) {
        return { selectedTimes: [] }
      }

      const unbilledTime = this.state.unbilledTime.map(time => ({
        id: time.id,
        unitsToBill: time.unitsToBill,
      }))

      return { selectedTimes: unbilledTime }
    })
  }
  handleUnitsToBillChange = (timeId, value) => {
    this.setState((state) => {
      const timeEntry = state.unbilledTime.find(time => time.id === timeId)

      const selectedTimes = state.selectedTimes.concat({
        id: timeEntry.id,
        unitsToBill: value,
      })

      return { selectedTimes }
    })
    this.setState((state) => {
      const unbilledTime = state.unbilledTime.concat()
      const index = unbilledTime.findIndex(item => item.id === timeId)

      if (index > -1) {
        let cost = value * unbilledTime[index].rate
        if (unbilledTime[index].__typename === 'TimeEntryType') {
          cost /= 10
        }
        unbilledTime[index] = {
          ...unbilledTime[index],
          unitsToBill: parseInt(value, 10),
          cost,
        }

        return { unbilledTime }
      }

      return null
    })
  }
  handleCreateInvoice = async (values) => {
    this.setState({ loading: true })

    const matterId = this.props.initialValues.matter.id

    const { data } = await this.props.mutate({
      variables: {
        invoiceData: {
          ...filter(doc, { ...values, matter: { ...values.matter, client: values.client } }),
          billingMethod: values.matter.billingMethod,
          recordedTime: this.state.selectedTimes,
        },
      },
      refetchQueries: [{ query: getMatter, variables: { id: matterId } }],
      update: (store, { data: { createInvoice } }) => {
        try {
          const cache = store.readQuery({
            query: getInvoices,
            variables: {
              after: null,
              numberOrClientName: null,
              isPaid: null,
              status: null,
            },
          })

          cache.invoices.edges.push({
            cursor: '',
            node: createInvoice.invoice,
            __typename: 'InvoiceType',
          })

          store.writeQuery({
            query: getInvoices,
            data: cache,
            variables: {
              after: null,
              numberOrClientName: null,
              isPaid: null,
              status: null,
            },
          })
        } catch (e) {} // eslint-disable-line
      },
    })

    if (data.createInvoice.errors.length > 0) {
      console.log(data.createInvoice.errors)
    } else {
      Router.push(
        `/invoice?id=${data.createInvoice.invoice.id}`,
        `/invoice/${data.createInvoice.invoice.id}`,
      )
    }

    this.setState({ loading: false })
  }
  handleOnMatterSelect = ({ value, label }) => {
    this.props.dispatch(change('invoiceForm', 'matter.id', value))
    this.props.dispatch(change('invoiceForm', 'matter.name', label))
  }
  handleOnClientSelect = ({ value, label }) => {
    this.props.dispatch(change('invoiceForm', 'client', { id: value, name: label }))
  }
  handleBillingMethodChange = (event) => {
    const { value } = event.target

    if (parseInt(value, 10) === 2) {
      this.props.dispatch(change('invoiceForm', 'fixedPriceItems', []))
      this.setState({ form: 1 })
    }
  }
  handleCreateFixedPriceItem = fixedPriceItem =>
    this.props.dispatch(
      change(
        'invoiceForm',
        'fixedPriceItems',
        this.props.form.fixedPriceItems.concat({
          ...fixedPriceItem,
          id: this.props.form.fixedPriceItems.length + 1,
        }),
      ),
    )
  handleRemoveFixedPriceItem = (fixedPriceItemId) => {
    const fixedPriceItems = this.props.form.fixedPriceItems.filter(
      item => item.id !== fixedPriceItemId,
    )

    this.props.dispatch(change('invoiceForm', 'fixedPriceItems', fixedPriceItems))
  }
  handleOnClientEdit = () => {
    this.props.dispatch(change('invoiceForm', 'client', null))
  }
  toggleModal = () => this.setState({ modal: !this.state.modal })
  selectForm = form => this.setState({ form })
  render() {
    const { form } = this.props
    const currencyMask = createNumberMask({
      prefix: '$',
      decimalPlaces: 2,
      locale: 'en-US',
    })
    return [
      <div key={1} className="card">
        <div className="card-body">
          <form
            className="form-row form-group p-3 form-control-line"
            onSubmit={this.props.handleSubmit(this.handleCreateInvoice)}
          >
            <Field name="fixedPriceItems" component="input" type="hidden" />
            <div className="col mr-sm-5">
              <div className="form-row form-group form-inline" style={{ overflow: 'visible' }}>
                <div className="col-sm-2">
                  <label htmlFor="client" className="mr-sm-3">
                    Client:
                  </label>
                </div>
                <div className="col">
                  <a href={`/client/${form.matter.client.id}`} target="_blank">
                    {form.matter.client.name}
                  </a>
                </div>
              </div>
              <div className="form-row form-group form-inline" style={{ overflow: 'visible' }}>
                <div className="col-sm-2">
                  <label htmlFor="matter" className="mr-sm-3">
                    Matter:
                  </label>
                </div>
                <div className="col">
                  <a href={`/matter/${form.matter.id}`} target="_blank">
                    {form.matter.name}
                  </a>
                </div>
              </div>
              <div className="form-row form-group form-inline">
                <div className="col-sm-2">
                  <label htmlFor="budget" className="mr-sm-3">
                    Budget:
                  </label>
                </div>
                <div className="col">
                  <Field
                    {...currencyMask}
                    component={renderInput}
                    name="matter.budget"
                    id="budget"
                    className="form-control w-100"
                  />
                </div>
              </div>
              <div className="form-row form-group form-inline">
                <div className="col-sm-2">
                  <label className="mr-sm-2" htmlFor="billingMethod">
                    Method:
                  </label>
                </div>
                <div className="col">
                  <Field
                    name="matter.billingMethod"
                    component="select"
                    onChange={this.handleBillingMethodChange}
                    className="custom-select form-control w-100 mb-2 mr-sm-2 mb-sm-0"
                    id="billingMethod"
                  >
                    <option value={1}>Fixed Price</option>
                    <option value={2}>Time Entry</option>
                  </Field>
                </div>
              </div>
              <div className="btn-group">
                <button style={{ width: 80 }} type="button" className="btn btn-warning">
                  W-Off
                </button>
                <Button
                  title="Invoice"
                  loading={this.state.loading}
                  className="btn btn-success"
                  type="submit"
                  style={{ width: 80 }}
                />
              </div>
            </div>
            <div className="col-8">
              <label htmlFor="description">Description:</label>
              <Field
                component={renderTextarea}
                style={{ height: 194 }}
                name="matter.description"
                id="description"
              />
            </div>
            <style jsx>{`
              .form-row {
                font-size: 17px;
              }
            `}</style>
          </form>
        </div>
      </div>,
      <div key={2} className="card">
        <ul className="nav nav-tabs profile-tab" role="tablist">
          <Tab number={1} currentNumber={this.state.form} onClick={this.selectForm}>
            Unbilled
          </Tab>
          <Tab
            number={2}
            currentNumber={this.state.form}
            onClick={this.selectForm}
            disabled={parseInt(this.props.form.matter.billingMethod, 10) === 2}
          >
            Fixed price items
          </Tab>
        </ul>
        <div className="card-body">
          {this.state.form === 1 && [
            <div key={1} className="pull-right form-group">
              <button
                style={{ width: 106 }}
                className="btn btn-success"
                type="button"
                onClick={this.toggleSelectAll}
              >
                {this.state.selectedTimes.length > 0 ? 'Unselect all' : 'Select all'}
              </button>
            </div>,
            <UnbilledTime
              key={2}
              handleUnitsToBillChange={this.handleUnitsToBillChange}
              toggleTimeEntry={this.toggleTimeEntry}
              selectedTimes={this.state.selectedTimes}
              unbilledTime={this.state.unbilledTime}
            />,
          ]}
          {this.state.form === 2 && [
            <div key={1} className="pull-right form-group">
              <button onClick={this.toggleModal} className="btn btn-success" type="button">
                Add
              </button>
            </div>,
            <FixedPriceItemList
              key={2}
              handleRemoveFixedPriceItem={this.handleRemoveFixedPriceItem}
              fixedPriceItems={this.props.form.fixedPriceItems}
            />,
          ]}
        </div>
      </div>,
      <FixedPriceItemForm
        key={3}
        toggleModal={this.toggleModal}
        modal={this.state.modal}
        handleCreateFixedPriceItem={this.handleCreateFixedPriceItem}
      />,
    ]
  }
}

const createInvoice = gql`
  mutation createInvoice($invoiceData: InvoiceInput!) {
    createInvoice(invoiceData: $invoiceData) {
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
    matter: {},
    client: {},
  }

  const matter = values.matter || {}
  const client = values.client || {}

  if (parseInt(matter.billingMethod, 10) === 1 && !matter.budget) {
    errors.budget = 'Budget is requried for fixed price invoice'
  }
  if (!client.name) {
    errors.client.name = 'This field is requried!'
  }
  if (!matter.description) {
    errors.matter.description = 'This field is requried!'
  }

  return errors
}

export default reduxForm({ form: 'invoiceForm', validate })(
  compose(
    graphql(createInvoice),
    connect(state => ({ form: state.form.invoiceForm.values })),
  )(InvoiceForm),
)
