import React from 'react'
import { graphql, gql } from 'react-apollo'


import { formatCurrency } from 'utils'
import LoadSpinner from 'components/LoadSpinner'


class AverageInvoice extends React.Component {
  state = {}
  componentDidMount() {
    this.props.onRef(this)
  }
  refetchData = ({ fromDate, toDate }) => this.props.data.refetch({ fromDate, toDate })
  render() {
    return (
      <div>
        <div className="table-responsive" style={{ minHeight: 500, overflowX: 'hidden' }}>
          <div>
            {this.props.data.loading
              ? <LoadSpinner />
              :
              <table id="mainTable" className="table table-bordered table-striped m-b-0">
                <thead>
                  <tr>
                    <th />
                    <th>Average Invoice</th>
                    <th>Total Amount</th>
                    <th>Outstanding</th>
                  </tr>
                </thead>
                <tbody>
                  {this.props.data.averageInvoiceReports.map(report => (
                    <tr key={report.id}>
                      <td className="italic">{report.month}</td>
                      <td>{formatCurrency(report.averageAmount)}</td>
                      <td><strong>{formatCurrency(report.totalAmount)}</strong></td>
                      <td>{formatCurrency(report.totalOutstanding)}</td>
                    </tr>
                  ))}
                  <tr className="totals">
                    <td>TOTAL</td>
                    <td>
                      {
                        formatCurrency(this.props.data.averageInvoiceReports.reduce(
                          (prev, curr) => prev + parseFloat(curr.averageAmount),
                          0,
                        ))
                      }
                    </td>
                    <td>
                      {
                        formatCurrency(this.props.data.averageInvoiceReports.reduce(
                          (prev, curr) => prev + parseFloat(curr.totalAmount),
                          0,
                        ))
                      }
                    </td>
                    <td>
                      {
                        formatCurrency(this.props.data.averageInvoiceReports.reduce(
                          (prev, curr) => prev + parseFloat(curr.totalOutstanding),
                          0,
                        ))
                      }
                    </td>
                  </tr>
                </tbody>
              </table>
            }
          </div>
        </div>
        <style jsx>{`
          .italic {
            font-style: italic;
          }
          .totals td {
            background-color: #898B8D;
            color: #fff;
            border: 0;
          }
        `}</style>
      </div>
    )
  }
}

const getReport = gql`
  query averageInvoiceReports($fromDate: String!, $toDate: String!) {
    averageInvoiceReports(fromDate: $fromDate, toDate: $toDate) {
      id
      month
      totalAmount
      totalOutstanding
      averageAmount
      averageOutstanding
    }
  }
`

export default graphql(getReport,
  {
    options: ({ fromDate, toDate }) => ({
      variables: {
        fromDate: fromDate.format('MM/DD/YYYY'),
        toDate: toDate.format('MM/DD/YYYY'),
      },
    }),
  },
)(AverageInvoice)
