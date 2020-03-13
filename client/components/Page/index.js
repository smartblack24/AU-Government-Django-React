import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import { withApollo } from 'react-apollo'
import { ToastContainer } from 'react-toastify'
import $ from 'jquery'

import withData from 'lib/withData'
import * as userActions from 'actions/user'
import { setHeight } from 'utils'
import Header from './Header'
import SideBar from './SideBar'
import Footer from './Footer'

class Page extends React.PureComponent {
  componentDidMount() {
    setHeight()
    const metisMenu = require('metismenu') // eslint-disable-line
    $('#sidebarnav').metisMenu()
  }
  logout = () => {
    this.props.actions.handleLogout()
    this.props.client.resetStore()
  }
  render() {
    return (
      <div>
        <div id="main-wrapper">
          <ToastContainer />
          <Header user={this.props.user} handleLogout={this.props.actions.handleLogout} />
          <SideBar user={this.props.user} handleLogout={this.props.actions.handleLogout} />
          <div className="page-wrapper">
            <div className="container-fluid">
              <div className="row page-titles justify-content-between">
                <div className="col-md-5 col-8 align-self-center">
                  <h3 className="text-themecolor m-b-0 m-t-0">
                    {this.props.pageTitle || 'Dashboard'}
                  </h3>
                  {/* <ol className="breadcrumb">
                    <li className="breadcrumb-item">
                      <a>Home</a>
                    </li>
                    <li className="breadcrumb-item active">Dashboard</li>
                  </ol> */}
                </div>
                <div className="col col-md-auto">{this.props.renderRight}</div>
              </div>
              <div className="row">
                <div className="col-12">
                  {this.props.wrappedByCard ? (
                    <div className="card">
                      <div className="card-body">{this.props.children}</div>
                    </div>
                  ) : (
                    this.props.children
                  )}
                </div>
              </div>
            </div>
            <Footer />
          </div>
        </div>
      </div>
    )
  }
}

Page.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.arrayOf(PropTypes.node),
    PropTypes.arrayOf(PropTypes.element),
    PropTypes.node,
    PropTypes.element,
  ]).isRequired,
  user: PropTypes.shape({
    id: PropTypes.string,
    photo: PropTypes.string,
    fullName: PropTypes.string,
    firstName: PropTypes.string,
    lastName: PropTypes.string,
  }).isRequired,
  actions: PropTypes.shape({
    handleLogout: PropTypes.func.isRequired,
  }).isRequired,
  client: PropTypes.shape({
    resetStore: PropTypes.func.isRequired,
  }).isRequired,
  wrappedByCard: PropTypes.bool,
}

Page.defaultProps = {
  wrappedByCard: true,
  pageTitle: '',
}

const mapDispatchToProps = dispatch => ({
  actions: bindActionCreators(userActions, dispatch),
})

export default withData(connect(() => ({}), mapDispatchToProps)(withApollo(Page)))
