import React from 'react'
import moment from 'moment'

import RemoveIcon from 'components/RemoveIcon'
import { getGstStatusDisplay, getBillableStatusDisplay, formatCurrency } from 'utils'

/* eslint-disable */
export default ({ fixedPriceItems, handleRemoveFixedPriceItem }) => {
  const calculateValueExGST = item => {
    const rate =
      item.rate.toString().indexOf('$') > -1
        ? parseFloat(item.rate.toString().slice(1, item.rate.toString().length))
        : parseFloat(item.rate)

    return rate * item.units
  }
  const calculateValueIncGST = item =>
    parseInt(item.gstStatus, 10) === 1
      ? calculateValueExGST(item) + calculateValueExGST(item) * 10 / 100
      : calculateValueExGST(item)
  return [
    <table key={1} className="table table-bordered table-striped m-b-0">
      <thead>
        <tr>
          <th>Date entered</th>
          <th>Units</th>
          <th>Entry description</th>
          <th>Rate</th>
          <th>Billable status</th>
          <th>Value ex GST</th>
          <th>GST Status</th>
          <th>Value inc GST</th>
          <th>Delete</th>
        </tr>
      </thead>
      <tbody>
        {fixedPriceItems.map(item => (
          <tr key={item.id}>
            <td>{moment(item.date).format('MMM Do YY')}</td>
            <td>{item.units}</td>
            <td>{item.description}</td>
            <td>{formatCurrency(item.rate)}</td>
            <td>{getBillableStatusDisplay(item.status)}</td>
            <td>{formatCurrency(calculateValueExGST(item))}</td>
            <td>{getGstStatusDisplay(item.gstStatus)}</td>
            <td>{formatCurrency(calculateValueIncGST(item))}</td>
            <td className="delete">
              <RemoveIcon value={item.id} onClick={handleRemoveFixedPriceItem} />
            </td>
          </tr>
        ))}
      </tbody>
      <style jsx>{`
        .delete {
          width: 10px;
          text-align: center;
        }
      `}</style>
    </table>,
    <div key={2} className="d-flex  justify-content-end mt-sm-3">
      <div className="mr-sm-3">
        <strong>Total:</strong> {formatCurrency(fixedPriceItems
          .reduce((prevValue, currValue) => prevValue + calculateValueExGST(currValue), 0))}{' '}
        ex GST
      </div>
      <div>
        {formatCurrency(fixedPriceItems
          .reduce((prevValue, currValue) => prevValue + calculateValueIncGST(currValue), 0))}{' '}
        inc GST
      </div>
    </div>,
  ]
}
