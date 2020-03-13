import React from 'react'
import PropTypes from 'prop-types'
import ImmutablePropTypes from 'react-immutable-proptypes'
import { graphql } from 'react-apollo'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'

import * as userActions from 'actions/user'
import { cookies } from 'utils'
import Loader from 'components/Loader'
import { getUser } from 'queries'

export default (ComposedComponent) => {
  class WithAuth extends React.PureComponent {
    static async getInitialProps(ctx) {
      if (!process.browser) {
        if (!cookies(ctx.req.headers).token) {
          ctx.res.redirect('/login')
          return {}
        }
      }

      let composedInitialProps = {}
      if (ComposedComponent.getInitialProps) {
        composedInitialProps = await ComposedComponent.getInitialProps(ctx)
      }

      return { ...composedInitialProps }
    }
    componentDidMount() {
      // For handle login with SSR
      if (this.props.data.me && !this.props.user.get('isAuthenticated')) {
        this.props.handleLogin(this.props.data.me)
      }
    }
    componentWillReceiveProps(nextProps) {
      // For handle login after redirect from somewhere
      if (nextProps.data.me && !nextProps.user.get('isAuthenticated')) {
        this.props.handleLogin(nextProps.data.me)
      }
    }
    render() {
      if (this.props.data.loading) {
        return <Loader />
      } else if (this.props.data.error) {
        return <div>Error</div>
      }

      return <ComposedComponent user={this.props.data.me} url={this.props.url} />
    }
  }

  WithAuth.propTypes = {
    data: PropTypes.shape({
      loading: PropTypes.bool.isRequired,
      me: PropTypes.shape({
        id: PropTypes.string.isRequired,
        firstName: PropTypes.string.isRequired,
        lastName: PropTypes.string.isRequired,
        fullName: PropTypes.string.isRequired,
        email: PropTypes.string.isRequired,
      }),
      error: PropTypes.string,
    }).isRequired,
    user: ImmutablePropTypes.mapContains({
      isAuthenticated: PropTypes.bool.isRequired,
    }).isRequired,
    handleLogin: PropTypes.func.isRequired,
    url: PropTypes.object, // eslint-disable-line
  }

  const mapStateToProps = state => ({
    user: state.user,
  })

  const mapDispatchToProps = dispatch => ({
    handleLogin: bindActionCreators(userActions.handleLogin, dispatch),
  })

  return connect(mapStateToProps, mapDispatchToProps)(graphql(getUser)(WithAuth))
}
