import React from 'react'
import Link from 'next/link'
import { reduxForm, Field } from 'redux-form'
import { gql, graphql } from 'react-apollo'
import Router from 'next/router'

import withData from 'lib/withData'
import { renderInput } from 'utils'
import Button from 'components/Button'
import { validate as emailPasswordValidation } from 'components/LoginForm'

class RegisterForm extends React.PureComponent {
  state = {
    loading: false,
    errors: [],
  }
  handleRegister = (data) => {
    this.setState({ loading: true })

    this.props
      .mutate({
        variables: {
          email: data.email,
          firstName: data.firstName,
          lastName: data.lastName,
          password: data.password,
        },
      })
      .then((response) => {
        if (response.data.register.errors.length > 0) {
          this.setState({ loading: false, errors: response.data.register.errors })
        } else {
          Router.push('/login')
        }
      })
  }
  render() {
    return (
      <form
        className="form-horizontal form-control-line"
        id="loginform"
        onSubmit={this.props.handleSubmit(this.handleRegister)}
      >
        <h3 className="box-title m-b-20">Sign Up</h3>
        <Field name="email" component={renderInput} type="email" placeholder="Email" />
        <Field name="firstName" component={renderInput} type="text" placeholder="First Name" />
        <Field name="lastName" component={renderInput} type="text" placeholder="Last Name" />
        <Field name="password" component={renderInput} type="password" placeholder="Password" />
        <Field
          name="confirmPassword"
          component={renderInput}
          type="password"
          placeholder="Confirm password"
        />
        <div className="form-group">
          <div className="col-md-12">
            <div className="checkbox checkbox-success p-t-0 p-l-10">
              <input className="mp-checkbox" id="checkbox-signup" type="checkbox" />
              <label htmlFor="checkbox-signup">
                I agree to all <a href="#">Terms</a>
              </label>
            </div>
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
              type="submit"
              title="Sign Up"
            />
          </div>
        </div>
        <div className="form-group m-b-0">
          <div className="col-sm-12 text-center">
            <p>
              Already have an account?
              <Link href="/login" prefetch>
                <a className="text-info m-l-5">
                  <b>Sign In</b>
                </a>
              </Link>
            </p>
          </div>
        </div>
      </form>
    )
  }
}

const registerMutation = gql`
  mutation register($email: String!, $firstName: String!, $lastName: String!, $password: String!) {
    register(email: $email, firstName: $firstName, lastName: $lastName, password: $password) {
      errors
    }
  }
`

const validate = (values) => {
  const errors = emailPasswordValidation(values)

  if (!values.confirmPassword) {
    errors.confirmPassword = 'Please confirm the password'
  } else if (values.password !== values.confirmPassword) {
    errors.password = 'Passwords must match'
    errors.confirmPassword = 'Passwords must match'
  }
  if (!values.firstName) {
    errors.firstName = 'First name is requried'
  }
  if (!values.lastName) {
    errors.lastName = 'Last name is requried'
  }

  return errors
}

export default withData(
  reduxForm({
    form: 'registerForm',
    validate,
  })(graphql(registerMutation)(RegisterForm)),
)
