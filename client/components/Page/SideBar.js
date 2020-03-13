import React from 'react'
import PropTypes from 'prop-types'
import { withApollo } from 'react-apollo'

import Link from 'utils/Link'
import { BACKEND_URL } from 'constants/page'

const defaultAvatar = '/static/assets/images/users/default-avatar.png'

const SideBar = ({ user, handleLogout }) => (
  <aside className="left-sidebar">
    <div className="scroll-sidebar">
      <div
        className="user-profile"
        style={{
          backgroundImage: 'url(/static/assets/images/background/user-info.jpg)',
        }}
      >
        <div className="profile-img">
          <img src={`${BACKEND_URL}${user.photo}` || defaultAvatar} alt="user" />
        </div>
        <div className="profile-text" style={{ zIndex: 1 }}>
          <a
            href="#"
            className="dropdown-toggle link u-dropdown"
            data-toggle="dropdown"
            role="button"
            aria-haspopup="true"
            aria-expanded="true"
          >
            {user.fullName} <span className="caret" />
          </a>
          <div className="dropdown-menu animated flipInY" style={{ zIndex: 100 }}>
            <Link as="/my-profile" href="/my-profile" prefetch>
              <a className="dropdown-item">
                <i className="ti-user" /> My Profile
              </a>
            </Link>
            {user.groups.length > 0 && (
              <a href={`${BACKEND_URL}/admin/`} target="_blank" className="dropdown-item">
                <i className="ti-panel" /> Admin panel
              </a>
            )}
            <div className="dropdown-divider" />
            <a role="link" tabIndex={0} className="dropdown-item" onClick={handleLogout}>
              <i className="fa fa-power-off" /> Logout
            </a>
          </div>
        </div>
      </div>
      <nav className="sidebar-nav">
        <ul id="sidebarnav">
          <li className="nav-small-cap">CONTACTS AND CLIENTS</li>
          <Link activeClassName="active" href="/contacts" prefetch>
            <li>
              <a href="#" aria-expanded="false">
                <i className="fa fa-address-book" />
                <span className="hide-menu">Contacts</span>
              </a>
            </li>
          </Link>
          <Link activeClassName="active" href="/organisations" prefetch>
            <li>
              <a href="#" aria-expanded="false">
                <i className="fa fa-building" />
                <span className="hide-menu">Organisations</span>
              </a>
            </li>
          </Link>
          <Link activeClassName="active" href="/clients" prefetch>
            <li>
              <a href="#" aria-expanded="false">
                <i className="fa fa-address-card" />
                <span className="hide-menu">Clients</span>
              </a>
            </li>
          </Link>
          <li className="nav-devider" />
          <li className="nav-small-cap">MATTERS AND BILLING</li>
          <Link activeClassName="active" href="/leads" prefetch>
            <li>
              <a href="#" aria-expanded="false">
                <i className="fa fa-list" />
                <span className="hide-menu">Leads</span>
              </a>
            </li>
          </Link>
          <Link activeClassName="active" href="/matters" prefetch>
            <li>
              <a href="#" aria-expanded="false">
                <i className="fa fa-book" />
                <span className="hide-menu">Matters</span>
              </a>
            </li>
          </Link>
          <Link activeClassName="active" href="/time-entries" prefetch>
            <li>
              <a href="#" aria-expanded="false">
                <i className="fa fa-clock-o" />
                <span className="hide-menu">Time Entry</span>
              </a>
            </li>
          </Link>
          <Link activeClassName="active" href="/disbursements" prefetch>
            <li>
              <a href="#" aria-expanded="false">
                <i className="fa fa-file-text" />
                <span className="hide-menu">Disbursement details</span>
              </a>
            </li>
          </Link>
          <li className="nav-devider" />
          <li className="nav-small-cap">INVOICING AND REPORTING</li>
          <Link activeClassName="active" href="/invoices" prefetch>
            <li>
              <a href="#" aria-expanded="false">
                <i className="fa fa-credit-card" />
                <span className="hide-menu">Invoice List</span>
              </a>
            </li>
          </Link>
          <li>
            <a className="has-arrow waves-effect waves-dark" href="#" aria-expanded="false">
              <i className="fa fa-file" />
              <span className="hide-menu">Reports </span>
            </a>
            <ul aria-expanded="false" className="collapse">
              <Link activeClassName="active" href="/my-matter-report" prefetch>
                <li>
                  <a href="#">My Matter report</a>
                </li>
              </Link>
              <Link activeClassName="active" href="/my-principal-report" prefetch>
                <li>
                  <a href="#">My Principal report</a>
                </li>
              </Link>
              <Link activeClassName="active" href="/staff-matter-report" prefetch>
                <li>
                  <a href="#">Staff Matter report</a>
                </li>
              </Link>
              <Link activeClassName="active" href="/average-invoice-report" prefetch>
                <li>
                  <a href="#">Average Invoice report</a>
                </li>
              </Link>
              <Link activeClassName="active" href="/new-matters" prefetch>
                <li>
                  <a href="#">New Matters report</a>
                </li>
              </Link>
              <Link activeClassName="active" href="/client-value-report" prefetch>
                <li>
                  <a href="#">Client Value report</a>
                </li>
              </Link>
              <Link activeClassName="active" href="/units-by-staff" prefetch>
                <li>
                  <a href="#">Units by staff report</a>
                </li>
              </Link>
              <Link activeClassName="active" href="/open-matters-by-staff" prefetch>
                <li>
                  <a href="#">Open matters by Staff</a>
                </li>
              </Link>
              <Link activeClassName="active" href="/total-of-matters" prefetch>
                <li>
                  <a href="#">Total of Matters by Staff</a>
                </li>
              </Link>
              <Link activeClassName="active" href="/effective-rate" prefetch>
                <li>
                  <a href="#">Effective Rate</a>
                </li>
              </Link>
              <Link activeClassName="active" href="/client-invoice-value" prefetch>
                <li>
                  <a href="#">Client Invoice Value</a>
                </li>
              </Link>
            </ul>
          </li>
        </ul>
      </nav>
    </div>
  </aside>
)

SideBar.propTypes = {
  user: PropTypes.shape({
    photo: PropTypes.string,
    fullName: PropTypes.string,
  }),
  handleLogout: PropTypes.func.isRequired,
}

SideBar.defaultProps = {
  user: {
    photo: '',
    fullName: '',
  },
}

export default withApollo(SideBar)
