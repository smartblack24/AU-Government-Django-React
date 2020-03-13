import React from 'react'
import moment from 'moment'
import { graphql, gql, compose } from 'react-apollo'
import swal from 'sweetalert'
import { connect } from 'react-redux'
import {
  MATTERS_LOADING_STATUS,
  TIME_ENTRIES_LOADING_STATUS,
  DISBURSEMENTS_LOADING_STATUS,
  FIXED_PRICE_ITEM_LOADING_STATUS,
} from 'constants/page'
import { setLoadingStatus } from 'actions/page'
import { formatCurrency, confirmAlert, getEntryType } from 'utils'
import Tr from 'utils/Tr'
import { invoiceFragment } from 'fragments'
import { getInvoice, getMatter } from 'queries'
import Button from 'components/Button'
import RemoveIcon from 'components/RemoveIcon'
import LineLoader from 'components/LineLoader'
import FixedPriceItemForm from 'components/InvoiceForm/FixedPriceItemForm'

const getInvoiceRecords = gql`
  query invoiceRecords($after: String, $invoiceId: String, $entryType: String, $timeRecords: Boolean) {
    invoiceRecords(first: 15, after: $after, invoiceId: $invoiceId, entryType: $entryType, timeRecords: $timeRecords) {
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
          recordType
          date
          rate
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

const fixedPriceItemInitial = {
  id: null,
  date: moment(),
  rate: 0,
  units: 0,
  gstStatus: 1,
  description: '',
  status: 1,
}

class Details extends React.Component {
  state = {
    modal: false,
    editFixedPriceItemMode: false,
    loading: false,
  }
  removeTime = async (timeKey) => {
    const [timeType, timeRecordId] = timeKey.split('-')

    const timeRecordType = timeType === 'TimeEntryType' ? 1 : 2
    const willDelete = await confirmAlert()

    if (willDelete) {
      const { data } = await this.props.deleteTime({
        variables: {
          timeRecordId,
          timeRecordType,
        },
        refetchQueries: [{ query: getMatter, variables: { id: this.props.matter.id } }],
        update: (store) => {
          const cache = store.readQuery({
            query: getInvoice,
            variables: { id: this.props.invoice.id },
          })

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
        if (timeType === 1) {
          this.props.dispatch(setLoadingStatus(TIME_ENTRIES_LOADING_STATUS, true))
        } else {
          this.props.dispatch(setLoadingStatus(DISBURSEMENTS_LOADING_STATUS, true))
        }
        this.props.dispatch(setLoadingStatus(MATTERS_LOADING_STATUS, true))
        swal({
          icon: 'success',
          text: 'The time record has been removed successfully',
        })
      }
    }
  }
  removeItem = async (itemId) => {
    const willDelete = await confirmAlert()

    if (willDelete) {
      const { data } = await this.props.deleteFixedPriceItem({ variables: { id: itemId } })

      if (data.removeFixedPriceItem.errors.length > 0) {
        console.log(data.removeFixedPriceItem.errors)
      } else {
        swal({
          icon: 'success',
          text: 'The fixed price item has been removed successfully',
        })
      }
    }
  }
  handleCreateFixedPriceItem = (fixedPriceItem) => {
    this.props.dispatch(setLoadingStatus(FIXED_PRICE_ITEM_LOADING_STATUS, true))
    if (this.state.editFixedPriceItemMode) {
      this.props.updateFixedPriceItem({ variables: { fixedPriceItem } })
    } else {
      this.props.createFixedPriceItem({
        variables: { invoiceId: this.props.invoice.id, fixedPriceItem },
      })
    }
  }
  handleEditFixedPriceItem = (fixedPriceItem) => {
    if (this.props.invoice.billingMethod === 1) {
      this.setState({
        fixedPriceItem: { ...fixedPriceItem, rate: formatCurrency(fixedPriceItem.rate) },
        modal: true,
        editFixedPriceItemMode: true,
      })
    }
  }
  handleAddItem = () => {
    this.setState({
      modal: true,
      fixedPriceItem: fixedPriceItemInitial,
      editFixedPriceItemMode: false,
    })
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
  toggleModal = () => this.setState({ modal: !this.state.modal })
  render() {
    const { data } = this.props
    const { invoiceRecords } = data
    return (
      <div>
        <div className="d-flex justify-content-between mb-sm-3">
          <div>
            {this.props.invoice.billingMethod === 1 && (
              <Button
                className="btn btn-info"
                icon="fa fa-plus"
                title="Add item"
                onClick={this.handleAddItem}
              />
            )}
          </div>
          <div>
            <strong>Portal total (incl GST):</strong>{' '}
            {formatCurrency(this.props.invoice.valueInclGst)}
          </div>
        </div>
        {this.props.dataLoading && <LineLoader />}
        <table id="mainTable" className="table table-bordered table-striped m-b-0">
          <thead>
            <tr>
              <th>Date created</th>
              <th>Entry description</th>
              <th>Actual units</th>
              <th>Units to bill</th>
              <th>Rate</th>
              <th>Amount</th>
              <th>GST</th>
              <th />
            </tr>
          </thead>
          <tbody>
            {invoiceRecords && invoiceRecords.edges.map(({ node }) => (
              <Tr
                key={`${node.__typename}-${node.id}`}
                className={`${this.props.invoice.billingMethod === 1 ? 'fixedPriceItem' : ''}`}
                value={node}
                onClick={this.handleEditFixedPriceItem}
              >
                <td style={{ width: '10%' }}>
                  {moment(node.date).format('DD/MM/YYYY')} <br />{' '}
                  <small>Type: {getEntryType(node.entryType)}</small>
                  {node.recordType === 2 && <span style={{ marginLeft: '5px' }} className="badge badge-info">sales</span>}
                </td>
                <td>
                  {node.description} <br />
                  <small>Staff Member: {node.staffMember && node.staffMember.fullName}</small>
                </td>
                <td>{node.units}</td>
                <td>{node.unitsToBill}</td>
                <td>{formatCurrency(node.rate)}</td>
                <td>{formatCurrency(node.cost)}</td>
                <td>{node.gstStatusDisplay}</td>
                {this.props.billingMethod === 2 ? (
                  <td className="delete">
                    <RemoveIcon value={`${node.__typename}-${node.id}`} onClick={this.removeTime} />
                  </td>
                ) : (
                  <td className="delete">
                    <RemoveIcon value={node.id} onClick={this.removeItem} />
                  </td>
                )}
              </Tr>
            ))}
          </tbody>
        </table>
        <div className="d-flex mb-sm-3">
          {invoiceRecords && invoiceRecords.pageInfo.hasNextPage && (
            <Button
              className="btn btn-info btn-block"
              icon="fa fa-plus"
              title="More"
              onClick={this.handleLoadMore}
            />
          )
          }
        </div>
        <FixedPriceItemForm
          toggleModal={this.toggleModal}
          modal={this.state.modal}
          initialValues={this.state.fixedPriceItem}
          handleCreateFixedPriceItem={this.handleCreateFixedPriceItem}
        />
        <style jsx>{`
          .delete {
            width: 30px;
            text-align: center;
          }
          td {
            vertical-align: middle;
          }
          .fixedPriceItem {
            cursor: pointer;
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

const removeFixedPriceItem = gql`
  mutation removeFixedPriceItem($id: ID!) {
    removeFixedPriceItem(id: $id) {
      errors
      invoice {
        ...Invoice
      }
    }
  }
  ${invoiceFragment}
`

const createFixedPriceItem = gql`
  mutation createFixedPriceItem($invoiceId: ID!, $fixedPriceItem: InvoiceFixedPriceItemInput!) {
    createFixedPriceItem(invoiceId: $invoiceId, fixedPriceItem: $fixedPriceItem) {
      invoice {
        ...Invoice
      }
    }
  }
  ${invoiceFragment}
`

const updateFixedPriceItem = gql`
  mutation updateFixedPriceItem($fixedPriceItem: InvoiceFixedPriceItemInput!) {
    updateFixedPriceItem(fixedPriceItem: $fixedPriceItem) {
      fixedPriceItem {
        id
        date
        rate
        description
        units
        gstStatus
        status
      }
      invoice {
        ...Invoice
      }
    }
  }
  ${invoiceFragment}
`

export default compose(
  graphql(getInvoiceRecords, { options: ({ invoice }) => (
    { variables: {
      invoiceId: invoice.id,
      entryType: invoice.billingMethod,
      timeRecords: false,
    } }) }),
  graphql(removeTimeRecord, { name: 'deleteTime' }),
  graphql(removeFixedPriceItem, { name: 'deleteFixedPriceItem' }),
  graphql(createFixedPriceItem, { name: 'createFixedPriceItem' }),
  graphql(updateFixedPriceItem, { name: 'updateFixedPriceItem' }),
  connect(state => ({ dataLoading: state.page.get(FIXED_PRICE_ITEM_LOADING_STATUS) })),
)(Details)
