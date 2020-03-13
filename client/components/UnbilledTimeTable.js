import React from 'react'
import moment from 'moment'

import { formatCurrency } from 'utils'
// import Pre from 'components/Pre'

export default ({ unbilledTime, modal }) => (
  <table id="mainTable" className="table table-bordered table-striped m-b-0">
    <thead>
      <tr>
        <th>Date created</th>
        <th>Staff Member</th>
        <th>Description</th>
        <th>Billable</th>
        <th>Actual units</th>
        <th>Units to bill</th>
        <th>Rate</th>
        <th>Value</th>
      </tr>
    </thead>
    <tbody>
      {unbilledTime.map(time => (
        <tr key={`${time.__typename}-${time.id}`} onClick={() => modal(time)}>
          <td style={{ width: '10%' }}>{moment(time.date).format('DD/MM/YYYY')} {time.recordType === 2 && <span className="badge badge-info">sales</span>}</td>
          <td>{time.staffMember && time.staffMember.fullName }</td>
          <td style={{ whiteSpace: 'pre-line' }}>{time.description}</td>
          <td>{time.statusDisplay && time.statusDisplay}</td>
          <td>{time.units}</td>
          <td>{time.statusDisplay === 'Non billable' ? 0 : time.unitsToBill}</td>
          <td>{formatCurrency(time.rate)}</td>
          <td>{formatCurrency(time.cost)}</td>
        </tr>
      ))}
    </tbody>
    <style jsx>{`
      .delete {
        width: 10px;
        text-align: center;
      }
    `}</style>
  </table>
)
