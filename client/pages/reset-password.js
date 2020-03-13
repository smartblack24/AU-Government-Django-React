import React from 'react'
import { gql, graphql } from 'react-apollo'

import withData from 'lib/withData'

import RequireResetPasswordForm from 'components/RequireResetPasswordForm'
import ResetPasswordForm from 'components/ResetPasswordForm'
import LoadSpinner from 'components/LoadSpinner'

const checkResetPasswordToken = gql`
  mutation checkResetPasswordToken($uid: ID!, $token: String!) {
    checkResetPasswordToken(uid: $uid, token: $token) {
      error
    }
  }
`

class ResetPasswordPage extends React.Component {
  state = {
    error: null,
    isLoading: false,
  }
  componentWillMount = async () => {
    const { url, mutate } = this.props

    if (url.query.token && url.query.uid) {
      this.setState({ isLoading: true })

      const { data } = await mutate({ variables: { uid: url.query.uid, token: url.query.token } })

      if (data.checkResetPasswordToken.error) {
        this.setState({ isLoading: false, error: data.checkResetPasswordToken.error })
      } else {
        this.setState({ isLoading: false })
      }
    }
  }
  render() {
    const { url } = this.props

    if (this.state.isLoading) {
      return <LoadSpinner />
    }

    return (
      <div>
        <section id="wrapper">
          <div className="login-register" style={{ backgroundColor: '#F8F8F8' }}>
            <div className="login-box card">
              <div className="card-body">
                {this.state.error && (
                  <div className="text-center">
                    <span className="text-danger">{this.state.error}</span>
                  </div>
                )}
                {!this.state.error &&
                  (url.query.token ? (
                    <ResetPasswordForm uid={this.props.url.query.uid} />
                  ) : (
                    <RequireResetPasswordForm />
                  ))}
              </div>
            </div>
          </div>
        </section>
      </div>
    )
  }
}

export default withData(graphql(checkResetPasswordToken)(ResetPasswordPage))
