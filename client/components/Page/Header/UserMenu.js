import React from 'react'
import PropTypes from 'prop-types'
import Link from 'next/link'

import { BACKEND_URL } from 'constants/page'

const defaultAvatar = '/static/assets/images/users/default-avatar.png'

const UserMenu = ({ user, handleLogout }) => (
  <li className="nav-item dropdown">
    <a
      className="nav-link dropdown-toggle text-muted waves-effect waves-dark"
      href=""
      data-toggle="dropdown"
      aria-haspopup="true"
      aria-expanded="false"
    >
      <img
        src={`${BACKEND_URL}${user.photo}` || defaultAvatar}
        alt="user"
        className="profile-pic"
      />
    </a>
    <div className="dropdown-menu dropdown-menu-right scale-up">
      <ul className="dropdown-user">
        <li>
          <div className="dw-user-box">
            <div className="u-img">
              <img src={`${BACKEND_URL}${user.photo}` || defaultAvatar} alt="user" />
            </div>
            <div className="u-text">
              <h4>{user.fullName}</h4>
              <p className="text-muted">{user.email}</p>
              <Link as="/my-profile" href="/my-profile" prefetch>
                <a className="btn btn-rounded btn-danger btn-sm">View Profile</a>
              </Link>
            </div>
          </div>
        </li>
        <li role="separator" className="divider" />
        <li>
          <Link as="/my-profile" href="/my-profile" prefetch>
            <a>
              <i className="ti-user" /> My Profile
            </a>
          </Link>
        </li>
        {user.groups.length > 0 && (
          <li>
            <a href={`${BACKEND_URL}/admin/`} target="_blank">
              <i className="ti-panel" /> Admin panel
            </a>
          </li>
        )}
        <li role="separator" className="divider" />
        <li>
          <a href="#" onClick={handleLogout}>
            <i className="fa fa-power-off" /> Logout
          </a>
        </li>
      </ul>
    </div>
  </li>
)

UserMenu.propTypes = {
  user: PropTypes.shape({
    photo: PropTypes.string,
    fullName: PropTypes.string,
  }),
  handleLogout: PropTypes.func.isRequired,
}

UserMenu.defaultProps = {
  user: {
    photo: '',
    fullName: '',
  },
}

export default UserMenu
