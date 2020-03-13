import React, { Fragment } from 'react'
import moment from 'moment'
import { formatCurrency } from 'utils'
import Button from 'components/Button'
import PaymentForm from './PaymentForm'

class Payments extends React.PureComponent {
  state = {
    modal: false,
  }

  toggleModal = () => {
    const { modal } = this.state
    this.setState({ modal: !modal })
  }

  render() {
    const { payments, user, isInXero, fetchingPayments, invoiceId } = this.props
    const { modal } = this.state

    const { canUseXero } = user

    return (
      <Fragment>
        <div>
          <div className="col-12 mb-3 pr-0 text-right">
            {canUseXero && isInXero &&
            <Button
              className="btn btn-primary mr-2"
              icon="fa fa-credit-card"
              title="Fetch from Xero"
              loading={fetchingPayments}
              onClick={this.props.onFetchPayments}
            />
            }
            <Button
              className="btn btn-info"
              icon="fa fa-plus"
              title="Add"
              onClick={this.toggleModal}
            />
          </div>
          <table id="mainTable" className="table table-bordered table-striped m-b-0">
            <thead>
              <tr>
                <th>Payment date</th>
                <th>Payment amount</th>
                <th>Payment method</th>
              </tr>
            </thead>
            <tbody>
              {payments.map(payment => (
                <tr key={payment.id}>
                  <td>{moment(payment.date).format('MMM Do YY')}</td>
                  <td>{formatCurrency(payment.amount)}</td>
                  <td>{payment.methodDisplay}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <PaymentForm
          user={user}
          invoiceId={invoiceId}
          modal={modal}
          toggleModal={this.toggleModal}
          initialValues={{ date: moment().format('YYYY-MM-DD'), method: 1 }}
        />
      </Fragment>
    )
  }
}

export default Payments
