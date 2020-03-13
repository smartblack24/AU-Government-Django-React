import React, { Component } from 'react'
import { compose, gql, graphql } from 'react-apollo'
import moment from 'moment'
import 'react-dates/initialize'
import { SingleDatePicker } from 'react-dates'
import swal from 'sweetalert'
import withData from 'lib/withData'
import EmailTable from 'components/EmailTable'
import Searchable from 'components/Searchable'
import ClearableInputWrapper from 'components/ClearableInputWrapper'
import Button from 'components/Button'
import { BACKEND_URL } from 'constants/page'
import { getMails } from 'queries'
import { emailHeader, getEmailContact, getEmailDate, swalCreator } from 'utils'
import EmailDetails from './EmailDetails'
import EmailMatters from './EmailMatters'

class Emails extends Component {
  constructor(props) {
    super(props)

    this.state = {
      sender: '',
      recipient: '',
      subject: '',
      dateFrom: null,
      dateFromFocus: false,
      dateTo: null,
      dateToFocus: false,
      page: 0,
      fetchedPages: [0],
      emailId: null,
      orderBy: '-date',
      selectAll: false,
      selection: [],
      detailModalOpened: false,
      matterModalOpened: false,
    }
  }

  handleResetPages = () => {
    this.setState({ page: 0, fetchedPages: [0] })
  }

  handleChangePage = (page) => {
    this.setState({ page, fetchedPages: this.state.fetchedPages.concat(page) })
  }

  handleFilterChange = (value, name, minSymbols = 3) => {
    this.setState({ [name]: value })

    if (value && value.length >= minSymbols) {
      this.handleFilterMails({ ...this.state, [name]: value })
    } else if (!value) {
      this.handleFilterMails({ ...this.state, [name]: null })
    }
  }

  handleFilterClear = (key) => {
    this.setState({ [key]: '' })
    this.handleFilterMails({ ...this.state, [key]: null })
  }

  handleFilterMails = (params) => {
    this.handleChangePage(0)
    this.setState({ fetchedPages: [0], selectAll: false, selection: [] })

    this.props.data.refetch(params)
  }

  handleHeaderClick = (orderBy) => {
    this.setState({ orderBy })
    this.handleFilterMails({ ...this.state, orderBy })
  }

  handleDateChange = (key, value) => {
    const prevValue = this.state[key]

    if (prevValue === value) {
      return
    }

    if (prevValue && value && prevValue.format('DD/MM/YYYY') === value.format('DD/MM/YYYY')) {
      return
    }

    this.setState({ [key]: value }, () => {
      const { dateFrom, dateTo } = this.state

      this.handleFilterMails({
        ...this.state,
        dateFrom: dateFrom ? moment(dateFrom).format('DD/MM/YYYY') : null,
        dateTo: dateTo ? moment(dateTo).format('DD/MM/YYYY') : null,
      })
    })
  }

  handleFocusChange = (key, value) => {
    this.setState({ [key]: value })
  }

  handleEmailClick = (id) => {
    this.setState({ emailId: id, detailModalOpened: true })
  }

  handleToggleDetailModal = () => {
    const { detailModalOpened } = this.state
    this.setState({ detailModalOpened: !detailModalOpened })
  }

  handleUpdateSelection = (selection) => {
    this.setState({ ...selection })
  }

  handleDownloadMails = async () => {
    const { selection } = this.state
    if (selection.length === 0) {
      return
    }

    window.open(`${BACKEND_URL}/mail/export/${selection.join(',')}`, '_blank')
  }

  handleDeleteEmails = async () => {
    const { selection } = this.state

    if (!selection.length) {
      return
    }

    const res = await this.props.deleteMails({ variables: { mails: selection } })
    const { success, errors } = res.data.deleteMails

    swalCreator({ success, errors, successMsg: 'Deleted mails successfully' })

    if (success) {
      this.handleRefetch()
    }
  }

  handleToggleMatterModal = () => {
    const { matterModalOpened } = this.state
    this.setState({ matterModalOpened: !matterModalOpened })
  }

  handleHideMail = async () => {
    const { emailId } = this.state

    const willHide = await swal({ text: 'Hide this email?', icon: 'info', buttons: true })

    if (willHide) {
      const res = await this.props.hideMail({ variables: { mailId: emailId } })
      const { hideMail } = res.data

      const success = hideMail.errors.length === 0

      swalCreator({ success, errors: hideMail.errors, successMsg: 'Successfully hid this email' }).then(this.handleToggleDetailModal)

      if (success) {
        this.handleRefetch()
      }
    }
  }

  handleRefetch = () => {
    this.handleFilterMails({ ...this.state })
  }

  render() {
    const { sender, recipient, subject, page, dateFrom, dateFromFocus, dateTo, dateToFocus, fetchedPages, detailModalOpened, matterModalOpened, emailId, orderBy, selectAll, selection } = this.state
    const { data, canDeleteMails } = this.props

    return (
      <div className="row" style={{ fontSize: '0.9rem' }}>
        <div className="col col-12 mb-3">
          <div className="row">
            <div className="col">
              <ClearableInputWrapper
                placeholder="Filter by Sender"
                name="sender"
                onChange={this.handleFilterChange}
                onClear={this.handleFilterClear}
                value={sender}
              />
            </div>
            <div className="col">
              <ClearableInputWrapper
                placeholder="Filter by Recipient"
                name="recipient"
                onChange={this.handleFilterChange}
                onClear={this.handleFilterClear}
                value={recipient}
              />
            </div>
            <div className="col">
              <ClearableInputWrapper
                placeholder="Filter by Subject"
                name="subject"
                onChange={this.handleFilterChange}
                onClear={this.handleFilterClear}
                value={subject}
              />
            </div>
            <div className="col">
              <SingleDatePicker
                date={dateFrom}
                displayFormat="DD/MM/YYYY"
                focused={dateFromFocus}
                hideKeyboardShortcutsPanel
                isOutsideRange={() => false}
                numberOfMonths={1}
                placeholder="Date From (DD/MM/YYYY)"
                showClearDate
                onDateChange={date => this.handleDateChange('dateFrom', date)}
                onFocusChange={({ focused }) => this.handleFocusChange('dateFromFocus', focused)}
              />
            </div>
            <div className="col">
              <SingleDatePicker
                date={dateTo}
                displayFormat="DD/MM/YYYY"
                focused={dateToFocus}
                hideKeyboardShortcutsPanel
                isOutsideRange={() => false}
                numberOfMonths={1}
                placeholder="Date To (DD/MM/YYYY)"
                showClearDate
                onDateChange={date => this.handleDateChange('dateTo', date)}
                onFocusChange={({ focused }) => this.handleFocusChange('dateToFocus', focused)}
              />
            </div>
          </div>
        </div>
        <div className="col col-12 mb-3 text-right">
          <Button title="Update matter" className="btn btn-success" disabled={selection.length === 0} onClick={this.handleToggleMatterModal} />
          <Button title="Download emails" className="btn btn-success ml-2" disabled={selection.length === 0} onClick={this.handleDownloadMails} />
          {canDeleteMails && <Button title="Delete emails" className="btn btn-success ml-2" disabled={selection.length === 0} onClick={this.handleDeleteEmails} />}
        </div>
        <div className="col col-12">
          <div className="row">
            <Searchable
              manual
              fetchedPages={fetchedPages}
              changePage={this.handleChangePage}
              resetPages={this.handleResetPages}
              data={data}
              dataKey="mails"
              sortable={false}
              multiSort={false}
              onPageChange={this.handleChangePage}
            >
              {() => (
                <div className="col col-12">
                  <EmailTable
                    page={page}
                    selectAll={selectAll}
                    selection={selection}
                    updateSelection={this.handleUpdateSelection}
                    getTdProps={(state, rowInfo, column) => ({
                      style: { padding: '15px 0.5rem', borderRightWidth: 0, textAlign: 'left' },
                      onClick: () => {
                        if (rowInfo && column.id !== '_selector') {
                          this.handleEmailClick(rowInfo.original.id)
                        }
                      },
                    })}
                    columns={[
                      {
                        Header: emailHeader('sender', orderBy, this.handleHeaderClick),
                        id: 'sender',
                        accessor: ({ senderName, senderAddress }) => getEmailContact(senderName, senderAddress),
                        width: 200,
                        sortable: false,
                      },
                      {
                        Header: emailHeader('recipient', orderBy, this.handleHeaderClick),
                        id: 'recipient',
                        accessor: ({ recipientName, recipientAddress }) => getEmailContact(recipientName, recipientAddress),
                        width: 200,
                        sortable: false,
                      },
                      {
                        Header: emailHeader('subject', orderBy, this.handleHeaderClick),
                        id: 'subject',
                        accessor: ({ subject: mailSubject }) => `${mailSubject}`,
                        sortable: false,
                      },
                      {
                        Header: <i className="mdi mdi-pill" aria-hidden="true" />,
                        id: 'attachments',
                        accessor: ({ hasAttachments }) => (hasAttachments ? <i className="mdi mdi-pill" aria-hidden="true" /> : null),
                        width: 35,
                        sortable: false,
                      },
                      {
                        Header: emailHeader('date', orderBy, this.handleHeaderClick),
                        id: 'date',
                        accessor: ({ date }) => getEmailDate(date),
                        width: 270,
                        sortable: false,
                      },
                    ]}
                  />
                </div>
              )}
            </Searchable>
          </div>
          {detailModalOpened &&
            <EmailDetails
              isOpen={detailModalOpened}
              emailId={emailId}
              toggleModal={this.handleToggleDetailModal}
              onHide={this.handleHideMail}
              onRefetch={this.handleRefetch}
            />
          }
          {matterModalOpened &&
            <EmailMatters
              isOpen={matterModalOpened}
              selection={selection}
              toggleModal={this.handleToggleMatterModal}
            />
          }
        </div>
      </div>
    )
  }
}

const deleteMails = gql`
  mutation deleteMails($mails: [ID]!) {
    deleteMails(mails: $mails) {
      errors
      success
    }
  }
`

const hideMail = gql`
  mutation hideMail($mailId: ID!) {
    hideMail(mailId: $mailId) {
      errors
    }
  }
`

export default withData(
  compose(
    graphql(getMails, {
      options: ({ contactId, organisationId, matterId }) => ({
        notifyOnNetworkStatusChange: true,
        variables: {
          contactId,
          organisationId,
          matterId,
          page: 0,
          fetchedPages: [0],
        },
      }),
    }),
    graphql(deleteMails, { name: 'deleteMails' }),
    graphql(hideMail, { name: 'hideMail' }),
  )(Emails),
)
