import React, { Fragment } from 'react'
import swal from 'sweetalert'
import { graphql, compose } from 'react-apollo'
import gql from 'graphql-tag'
import Router from 'next/router'
import { connect } from 'react-redux'
import { getMatter } from 'queries'
import { getInvoices } from 'pages/invoices'
import { BACKEND_URL } from 'constants/page'
import { Tab, swalCreator } from 'utils'
import Button from 'components/Button'
import Slider from 'components/Slider'
import Details from './Details'
import Info from './Info'
import TimeEntryRecords from './TimeEntryRecords'
import Payments from './Payments'
import ActivityAudit from './ActivityAudit'

const getInvoice = gql`
  query invoice($id: ID!) {
    invoice(id: $id) {
      id
      number
      createdDate
      dueDate
      valueInclGst
      valueExGst
      billingMethod
      status {
        id
      }
      timeEntryValue
      fixedPriceValue
      statusDisplay
      receivedPayments
      netOutstanding
      history
      isPaid
      totalBilledValue
      friendlyReminder
      firstReminder
      secondReminder
      canSendXero
      isInXero
      payments {
        id
        method
        methodDisplay
        amount
        date
      }
      matter {
        id
        name
        description
        billingMethod
        totalTimeValue
        client {
          id
          name
        }
        manager {
          id
          fullName
        }
      }
    }
  }
`

class InvoiceDetails extends React.Component {
  state = {
    form: 1,
    sendingEmail: false,
    sendingToXero: false,
    fetchingFromXero: false,
  }

  handleSendEmail = async () => {
    const { id } = this.props.initialValues

    this.setState({ sendingEmail: true })

    const res = await this.props.sendInvoiceEmail({
      variables: { invoiceId: id },
    })


    this.setState({ sendingEmail: false })

    const { success, errors } = res.data.sendInvoiceEmail

    swalCreator({ success, errors, successMsg: 'The email has been sent successfully' })
  }

  handleRemoveInvoice = async () => {
    const { initialValues } = this.props
    const { matter } = initialValues

    const willDelete = await swal({
      title: 'Confirmation',
      text: 'Are you sure?',
      icon: 'warning',
      buttons: {
        cancel: true,
        confirm: {
          closeModal: false,
        },
      },
    })

    if (willDelete) {
      const res = await this.props.removeInvoice({
        variables: {
          instanceId: initialValues.id,
          instanceType: 8,
        },
        refetchQueries: [
          { query: getMatter, variables: { id: matter.id } },
        ],
        update: (store, { data: { removeInstance } }) => {
          try {
            if (removeInstance.errors.length === 0) {
              const cache = store.readQuery({
                query: getInvoices,
                variables: {
                  after: null,
                  numberOrClientName: null,
                  isPaid: null,
                  status: null,
                },
              })

              cache.invoices.edges = cache.invoices.edges.filter(
                ({ node }) => node.id !== initialValues.id,
              )

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
            }
          } catch (e) {} // eslint-disable-line
        },
      })

      const { errors } = res.data.removeInstance

      if (errors.length > 0) {
        swal({ icon: 'error', text: errors.join('\n') })
      } else {
        Router.push('/invoices')
        swal({ icon: 'success', text: 'The invoice has been removed successfully' })
      }
    }
  }

  handleSendToXero = async () => {
    this.setState({ sendingToXero: true })

    const { id } = this.props.initialValues

    const res = await this.props.sendInvoiceToXero({
      variables: { invoiceId: id },
      refetchQueries: [
        { query: getInvoice, variables: { id } },
      ],
    })

    this.setState({ sendingToXero: false })

    const { success, errors } = res.data.sendInvoiceToXero

    swalCreator({ success, errors, successMsg: 'The invoice has been sent successfully' })
  }

  handleFetchPaymentsFromXero = async () => {
    this.setState({ fetchingFromXero: true })

    const { id } = this.props.initialValues

    const res = await this.props.fetchPaymentsFromXero({
      variables: { invoiceId: id },
      refetchQueries: [
        { query: getInvoice, variables: { id } },
      ],
    })

    this.setState({ fetchingFromXero: false })

    const { success, errors } = res.data.fetchPaymentsFromXero

    swalCreator({ success, errors, successMsg: 'Fetched payments from Xero' })
  }

  selectForm = form => this.setState({ form })

  render() {
    const { initialValues, user } = this.props
    const {
      canSendXero,
      isInXero,
      id,
      matter,
      billingMethod,
      // fixedPriceItems,
      // disbursements,
      receivedPayments,
      // timeEntries,
      payments,
      statusDisplay,
      history,
    } = initialValues
    let displayEmailButton = false
    if (statusDisplay === 'Approved'
      || statusDisplay === 'Printed'
      || statusDisplay === 'In Xero') {
      displayEmailButton = true
    }
    // const recordedTime = timeEntries.edges
    const { sendingToXero, sendingEmail, fetchingFromXero, form } = this.state
    const { canUseXero } = user

    return (
      <Fragment>
        <div className="text-right py-3">
          {canUseXero && canSendXero &&
            <Button
              className="btn btn-primary mr-2"
              icon="fa fa-credit-card"
              title="Send To Xero"
              loading={sendingToXero}
              onClick={this.handleSendToXero}
            />
          }
          { displayEmailButton && (
            <Button
              className="btn btn-warning mr-2"
              icon="fa fa-envelope"
              title="Send Email"
              loading={sendingEmail}
              onClick={this.handleSendEmail}
            />
          )}
          <Button
            className="btn btn-danger mr-2"
            icon="fa fa-times"
            title="Delete"
            onClick={this.handleRemoveInvoice}
          />
          <a
            href={`${BACKEND_URL}/pdf/invoice/${id}/`}
            target="_blank"
            className="btn btn-success"
          >
            <i className="fa fa-download" /> PDF
          </a>
        </div>
        <div className="card">
          <Slider id="invoice-slider" title="Info" initialState="open">
            <div className="card-body">
              {isInXero &&
                <div className="ribbon ribbon-info ribbon-right" style={{ top: 50 }}>
                  In Xero
                </div>
              }
              <Info
                user={user}
                receivedPayments={receivedPayments}
                initialValues={initialValues}
              />
            </div>
          </Slider>
        </div>
        <div className="card">
          <ul className="nav nav-tabs profile-tab" role="tablist">
            <Tab number={1} currentNumber={form} onClick={this.selectForm}>
              Details
            </Tab>
            <Tab number={2} currentNumber={form} onClick={this.selectForm}>
              Payments
            </Tab>
            <Tab number={3} currentNumber={form} onClick={this.selectForm}>
              Activity Audit
            </Tab>
            <Tab number={4} currentNumber={form} onClick={this.selectForm}>
              Time Entry Records
            </Tab>
          </ul>
          <div className="card-body">
            {form === 1 && (
              <Details
                invoice={initialValues}
                matter={matter}
                // recordedTime={
                //   billingMethod === 1
                //     ? fixedPriceItems.edges.concat(disbursements.edges)
                //     : recordedTime.concat(disbursements.edges)
                // }
              />
            )}
            {form === 2 && (
              <Payments
                user={user}
                payments={payments}
                invoiceId={id}
                isInXero={isInXero}
                fetchingPayments={fetchingFromXero}
                onFetchPayments={this.handleFetchPaymentsFromXero}
              />
            )}
            {form === 3 && <ActivityAudit history={history} />}
            {form === 4 && (
              <TimeEntryRecords
                billingMethod={billingMethod}
                invoice={initialValues}
                matter={matter}
                // recordedTime={recordedTime}
              />
            )}
          </div>
        </div>
      </Fragment>
    )
  }
}

const removeInvoice = gql`
  mutation removeInvoice($instanceId: ID!, $instanceType: Int!) {
    removeInstance(input: { instanceId: $instanceId, instanceType: $instanceType }) {
      errors
    }
  }
`

const sendInvoiceEmail = gql`
  mutation sendInvoiceEmail($invoiceId: ID!) {
    sendInvoiceEmail(invoiceId: $invoiceId) {
      success
      errors
    }
  }
`

const sendInvoiceToXero = gql`
  mutation sendInvoiceToXero($invoiceId: ID!) {
    sendInvoiceToXero(invoiceId: $invoiceId) {
      success
      errors
    }
  }
`

const fetchPaymentsFromXero = gql`
  mutation fetchPaymentsFromXero($invoiceId: ID!) {
    fetchPaymentsFromXero(invoiceId: $invoiceId) {
      success
      errors
    }
  }
`

export default compose(
  graphql(removeInvoice, { name: 'removeInvoice' }),
  graphql(sendInvoiceEmail, { name: 'sendInvoiceEmail' }),
  graphql(sendInvoiceToXero, { name: 'sendInvoiceToXero' }),
  graphql(fetchPaymentsFromXero, { name: 'fetchPaymentsFromXero' }),
  connect(),
)(InvoiceDetails)
