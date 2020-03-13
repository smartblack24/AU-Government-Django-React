import React, { Component, Fragment } from 'react'
import PropTypes from 'prop-types'
import { gql, graphql } from 'react-apollo'
import swal from 'sweetalert'
import { BACKEND_URL } from 'constants/page'
import Button from 'components/Button'

const defaultAvatar = '/static/assets/images/users/default-avatar.png'

class UserInfo extends Component {
  static propTypes = {
    profile: PropTypes.shape({
      photo: PropTypes.string,
      fullName: PropTypes.string,
      email: PropTypes.string,
    }).isRequired,
  }

  constructor(props) {
    super(props)

    this.state = {
      isSync: false,
    }
  }

  get address() {
    const { location } = this.props.profile
    return `${location.address1 && `${location.address1}, `}${location
      .address2 && `${location.address2}, `} ${location.suburb &&
      `${location.suburb}, `} ${location.stateDisplay &&
      `${location.stateDisplay}, `}${location.postCode &&
      `${location.postCode}`}${location.country &&
      `, ${location.country}`}`
  }

  handleSyncMails = async () => {
    this.setState({ isSync: true })

    const res = await this.props.syncMails()
    const { success, errors } = res.data.syncMails

    if (success) {
      swal({ title: 'Successfully started downloading emails!', text: 'This process can take some time, please check back later', icon: 'success' })
    } else {
      swal({ title: 'Something went wrong!', text: errors.join('\n'), icon: 'error' })
    }

    this.setState({ isSync: false })
  }

  render() {
    const { photo, fullName, gmail, email, mobile } = this.props.profile
    const { isSync } = this.state

    return (
      <div className="card">
        <div className="card-body">
          <center className="m-t-30">
            <img
              src={`${BACKEND_URL}${photo}` || defaultAvatar}
              alt="avatar"
              className="img-circle"
              width="150"
            />
            <h4 className="card-title m-t-10">{fullName}</h4>
            {
              gmail && <Button
                loading={isSync}
                icon="fa fa-inbox"
                className="btn btn-rounded btn-primary"
                title="Sync mails"
                onClick={this.handleSyncMails}
              />
            }
          </center>
          {gmail &&
            <div className="ribbon ribbon-info ribbon-left" style={{ left: -10 }}>
              Gmail activated
            </div>
          }
        </div>
        <div>
          <hr />
        </div>
        <div className="card-body">
          <small className="text-muted">Email address</small>
          <h6>{email}</h6>
          <small className="text-muted p-t-30 db">Phone</small>
          <h6>{mobile}</h6>
          <small className="text-muted p-t-30 db">Address</small>
          <h6>{this.address}</h6>
          {gmail &&
            <Fragment>
              <small className="text-muted p-t-30 db">Gmail</small>
              <h6>{gmail}</h6>
            </Fragment>
          }
        </div>
      </div>
    )
  }
}

const syncMails = gql`
  mutation syncMails {
    syncMails {
      success
      errors
    }
  }
`

export default graphql(syncMails, { name: 'syncMails' })(UserInfo)
