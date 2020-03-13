import React from 'react'
import moment from 'moment'
import { graphql, gql, compose } from 'react-apollo'
import swal from 'sweetalert'
import { connect } from 'react-redux'

// import {
//   MATTERS_LOADING_STATUS,
//   TIME_ENTRIES_LOADING_STATUS,
//   DISBURSEMENTS_LOADING_STATUS,
// } from 'constants/page'
// import { setLoadingStatus } from 'actions/page'
import { formatCurrency, getEntryType } from 'utils'
import { getInvoice, getMatter } from 'queries'
import RemoveIcon from 'components/RemoveIcon'
import Button from 'components/Button'
import LineLoader from 'components/LineLoader'

const getInvoiceRecords = gql`
  query invoiceRecords(
      $after: String,
      $invoiceId: String,
      $entryType: String,
      $timeRecords: Boolean
    ) {
    invoiceRecords(
      first: 15,
      after: $after,
      invoiceId: $invoiceId,
      entryType: $entryType,
      timeRecords: $timeRecords
    ) {
      edges {
        cursor
        node {
          id
          description
          units
          cost
          entryType
          unitsToBill
          statusDisplay
          gstStatusDisplay
          date
          rate
          recordType
          billedValue
          staffMember {
            id
            fullName
          }
        }
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
`

class TimeEntryRecords extends React.Component {
  state = {
    loading: false,
  }
  removeTime = async (timeKey) => {
    const [timeType, timeRecordId] = timeKey.split('-')

    const timeRecordType = timeType === 'TimeEntryType' ? 1 : 2

    const willDelete = await swal({
      title: 'Confirmation',
      text: 'Are you sure?',
      icon: 'warning',
      buttons: {
        cancel: true,
        confirm: {
          closeModal: false,
        },
      },
    })

    if (willDelete) {
      const { data } = await this.props.mutate({
        variables: {
          timeRecordId,
          timeRecordType,
        },
        refetchQueries: [{ query: getMatter, variables: { id: this.props.matter.id } }],
        update: (store) => {
          const cache = store.readQuery({ query: getInvoice,
            variables: { id: this.props.invoice.id } })

          cache.invoice.timeEntries.edges = cache.invoice.timeEntries.edges.filter(
            ({ node }) => node.id !== timeRecordId,
          )
          cache.invoice.disbursements.edges = cache.invoice.disbursements.edges.filter(
            ({ node }) => node.id !== timeRecordId,
          )

          store.writeQuery({
            query: getInvoice,
            variables: { id: this.props.invoice.id },
            data: cache,
          })
        },
      })

      if (data.removeTimeRecord.errors.length > 0) {
        console.log(data.removeTimeRecord.errors)
      } else {
        // if (timeType === 1) {
        //   dispatch(setLoadingStatus(TIME_ENTRIES_LOADING_STATUS, true))
        // } else {
        //   dispatch(setLoadingStatus(DISBURSEMENTS_LOADING_STATUS, true))
        // }
        // dispatch(setLoadingStatus(MATTERS_LOADING_STATUS, true))
        swal({
          icon: 'success',
          text: 'The time record has been removed successfully',
        })
      }
    }
  }
  handleLoadMore = () => {
    const { data } = this.props
    const { invoiceRecords } = this.props.data

    this.setState({ loading: true })

    data.fetchMore({
      variables: { after: invoiceRecords.pageInfo.endCursor },
      updateQuery: (previousResult, { fetchMoreResult }) => {
        if (!fetchMoreResult.invoiceRecords) {
          return previousResult
        }

        const previousEdges = previousResult.invoiceRecords.edges
        const newEdges = fetchMoreResult.invoiceRecords.edges
        const newPageInfo = fetchMoreResult.invoiceRecords.pageInfo
        const previousPageInfo = previousResult.invoiceRecords.pageInfo

        this.setState({ loading: false })

        return {
          invoiceRecords: {
            edges: [...previousEdges, ...newEdges],
            pageInfo: { ...previousPageInfo, ...newPageInfo },
            __typename: fetchMoreResult.invoiceRecords.__typename,
          },
        }
      },
    })
  }

  render() {
    const { invoice } = this.props
    const { data } = this.props
    const { invoiceRecords } = data
    if (data.loading) {
      return (
        <LineLoader />
      )
    }
    return (
      <div>
        <div className="d-flex justify-content-end mb-sm-3">
          <div>
            <strong>Time Entry Value:</strong> {formatCurrency(invoice.timeEntryValue)}
          </div>
          {this.props.invoice.billingMethod === 1 && (
            <div className="ml-sm-3">
              <div>
                <strong>Fixed Price Value:</strong> {formatCurrency(invoice.fixedPriceValue)}
              </div>
              <div>
                <strong>Entry Billed Value:</strong> {formatCurrency(invoice.totalBilledValue)}
              </div>
            </div>
          )}
        </div>
        <table id="mainTable" className="table table-bordered table-striped m-b-0">
          <thead>
            <tr>
              <th>Date created</th>
              <th>Entry description</th>
              <th>Units</th>
              <th>Rate</th>
              <th>Amount</th>
              <th>GST</th>
              {this.props.invoice.billingMethod === 1 && <th>Billed value</th>}
              <th />
            </tr>
          </thead>
          <tbody>
            {invoiceRecords && invoiceRecords.edges.map(({ node }) => (
              <tr key={`${node.__typename}-${node.id}`}>
                <td style={{ width: '10%' }}>
                  {moment(node.date).format('DD/MM/YYYY')} <br />{' '}
                  <small>Type: {getEntryType(node.entryType)}</small>
                </td>
                <td>
                  {node.description}
                  <br />
                  <small>Staff Member: {node.staffMember && node.staffMember.fullName}</small>
                  {node.recordType === 2 && <span style={{ marginLeft: '5px' }} className="badge badge-info">sales</span>}
                </td>
                <td>{node.units}</td>
                <td>{formatCurrency(node.rate)}</td>
                <td>{formatCurrency(node.cost)}</td>
                <td>{node.gstStatusDisplay}</td>
                {this.props.invoice.billingMethod === 1 && <td>
                  {formatCurrency(node.billedValue)}
                </td>}
                <td className="delete">
                  <RemoveIcon value={`${node.__typename}-${node.id}`} onClick={this.removeTime} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="d-flex mb-sm-3">
          {invoiceRecords.pageInfo.hasNextPage && (
            <Button
              className="btn btn-info btn-block"
              icon="fa fa-plus"
              title="More"
              onClick={this.handleLoadMore}
            />
          )
          }
        </div>
        <style jsx>{`
          .delete {
            width: 30px;
            text-align: center;
          }
          td {
            vertical-align: middle;
          }
        `}</style>
      </div>
    )
  }
}

const removeTimeRecord = gql`
  mutation removeTimeRecord($timeRecordId: ID!, $timeRecordType: Int!) {
    removeTimeRecord(timeRecordId: $timeRecordId, timeRecordType: $timeRecordType) {
      errors
    }
  }
`

export default compose(
  graphql(removeTimeRecord),
  graphql(getInvoiceRecords, { options: ({ invoice }) => (
    { variables: {
      invoiceId: invoice.id,
      timeRecords: true,
    } }) }),
  connect(),
)(TimeEntryRecords)
