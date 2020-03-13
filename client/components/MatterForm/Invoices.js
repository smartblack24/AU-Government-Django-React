import React from 'react'
import Link from 'next/link'
import moment from 'moment'

import { formatCurrency } from 'utils'

export default ({ matterId, invoices }) => (
  <div>
    <div className="dt-buttons float-right col-xs-12">
      <Link href={`/addinvoice?id=${matterId}`} as={`/invoices/add/${matterId}`} prefetch>
        <a className="dt-button buttons-html5">
          <span>Create invoice</span>
        </a>
      </Link>
    </div>
    <table id="mainTable" className="table table-bordered table-striped m-b-0">
      <thead>
        <tr>
          <th>Invoice</th>
          <th>Date created</th>
          <th>Due date</th>
          <th>Invoice amount ex GST</th>
          <th>Invoice amount incl GST</th>
          <th>Outstanding incl GST</th>
        </tr>
      </thead>
      <tbody>
        {invoices.edges.map(({ node }) => (
          <Link key={node.id} href={`/invoice?id=${node.id}`} as={`/invoice/${node.id}`}>
            <tr key={node.id}>
              <td>{node.number}</td>
              <td>{moment(node.createdDate).format('MMM Do YY')}</td>
              <td>{moment(node.dueDate).format('MMM Do YY')}</td>
              <td>{formatCurrency(node.valueExGst)}</td>
              <td>{formatCurrency(node.valueInclGst)}</td>
              <td>{formatCurrency(node.netOutstanding)}</td>
            </tr>
          </Link>
        ))}
      </tbody>
    </table>
  </div>
)
