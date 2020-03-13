import React, { PureComponent } from 'react'
import PropTypes from 'prop-types'
import { compose, graphql } from 'react-apollo'
import withData from 'lib/withData'
import withAuth from 'lib/withAuth'
import Page from 'components/Page'
import { getUser } from 'queries'
import UserInfoCard from 'components/UserInfoCard'
import ProfileForm from 'components/ProfileForm'
import LoadSpinner from 'components/LoadSpinner'

class MyProfile extends PureComponent {
  static propTypes = {
    user: PropTypes.shape({
      id: PropTypes.string,
      photo: PropTypes.string,
      fullName: PropTypes.string,
      firstName: PropTypes.string,
      lastName: PropTypes.string,
    }).isRequired,
  }

  render() {
    const { data, user } = this.props

    if (data.loading) {
      return (
        <Page user={user} wrappedByCard={false} pageTitle="Profile">
          <LoadSpinner />
        </Page>
      )
    }

    return (
      <Page user={user} wrappedByCard={false} pageTitle="Profile">
        <div className="row">
          <div className="col-lg-4 col-xlg-3 col-md-5">
            <UserInfoCard profile={user} />
          </div>
          <div className="col-lg-8 col-xlg-9 col-md-7">
            <ProfileForm
              initialValues={user}
              isStrange={false}
            />
          </div>
        </div>
      </Page>
    )
  }
}

export default withData(
  withAuth(
    compose(
      graphql(getUser),
    )(MyProfile),
  ),
)
