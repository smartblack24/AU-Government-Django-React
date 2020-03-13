import React from 'react'
import PropTypes from 'prop-types'
import Link from 'next/link'

import { toggleSideBar } from 'utils'
import { BACKEND_URL } from 'constants/page'
import UserMenu from './UserMenu'

const Header = ({ user, handleLogout }) => (
  <header className="topbar">
    <nav className="navbar top-navbar navbar-expand-md navbar-light">
      <div className="navbar-header">
        <Link href="/" prefetch>
          <a className="navbar-brand">
            <span>
              <img src="/static/assets/images/logo-text.png" alt="homepage" className="dark-logo" />
              <img
                src={`${BACKEND_URL}/media/logo/logo.png`}
                className="light-logo"
                style={{ width: '70%' }}
                alt="homepage"
              />
            </span>
          </a>
        </Link>
      </div>
      <div className="navbar-collapse">
        <ul className="navbar-nav mr-auto mt-md-0">
          <li className="nav-item">
            <a className="nav-link nav-toggler hidden-md-up text-muted waves-effect waves-dark">
              <i className="mdi mdi-menu" />
            </a>
          </li>
          <li className="nav-item">
            <a
              onClick={toggleSideBar}
              role="button"
              tabIndex="-1"
              className="nav-link sidebartoggler hidden-sm-down text-muted waves-effect waves-dark"
            >
              <i className="ti-menu" />
            </a>
          </li>
        </ul>
        <ul className="navbar-nav my-lg-0">
          <UserMenu user={user} handleLogout={handleLogout} />
        </ul>
      </div>
    </nav>
  </header>
)

Header.propTypes = {
  user: UserMenu.propTypes.user,
  handleLogout: PropTypes.func.isRequired,
}

Header.defaultProps = {
  user: UserMenu.defaultProps.user,
}

export default Header
