import CustomDatePicker from 'components/DatePicker'
import moment from 'moment'
import React from 'react'
import { Modal, ModalBody, ModalFooter, ModalHeader } from 'reactstrap'
import { Input, Select, Textarea, formatCurrency, parseCurrency } from 'utils'
import { createNumberMask } from 'redux-form-input-masks'

const initialValues = {
  id: null,
  date: moment(),
  rate: 0,
  units: 0,
  unitsToBill: 0,
  gstStatus: 1,
  description: '',
  status: 1,
}

const currencyMask = createNumberMask({
  prefix: '$',
  decimalPlaces: 2,
  locale: 'en-US',
})

class FixedPriceItemForm extends React.PureComponent {
  state = {
    ...initialValues,
  }
  componentWillReceiveProps(nextProps) {
    if (nextProps.initialValues) {
      this.setState({
        id: nextProps.initialValues.id,
        date: moment(nextProps.initialValues.date),
        rate: nextProps.initialValues.rate,
        units: nextProps.initialValues.units,
        unitsToBill: nextProps.initialValues.unitsToBill,
        gstStatus: nextProps.initialValues.gstStatus,
        description: nextProps.initialValues.description,
        status: nextProps.initialValues.status,
      })
    }
  }
  handleDateChange = date => this.setState({ date })
  handleValueChange = (value, fieldName) => {
    if (fieldName === 'units') {
      this.setState({ unitsToBill: value })
    }
    this.setState({ [fieldName]: value })
  }
  submit = () => {
    const rate = parseCurrency(this.state.rate)
    this.props.handleCreateFixedPriceItem({
      ...this.state,
      rate,
      date: this.state.date.format('YYYY-MM-DD'),
    })
  }
  handleSubmit = () => {
    this.submit()
    this.props.toggleModal()
    this.setState(initialValues)
  }
  handleSubmitAndAddAnother = () => {
    this.submit()
    this.setState(initialValues)
  }
  render() {
    const rate = parseCurrency(this.state.rate)
    const valueExGST = rate * this.state.units || 0
    const valueIncGST =
      // eslint-disable-next-line
      parseInt(this.state.gstStatus, 10) === 1 ? valueExGST + (valueExGST * 10) / 100 : valueExGST
    return (
      <Modal key={3} size="lg" isOpen={this.props.modal} toggle={this.props.toggleModal}>
        <ModalHeader toggle={this.props.toggleModal}>Add a fixed price item</ModalHeader>
        <ModalBody>
          <div className="form-control-line">
            <div className="form-group form-row" style={{ overflow: 'visible' }}>
              <div className="col">
                <label htmlFor="date">Date</label>
                <CustomDatePicker id="date" selected={this.state.date} onChange={this.handleDateChange} />
              </div>
              <div className="col">
                <label htmlFor="units">Units</label>
                <Input
                  type="text"
                  id="units"
                  name="units"
                  normalize={parseCurrency}
                  value={this.state.units === 0 ? '' : this.state.units}
                  className="form-control"
                  onChange={this.handleValueChange}
                />
              </div>
              <div className="col">
                <label htmlFor="rate">Rate</label>
                <Input
                  type="text"
                  name="rate"
                  {...currencyMask}
                  id="rate"
                  value={this.state.rate === 0 ? '' : this.state.rate}
                  className="form-control"
                  onChange={this.handleValueChange}
                />
              </div>
            </div>
            <div className="form-group">
              <label htmlFor="description">Description</label>
              <Textarea
                className="form-control"
                id="description"
                name="description"
                value={this.state.description}
                onChange={this.handleValueChange}
              />
            </div>
            <div className="form-group form-row">
              <div className="col">
                <label htmlFor="status">Billable Status</label>
                <Select
                  className="form-control w-75"
                  id="status"
                  name="status"
                  value={this.state.status}
                  onChange={this.handleValueChange}
                >
                  <option value={1}>Billable</option>
                  <option value={2}>Non billable</option>
                </Select>
              </div>
              <div className="col">
                <label htmlFor="gstStatus">GST Status</label>
                <Select
                  className="form-control w-75"
                  id="gstStatus"
                  name="gstStatus"
                  value={this.state.gstStatus}
                  onChange={this.handleValueChange}
                >
                  <option value={1}>GST(10%)</option>
                  <option value={2}>GST Export (0%)</option>
                  <option value={3}>BAS Excluded (0%)</option>
                </Select>
              </div>
              <div className="col">
                <span>Value ex GST</span>{' '}
                <div className="mt-sm-3 w-100">
                  <strong>{formatCurrency(valueExGST)}</strong>
                </div>
              </div>
              <div className="col">
                <span>Value inc GST</span>{' '}
                <div className="mt-sm-3 w-100">
                  <strong>{formatCurrency(valueIncGST)}</strong>
                </div>
              </div>
            </div>
          </div>
        </ModalBody>
        <ModalFooter>
          <button
            className="btn btn-primary"
            type="button"
            onClick={this.handleSubmitAndAddAnother}
          >
            Save and add another
          </button>
          <button className="btn btn-success" type="button" onClick={this.handleSubmit}>
            Save
          </button>
        </ModalFooter>
      </Modal>
    )
  }
}

export default FixedPriceItemForm
