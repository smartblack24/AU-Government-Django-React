import React from 'react'
import moment from 'moment'

import Tr from 'utils/Tr'
import EditableTd from 'utils/EditableTd'
import { formatCurrency } from 'utils'

/* eslint-disable no-mixed-operators */

export default ({ unbilledTime, selectedTimes, toggleTimeEntry, handleUnitsToBillChange }) => {
  const totaExGst = unbilledTime.reduce((total, time) => {
    const gst =
      time.gstStatus === 1
        ? parseFloat(time.cost) + (10 / 100) * parseFloat(time.cost)
        : parseFloat(time.cost)

    return total + gst
  }, 0)
  return (
    <div>
      <table id="mainTable" className="table table-bordered table-striped m-b-0">
        <thead>
          <tr>
            <th>Date entered</th>
            <th>Staff</th>
            <th>Entry description</th>
            <th>Billable status</th>
            <th>Actual units</th>
            <th style={{ width: '5%' }}>Units to bill</th>
            <th>Rate</th>
            <th>Value ex GST</th>
            <th>GST Status</th>
            <th>Value inc GST</th>
          </tr>
        </thead>
        <tbody>
          {unbilledTime.map(time => (
            <Tr
              key={`${time.__typename}-${time.id}`}
              value={time.id}
              onClick={toggleTimeEntry}
              className={
                selectedTimes.map(item => item.id).includes(time.id) ? 'table-success' : ''
              }
            >
              <td style={{ width: '7%' }}>{moment(time.date).format('DD/MM/YYYY')}
                {time.recordType === 2 && <span style={{ marginLeft: '5px' }} className="badge badge-info">sales</span>}
              </td>
              <td>{time.staffMember && time.staffMember.fullName}</td>
              <td>{time.description}</td>
              <td>{time.statusDisplay}</td>
              <td>{time.units}</td>
              <EditableTd onChange={handleUnitsToBillChange} id={time.id} fieldName="unitsToBill">
                {time.statusDisplay === 'Non billable' ? 0 : parseFloat(time.unitsToBill)}
              </EditableTd>
              <td>{formatCurrency(time.rate)}</td>
              <td>{formatCurrency(time.cost)}</td>
              <td>{time.gstStatusDisplay}</td>
              <td>
                {time.gstStatus && time.gstStatus === 1
                  ? formatCurrency(parseFloat(time.cost) + (10 / 100) * time.cost)
                  : formatCurrency(time.cost)}
              </td>
            </Tr>
          ))}
        </tbody>
      </table>
      <div className="p-3 d-flex justify-content-between">
        <div>
          <strong>Total actual units: </strong>
          {unbilledTime.reduce((units, time) => units + parseFloat(time.units), 0)}
        </div>
        <div className="d-flex justify-content-between">
          <div style={{ marginRight: 20 }}>
            <strong>Total: </strong>
            {formatCurrency(
              unbilledTime.reduce((total, time) => total + parseFloat(time.cost), 0),
            )}{' '}
            ex GST
          </div>
          <div>{formatCurrency(totaExGst)} inc GST</div>
        </div>
      </div>
    </div>
  )
}
