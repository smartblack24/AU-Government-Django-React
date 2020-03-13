import PropTypes from 'prop-types'
import React from 'react'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'

import * as userActions from 'actions/user'
import LoginForm from 'components/LoginForm'
import withData from 'lib/withData'
import withPreloader from 'lib/withPreloader'

const LoginPage = ({ actions }) => (
  <div>
    <section id="wrapper">
      <div className="login-register" style={{ backgroundColor: '#F8F8F8' }}>
        <div className="login-box card">
          <div className="card-body">
            <LoginForm handleLogin={actions.handleLogin} />
          </div>
        </div>
      </div>
    </section>
  </div>
)

LoginPage.propTypes = {
  actions: PropTypes.shape({
    handleLogin: PropTypes.func.isRequired,
  }).isRequired,
}

const mapDispatchToProps = dispatch => ({
  actions: bindActionCreators(userActions, dispatch),
})

export default withData(connect(() => ({}), mapDispatchToProps)(withPreloader(LoginPage)))
