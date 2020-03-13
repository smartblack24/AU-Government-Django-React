import React from 'react'
import { graphql, gql, compose } from 'react-apollo'
import Head from 'next/head'
import 'react-dates/initialize'
import { DateRangePicker } from 'react-dates'
import ReactTable from 'react-table'
import { Async } from 'react-select'

import { formatCurrency } from 'utils'
import { getClientValueReports } from 'queries'
import Page from 'components/Page'
import LoadSpinner from 'components/LoadSpinner'
import withData from 'lib/withData'
import withAuth from 'lib/withAuth'

const getClients = gql`
  query clientValueReportClients($name: String, $skip: Boolean!) {
    clients(name: $name) @skip(if: $skip) {
      edges {
        cursor
        node {
          id
          name
        }
      }
    }
  }
`

class ClientValueReport extends React.Component {
  state = {}
  getClients = async (input, callback) => {
    const { clientsData } = this.props
    if (input.length > 2) {
      const response = await clientsData.refetch({ skip: false, name: input })
      if (response.data.clients.edges.length) {
        // transform to react-select format
        const options = response.data.clients.edges.map(({ node }) => ({
          value: node.id,
          label: node.name,
        }))

        // callback with fetched data
        callback(null, { options })
      }
    }
  }
  handleSelectChange = clients => this.setState({ clients })
  handleRefetchData = () => {
    let clients = []
    let fromDate = null
    let toDate = null

    if (this.state.clients) {
      clients = this.state.clients.map(client => client.value)
    }

    if (this.state.fromDate) {
      fromDate = this.state.fromDate.format('YYYY-MM-DD')
    }

    if (this.state.toDate) {
      toDate = this.state.toDate.format('YYYY-MM-DD')
    }

    this.props.reportsData.refetch({ clients, fromDate, toDate, skip: false })
  }
  handleDatesChange = ({ startDate, endDate }) => {
    this.setState({ fromDate: startDate, toDate: endDate })
  }
  handleFocusChange = focusedInput => this.setState({ focusedInput })
  render() {
    let totalValue = 0
    if (!this.props.reportsData.loading) {
      const { clientValueReports } = this.props.reportsData
      if (clientValueReports) {
        totalValue = clientValueReports.reduce((x, y) => x + parseFloat(y.value), 0)
      }
    }
    return (
      <Page user={this.props.user} pageTitle="Client value report">
        <Head>
          <link rel="stylesheet" href="/static/css/react-select.min.css" />
          <link rel="stylesheet" href="/static/css/datepicker.css" />
        </Head>
        <div className="row justify-content-between mb-sm-3">
          <div className="col col-md-auto row justify-content-between">
            <div className="col">
              <Async
                multi
                autoload={false}
                cache={false}
                style={{ width: 300, height: '100%' }}
                wrapperStyle={{ height: '100%' }}
                onChange={this.handleSelectChange}
                name="form-field-name"
                placeholder="Select a Client"
                value={this.state.clients}
                loadOptions={this.getClients}
              />
            </div>
            <div className="col col-md-auto">
              <DateRangePicker
                startDate={this.state.fromDate}
                startDateId="1"
                isOutsideRange={() => false}
                endDateId="2"
                endDate={this.state.toDate}
                onDatesChange={this.handleDatesChange}
                focusedInput={this.state.focusedInput}
                onFocusChange={this.handleFocusChange}
              />
            </div>
          </div>
          <div className="col col-md-auto">
            <button onClick={this.handleRefetchData} className="btn btn-info">
              Update
            </button>
          </div>
        </div>
        {this.props.reportsData && this.props.reportsData.loading ? (
          <LoadSpinner />
        ) : (
          <ReactTable
            data={this.props.reportsData.clientValueReports}
            columns={[
              {
                Header: 'Client',
                accessor: 'name',
                headerStyle: {
                  fontWeight: 500,
                  textAlign: 'left',
                  padding: '0.75rem',
                },
                Cell: ({ original }) => <div className="with-padding">{original.name}</div>,
                Footer: (
                  <div className="with-padding">
                    <strong>Total</strong>
                  </div>
                ),
              },
              {
                Header: 'Invoice Amount ex GST',
                accessor: 'value',
                headerStyle: { fontWeight: 500, textAlign: 'left', padding: '0.75rem' },
                Cell: ({ original }) => (
                  <div className="with-padding text-right">{formatCurrency(original.value)}</div>
                ),
                Footer: <div className="with-padding text-right">{formatCurrency(totalValue)}</div>,
              },
            ]}
            defaultSorted={[
              {
                id: 'name',
                desc: false,
              },
            ]}
            defaultPageSize={15}
            pageSizeOptions={[15, 25, 50]}
            headerStyle={{ display: 'none' }}
            className="-striped -highlight"
          />
        )}
        <style jsx>{`
          tr {
            cursor: pointer;
          }
          .autocomplete-item {
            cursor: pointer;
            padding: 10px;
          }
          .with-padding {
            padding: 10px;
            cursor: pointer;
          }
        `}</style>
      </Page>
    )
  }
}

export default withData(
  withAuth(
    compose(
      graphql(getClientValueReports, {
        name: 'reportsData',
        options: { variables: { skip: true } },
      }),
      graphql(getClients, { name: 'clientsData', options: { variables: { skip: true } } }),
    )(ClientValueReport),
  ),
)
