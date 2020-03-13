import React, { PureComponent, Fragment } from 'react'
import PropTypes from 'prop-types'
import { Modal, ModalBody, ModalHeader } from 'reactstrap'
import { compose, gql, graphql } from 'react-apollo'
import { find } from 'lodash'
import moment from 'moment'
import swal from 'sweetalert'
import Button from 'components/Button'
import { BACKEND_URL, MEDIA_URI } from 'constants/page'
import withData from 'lib/withData'
import { MatterOptions, swalCreator } from 'utils'
import { mailFragment } from 'fragments'

class EmailDetails extends PureComponent {
  static propTypes = {
    data: PropTypes.shape({
      mail: PropTypes.object,
    }),
    isOpen: PropTypes.bool.isRequired,
    toggleModal: PropTypes.func.isRequired,
    updateMailMatter: PropTypes.func.isRequired,
    onHide: PropTypes.func.isRequired,
    onRefetch: PropTypes.func.isRequired,
  }

  handleMatterChange = async (evt) => {
    const { value: newId } = evt.target
    const { mail } = this.props.data
    const { availableMatters } = mail

    const text = newId === 'no_matter' ? 'Remove matter from this email?' : `Set ${find(availableMatters, { id: newId }).name} for this email?`

    const willUpdate = await swal({ text, icon: 'info', buttons: true })

    if (willUpdate) {
      const res = await this.props.updateMailMatter({ variables: { mailId: mail.id, matterId: newId } })
      const { updateMailMatter } = res.data

      const success = updateMailMatter.errors.length === 0

      if (success) {
        this.setState({ email: updateMailMatter.email })
      }

      const successMsg = newId === 'no_matter' ? 'Successfully removed matter from this email' : 'Successfully set matter for this email'

      swalCreator({ success, errors: updateMailMatter.errors, successMsg })

      this.props.onRefetch()
    }
  }

  render() {
    const { data, isOpen, toggleModal } = this.props

    if (data.loading) {
      return null
    }

    const { id, senderName, senderAddress, recipientName, recipientAddress, subject, date, attachments, availableMatters, matter } = data.mail

    return (
      <Modal key={3} size="lg" isOpen={isOpen} toggle={toggleModal}>
        <ModalHeader toggle={toggleModal} className="email-modal-header" style={{ padding: '1.25rem calc(1.25rem + 15px)' }}>
          {subject}
        </ModalHeader>
        <ModalBody>
          <div className="card-body">
            <h5 className="mb-3">From: {`${senderName} <${senderAddress}>`}</h5>
            <h5 className="mb-3">To: {`${recipientName} <${recipientAddress}>`}</h5>
            <h5 className="mb-3">Date: {moment(date).format('MMM Do, YYYY h:mm A')}</h5>
            <div>
              <h5 className="mb-4">
                Matter:{' '}
                {!availableMatters.length && (matter.name || 'No matter')}
                {availableMatters.length > 0 &&
                  <select className="form-control w-50" style={{ height: 'auto' }} value={matter ? matter.id : 'no_matter'} onChange={this.handleMatterChange}>
                    <MatterOptions matters={availableMatters} />
                  </select>
                }
              </h5>
            </div>
            <Button className="btn btn-danger btn-circle btn-hide-mail" icon="mdi mdi-eye-off" onClick={this.props.onHide} />
            <iframe
              className="mail-content"
              src={`${BACKEND_URL}/mail/${id}/`}
              title={id}
              position="static"
              width="100%"
            />
          </div>
          {attachments.length > 0 &&
            <Fragment>
              <div>
                <hr className="m-t-0" />
              </div>
              <div className="card-body">
                <h5><i className="fa fa-paperclip m-r-10 m-b-10" /> Attachments <span>({attachments.length})</span></h5>
                <div>
                  {attachments.map(attachment => (
                    <div key={attachment.id}>
                      <a href={`${MEDIA_URI}/${attachment.data}`} className="attachment-link" target="_blank">{attachment.name}</a>
                    </div>
                  ))}
                </div>
              </div>
            </Fragment>
          }
          <style jsx>{`
            .attachment-link {
              word-break: break-all;
              font-size: 13px;
              font-weight: 400;
              color: black;
            }
            .mail-content {
              border: 1px solid #e9ecef;
              height: 500px;
            }
          `}</style>
        </ModalBody>
      </Modal>
    )
  }
}

export const getMail = gql`
  query mail($id: ID!) {
    mail(id: $id) {
      ...Mail
    }
  }
  ${mailFragment}
`


const updateMailMatter = gql`
  mutation updateMailMatter($mailId: ID!, $matterId: String!) {
    updateMailMatter(mailId: $mailId, matterId: $matterId) {
      errors
      mail {
        ...Mail
      }
    }
  }
  ${mailFragment}
`

export default withData(
  compose(
    graphql(getMail, {
      options: ({ emailId }) => ({
        variables: { id: emailId },
        fetchPolicy: 'cache-and-network',
      }),
    }),
    graphql(updateMailMatter, { name: 'updateMailMatter' }),
  )(EmailDetails),
)
