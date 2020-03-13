import React from 'react'
import moment from 'moment'

export default ({ history }) => (
  <table id="mainTable" className="table table-bordered table-striped m-b-0">
    <thead>
      <tr>
        <th>Date</th>
        <th>Description</th>
        <th>Staff Member</th>
      </tr>
    </thead>
    <tbody>
      {history.map(record => (
        <tr key={record.id}>
          <td>{moment(record.date).format('MMM Do YY')}</td>
          <td>{record.changeReason}</td>
          <td>{record.user}</td>
        </tr>
      ))}
    </tbody>
  </table>
)
