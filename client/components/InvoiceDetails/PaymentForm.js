import React from 'react'
import { Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap'
import { reduxForm, Field, change, reset } from 'redux-form'
import moment from 'moment'
import { graphql, gql } from 'react-apollo'
import { createNumberMask } from 'redux-form-input-masks'
import swal from 'sweetalert'
import { renderInput } from 'utils'
import { invoiceFragment, paymentFragment } from 'fragments'
import CustomDatePicker from 'components/DatePicker'
import Button from 'components/Button'

class PaymentForm extends React.PureComponent {
  state = {
    date: moment(),
    loading: false,
  }
  handleDateChange = (date) => {
    this.setState({ date })
    this.props.dispatch(change('paymentForm', 'date', date.format('YYYY-MM-DD')))
  }
  handleOnSubmit = async (values) => {
    this.setState({ loading: true })

    const amount = parseFloat(values.amount.toString().slice(0, values.amount.toString().length))

    const { data } = await this.props.mutate({
      variables: { ...values, amount, invoiceId: this.props.invoiceId },
      update: (store, { data: { addPayment } }) => {
        if (addPayment.errors.length === 0) {
          const cache = store.readFragment({
            id: `InvoiceType-${this.props.invoiceId}`,
            fragment: invoiceFragment,
            fragmentName: 'Invoice',
          })

          cache.receivedPayments =
            parseFloat(cache.receivedPayments) + parseFloat(addPayment.payment.amount)
          cache.netOutstanding =
            parseFloat(cache.netOutstanding) - parseFloat(addPayment.payment.amount)

          cache.payments.push(addPayment.payment)
          const history = cache.history.concat()
          history.unshift({
            id: `payment-${cache.history.length + 1}`,
            changeReason: 'Payment was made',
            date: moment().format('YYYY-MM-DD'),
            user: this.props.user.fullName,
          })

          cache.history = history

          store.writeFragment({
            id: `InvoiceType-${this.props.invoiceId}`,
            fragment: invoiceFragment,
            fragmentName: 'Invoice',
            data: cache,
          })
        }
      },
    })

    if (data.addPayment.errors.length > 0) {
      swal({ icon: 'error', text: data.addPayment.errors.join('\n') })
    } else {
      this.props.dispatch(reset('paymentForm'))
      this.props.toggleModal()
      swal({ icon: 'success', text: 'Payments was save in database' })
    }

    this.setState({ loading: false })
  }

  render() {
    const currencyMask = createNumberMask({
      prefix: '$',
      decimalPlaces: 2,
      locale: 'en-US',
    })
    return (
      <Modal isOpen={this.props.modal} toggle={this.props.toggleModal}>
        <ModalHeader toggle={this.props.toggleModal}>Add a payment</ModalHeader>
        <form onSubmit={this.props.handleSubmit(this.handleOnSubmit)}>
          <ModalBody>
            <div>
              <div className="form-group">
                <label htmlFor="date">Date</label>
                <CustomDatePicker id="date" selected={this.state.date} onChange={this.handleDateChange} />
              </div>
              <div>
                <label htmlFor="amount">Amount</label>
                <Field {...currencyMask} id="amount" component={renderInput} name="amount" />
              </div>
              <div>
                <label htmlFor="method">Method</label>
                <Field name="method" id="method" component="select" className="form-control">
                  <option value={1}>EFT</option>
                  <option value={2}>BPAY</option>
                  <option value={3}>Credit Card</option>
                  <option value={4}>Cheque</option>
                  <option value={5}>Trust Account</option>
                  <option value={6}>Trust Clearing Account</option>
                  <option value={7}>Cash</option>
                  <option value={8}>Write Off</option>
                </Field>
              </div>
            </div>
          </ModalBody>
          <ModalFooter>
            <Button
              title="Save"
              loading={this.state.loading}
              className="btn btn-success"
              type="submit"
              style={{ width: 80 }}
            />
          </ModalFooter>
        </form>
      </Modal>
    )
  }
}

const addPayment = gql`
  mutation addPayment($invoiceId: ID!, $method: Int!, $amount: Float!, $date: String!) {
    addPayment(invoiceId: $invoiceId, method: $method, amount: $amount, date: $date) {
      errors
      payment {
        ...Payment
      }
    }
  }
  ${paymentFragment}
`

export default reduxForm({ form: 'paymentForm' })(graphql(addPayment)(PaymentForm))
