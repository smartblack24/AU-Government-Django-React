import React from 'react'
import { gql, graphql } from 'react-apollo'

import Button from 'components/Button'

const sendResetPasswordEmail = gql`
  mutation sendResetPasswordEmail($email: String!) {
    sendResetPasswordEmail(email: $email) {
      error
    }
  }
`

class RequireResetPasswordForm extends React.Component {
  state = {
    value: '',
    isLoading: false,
    error: null,
    resetRequested: false,
  }
  handleChange = event => this.setState({ value: event.target.value })
  handleSubmit = async () => {
    if (/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(this.state.value)) {
      this.setState({ isLoading: true })
      const { data } = await this.props.mutate({ variables: { email: this.state.value } })

      if (data.sendResetPasswordEmail.error) {
        this.setState({ isLoading: false, error: data.sendResetPasswordEmail.error })
      } else {
        this.setState({ resetRequested: true, isLoading: false, error: '' })
      }
    } else {
      this.setState({ error: 'Invalid email!' })
    }
  }
  render() {
    if (this.state.resetRequested) {
      return <div>Check your email for further instructions!</div>
    }
    return (
      <form className="form-horizontal">
        <div className="form-group ">
          <div className="col-xs-12">
            <h3>Recover Password</h3>
            <p className="text-muted">Enter your Email and instructions will be sent to you!</p>
          </div>
        </div>
        <div className="form-group ">
          <div className="col-xs-12">
            <input
              onChange={this.handleChange}
              value={this.state.value}
              className="form-control"
              type="text"
              required=""
              placeholder="Email"
            />
          </div>
        </div>
        <div className="form-group text-center">
          {this.state.error && <span className="text-danger">{this.state.error}</span>}
        </div>
        <div className="form-group text-center m-t-20">
          <div className="col-xs-12">
            <Button
              loading={this.state.isLoading}
              onClick={this.handleSubmit}
              className="btn btn-primary btn-lg btn-block text-uppercase waves-effect waves-light"
              // type="submit"
              title="Reset"
            />
          </div>
        </div>
      </form>
    )
  }
}

export default graphql(sendResetPasswordEmail)(RequireResetPasswordForm)
