import React from 'react'
import PropTypes from 'prop-types'
import { reduxForm, Field } from 'redux-form'
import { gql, graphql } from 'react-apollo'
import Router from 'next/router'
import Link from 'next/link'
import Cookies from 'js-cookie'

import withData from 'lib/withData'
import { renderInput } from 'utils'
import Button from 'components/Button'

class LoginForm extends React.PureComponent {
  state = {
    loading: false,
    errors: [],
  }
  login = (data) => {
    this.setState({ loading: true })

    this.props
      .mutate({
        variables: {
          email: data.email,
          password: data.password,
        },
      })
      .then((response) => {
        if (response.data.login.errors.length > 0) {
          this.setState({ loading: false, errors: response.data.login.errors })
        } else {
          this.props.handleLogin(response.data.login.user, response.data.login.token)
          if (data.rememberMe) {
            Cookies.set('rememberMe', { email: data.email, password: data.password })
          }
          Router.push('/addtimeentry', '/time-entries/add', { swallow: true })
        }
      })
  }
  render() {
    const { handleSubmit } = this.props
    return (
      <form
        className="form-horizontal form-control-line"
        id="loginform"
        onSubmit={handleSubmit(this.login)}
      >
        <h3 className="box-title m-b-20">Sign In</h3>
        <Field component={renderInput} type="text" name="email" placeholder="Email" />
        <Field component={renderInput} type="password" name="password" placeholder="Password" />
        <div className="form-group">
          <div className="col-md-12">
            <div className="checkbox checkbox-primary pull-left p-t-0">
              <label>
                Remember me
                <Field
                  name="rememberMe"
                  component="input"
                  style={{ position: 'absolute', opacity: 1, left: 0 }}
                  type="checkbox"
                />
              </label>
            </div>
            <Link href="/reset-password">
              <a style={{ cursor: 'pointer' }} className="text-dark pull-right">
                <i className="fa fa-lock m-r-5" /> Forgot pwd?
              </a>
            </Link>
          </div>
        </div>
        {this.state.errors.length > 0 && (
          <div className="form-group error">
            <div className="col-md-12 text-center">
              <div className="help-block">
                <ul>{this.state.errors.map(error => <li key={error}>{error}</li>)}</ul>
              </div>
            </div>
          </div>
        )}
        <div className="form-group text-center m-t-20">
          <div className="col-xs-12">
            <Button
              loading={this.state.loading}
              className="btn btn-info btn-lg btn-block text-uppercase waves-effect waves-light"
              title="Log In"
              type="submit"
            />
          </div>
        </div>
        <div className="form-group m-b-0">
          <div className="col-sm-12 text-center">
            <p>
              Dont have an account?
              <Link href="/register" prefetch>
                <a className="text-info m-l-5">
                  <b>Sign Up</b>
                </a>
              </Link>
            </p>
          </div>
        </div>
      </form>
    )
  }
}

LoginForm.propTypes = {
  mutate: PropTypes.func.isRequired,
  handleSubmit: PropTypes.func.isRequired,
  handleLogin: PropTypes.func.isRequired,
}

const loginMutation = gql`
  mutation login($email: String!, $password: String!, $rememberMe: Boolean) {
    login(email: $email, password: $password, rememberMe: $rememberMe) {
      errors
      token
    }
  }
`

export const validate = (values) => {
  const errors = {}

  if (!values.email) {
    errors.email = 'Email is required'
  } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(values.email)) {
    errors.email = 'Invalid email address'
  }
  if (!values.password) {
    errors.password = 'Password is required'
  }

  return errors
}

export default withData(
  reduxForm({
    form: 'loginForm',
    validate,
  })(graphql(loginMutation)(LoginForm)),
)
