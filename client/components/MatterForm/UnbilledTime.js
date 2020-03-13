import React, { Fragment } from 'react'
import Link from 'next/link'
import { Modal, ModalHeader, ModalBody } from 'reactstrap'
import { withApollo } from 'react-apollo'
import moment from 'moment'

import UnbilledTimeTable from 'components/UnbilledTimeTable'
import TimeEntryForm from 'components/TimeEntryForm'

class UnbilledTime extends React.Component {
  state = { modal: false, editModal: false }
  toggleModal = () => this.setState({ modal: !this.state.modal })
  toggleEditModal = (timeEntryValues) => {
    const timeEntry = timeEntryValues
    if (timeEntry && timeEntry) {
      this.setState({
        editModal: !this.state.editModal,
        timeEntryEditValues: {
          id: timeEntry.id,
          client: this.props.initialValues.client,
          matter: {
            id: this.props.initialValues.id,
            name: this.props.initialValues.name,
          },
          staffMember: timeEntry.staffMember,
          date: timeEntry.date,
          status: timeEntry.statusDisplay === 'Billable' ? 1 : 2,
          gstStatus: timeEntry.gstStatus,
          rate: timeEntry.rate,
          cost: timeEntry.cost,
          units: timeEntry.units,
          description: timeEntry.description,
        },
      })
    } else {
      this.setState({ editModal: !this.state.editModal })
    }
  }
  render() {
    const { initialValues } = this.props
    const timeEntryValues = {
      client: initialValues.client,
      matter: {
        id: initialValues.id,
        name: initialValues.name,
      },
      date: moment().format('YYYY-MM-DD'),
      status: 1,
      gstStatus: 1,
      staffMember: this.props.user,
      rate: this.props.user.rate,
    }
    return (
      <Fragment>
        <div>
          <div className="row justify-content-end mb-3">
            <div className="col-auto">
              <button className="btn btn-success" onClick={this.toggleModal}>
                Add Time Entry
              </button>
            </div>
            <div className="col-auto">
              <Link
                href={`/addinvoice?id=${initialValues.id}`}
                as={`/invoices/add/${initialValues.id}`}
                prefetch
              >
                <a className="btn btn-info">Create invoice</a>
              </Link>
            </div>
          </div>
          <UnbilledTimeTable
            unbilledTime={initialValues.unbilledTime}
            modal={this.toggleEditModal}
          />
        </div>
        <Modal size="lg" isOpen={this.state.modal} toggle={this.toggleModal}>
          <ModalHeader toggle={this.toggleModal}>Add a Time Entry</ModalHeader>
          <ModalBody>
            <TimeEntryForm
              afterCloseCallBack={this.toggleModal}
              buttonTitle="Add"
              editable={false}
              initialValues={timeEntryValues}
            />
          </ModalBody>
        </Modal>
        <Modal size="lg" isOpen={this.state.editModal} toggle={this.toggleEditModal}>
          <ModalHeader toggle={this.toggleEditModal}>Edit a Time Entry</ModalHeader>
          <ModalBody>
            <TimeEntryForm
              afterCloseCallBack={this.toggleEditModal}
              buttonTitle="Save"
              initialValues={this.state.timeEntryEditValues}
              isEdit
            />
          </ModalBody>
        </Modal>
      </Fragment>
    )
  }
}

export default withApollo(UnbilledTime)
