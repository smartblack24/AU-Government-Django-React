import React, { PureComponent } from 'react'
import PropTypes from 'prop-types'
import { compose, graphql } from 'react-apollo'
import withData from 'lib/withData'
import withAuth from 'lib/withAuth'
import Page from 'components/Page'
import { getProfile } from 'queries'
import UserInfoCard from 'components/UserInfoCard'
import ProfileForm from 'components/ProfileForm'
import LoadSpinner from 'components/LoadSpinner'

class Profile extends PureComponent {
  static propTypes = {
    user: PropTypes.shape({
      id: PropTypes.string,
      photo: PropTypes.string,
      fullName: PropTypes.string,
      firstName: PropTypes.string,
      lastName: PropTypes.string,
    }).isRequired,
    url: PropTypes.shape({
      query: PropTypes.shape({
        id: PropTypes.string.isRequired,
      }),
    }).isRequired,
  }

  render() {
    const { data, user, url } = this.props

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
            <UserInfoCard profile={data.user} />
          </div>
          <div className="col-lg-8 col-xlg-9 col-md-7">
            <ProfileForm
              initialValues={data.user}
              isStrange={url.query.id !== user.id}
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
      graphql(getProfile, {
        options: ({ url }) => ({
          variables: { id: url.query.id },
        }),
      }),
    )(Profile),
  ),
)
