import React from 'react'
import { compose, gql, graphql } from 'react-apollo'
import Router from 'next/router'

import { reduxForm, Field } from 'redux-form'

import Button from 'components/Button'
import { renderInput } from 'utils'

const resetPassword = gql`
  mutation resetPassword($uid: ID!, $newPassword: String!) {
    resetPassword(uid: $uid, newPassword: $newPassword) {
      error
    }
  }
`

class ResetPasswordForm extends React.Component {
  state = {
    isLoading: false,
  }
  onSubmit = async ({ newPassword }) => {
    this.setState({ isLoading: true })

    const { data } = await this.props.mutate({
      variables: {
        uid: this.props.uid,
        newPassword,
      },
    })

    if (data.resetPassword.error) {
      this.setState({ error: data.resetPassword.error, isLoading: false })
    } else {
      Router.push('/login')
    }
  }
  render() {
    const { handleSubmit } = this.props
    return (
      <form className="form-horizontal" onSubmit={handleSubmit(this.onSubmit)}>
        <div className="form-group ">
          <div className="col-xs-12">
            <h3>Recover Password</h3>
            <p className="text-muted">Enter new password</p>
          </div>
        </div>
        <div className="form-group ">
          <div className="col-xs-12">
            <Field
              name="newPassword"
              type="password"
              component={renderInput}
              className="form-control"
              placeholder="New password"
            />
          </div>
        </div>
        <div className="form-group ">
          <div className="col-xs-12">
            <Field
              name="confirmPassword"
              type="password"
              component={renderInput}
              className="form-control"
              placeholder="Confirm password"
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
              type="submit"
              title="Reset"
            />
          </div>
        </div>
      </form>
    )
  }
}

const validate = (values) => {
  const errors = {}

  if (!values.newPassword) {
    errors.newPassword = 'This field is required!'
  }
  if (!values.confirmPassword) {
    errors.confirmPassword = 'This field is required!'
  }
  if (values.newPassword !== values.confirmPassword) {
    errors.confirmPassword = 'Password do not match!'
  }

  return errors
}

export default compose(reduxForm({ form: 'resetPasswordForm', validate }), graphql(resetPassword))(
  ResetPasswordForm,
)
