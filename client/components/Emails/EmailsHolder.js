import React from 'react'

import LineLoader from 'components/LineLoader'
import EmailDetails from './EmailDetails'

const EmailsHolder = ({ state, inbox, sentbox, emailsearch, showEmail, nextPage }) => (
  <div className="col">
    <div className="card-body p-t-0">
      <div className="card b-all shadow-none card-nooverflow">
        {!state.emailToShow ? (
          <div className="inbox-center table-responsive">
            <table
              className="table table-hover no-wrap color-table success-table"
              style={{ marginBottom: 0 }}
            >
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Sender</th>
                  <th>Recipient</th>
                  <th>Subject</th>
                </tr>
              </thead>
              {state.activeFolder === 'Inbox' && (
                <tbody>
                  {inbox.loading && (
                    <tr className="unread">
                      <td colSpan="4" style={{ padding: 0 }}>
                        <LineLoader />
                      </td>
                    </tr>
                  )}
                  {inbox.inboxEmails &&
                    inbox.inboxEmails.objects.length === 0 && (
                      <tr className="unread">
                        <td colSpan="4">
                          <p>That box is empty</p>
                        </td>
                      </tr>
                    )}
                  {inbox.inboxEmails &&
                    inbox.inboxEmails.objects.map(item => (
                      <tr
                        className="unread email-row"
                        key={item.id}
                        onClick={() => showEmail(item)}
                      >
                        <td className="hidden-xs-down">{item.date}</td>
                        <td className="hidden-xs-down">{item.sender}</td>
                        <td className="hidden-xs-down">{item.recipient}</td>
                        <td className="hidden-xs-down">{item.subject}</td>
                      </tr>
                    ))}
                </tbody>
              )}
              {state.activeFolder === 'Sent' && (
                <tbody>
                  {sentbox.loading && (
                    <tr className="unread">
                      <td colSpan="4" style={{ padding: 0 }}>
                        <LineLoader />
                      </td>
                    </tr>
                  )}
                  {sentbox.sentEmails &&
                    sentbox.sentEmails.objects.length === 0 && (
                      <tr className="unread">
                        <td colSpan="4">
                          <p>That box is empty</p>
                        </td>
                      </tr>
                    )}
                  {sentbox.sentEmails &&
                    sentbox.sentEmails.objects.map(item => (
                      <tr
                        className="unread email-row"
                        key={item.id}
                        onClick={() => showEmail(item)}
                      >
                        <td className="hidden-xs-down">{item.date}</td>
                        <td className="hidden-xs-down">{item.sender}</td>
                        <td className="hidden-xs-down">{item.recipient}</td>
                        <td className="hidden-xs-down">{item.subject}</td>
                      </tr>
                    ))}
                </tbody>
              )}
              {state.activeFolder === 'Search' && (
                <tbody>
                  {emailsearch.loading && (
                    <tr className="unread">
                      <td colSpan="4" style={{ padding: 0 }}>
                        <LineLoader />
                      </td>
                    </tr>
                  )}
                  {emailsearch.emailsSearch &&
                    emailsearch.emailsSearch.objects.length === 0 && (
                      <tr className="unread">
                        <td colSpan="4">
                          <p>Nothing suitable found</p>
                        </td>
                      </tr>
                    )}
                  {emailsearch.emailsSearch &&
                    emailsearch.emailsSearch.objects.map(item => (
                      <tr
                        className="unread email-row"
                        key={item.id}
                        onClick={() => showEmail(item)}
                      >
                        <td className="hidden-xs-down">{item.date}</td>
                        <td className="hidden-xs-down">{item.sender}</td>
                        <td className="hidden-xs-down">{item.recipient}</td>
                        <td className="hidden-xs-down">{item.subject}</td>
                      </tr>
                    ))}
                </tbody>
              )}
            </table>
            {false && (
              <div className="card-body group-centered">
                <div className="btn-group">
                  <button
                    type="button"
                    className="btn btn-secondary m-r-10 m-b-10 font-18 text-dark"
                  >
                    <i className="mdi mdi-chevron-left" />
                  </button>
                  <button
                    type="button"
                    className="btn btn-secondary active m-r-10 m-b-10 font-18 text-dark"
                  >
                    {state.range}
                  </button>
                  <button
                    type="button"
                    className="btn btn-secondary m-b-10 text-dark"
                    onClick={nextPage}
                  >
                    <i className="mdi mdi-chevron-right font-18" />
                  </button>
                </div>
              </div>
            )}
            {state.activeFolder === 'Inbox' &&
              inbox.inboxEmails &&
              inbox.inboxEmails.nextCursor && (
                <button
                  onClick={nextPage}
                  className="btn btn-success m-l-20 m-b-20 p-10 waves-effect waves-light"
                >
                  {inbox.loading ? (
                    <i className="fa fa-circle-o-notch fa-spin fa-fw" aria-hidden="true" />
                  ) : (
                    'Load more ...'
                  )}
                </button>
              )}
            {state.activeFolder === 'Sent' &&
              sentbox.sentEmails &&
              sentbox.sentEmails.nextCursor && (
                <button
                  onClick={nextPage}
                  className="btn btn-success m-l-20 m-b-20 p-10 waves-effect waves-light"
                >
                  {inbox.loading ? (
                    <i className="fa fa-circle-o-notch fa-spin fa-fw" aria-hidden="true" />
                  ) : (
                    'Load more ...'
                  )}
                </button>
              )}
          </div>
        ) : (
          <EmailDetails email={state.emailToShow} />
        )}
      </div>
    </div>
    <style jsx>{`
      .card-nooverflow {
        overflow: auto;
      }
      .group-centered {
        text-align: center;
      }
      .email-row {
        cursor: pointer;
      }
    `}</style>
  </div>
)

export default EmailsHolder
