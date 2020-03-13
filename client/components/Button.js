import React, { Fragment } from 'react'
import PropTypes from 'prop-types'

const Button = ({ loading, className, icon, onClick, title, type, style, disabled }) => {
  let content

  if (loading && icon) {
    content = <Fragment><i className="fa fa-circle-o-notch fa-spin fa-fw" aria-hidden="true" />{title}</Fragment>
  } else if (loading && !icon) {
    content = <i className="fa fa-circle-o-notch fa-spin fa-fw" aria-hidden="true" />
  } else if (icon) {
    content = <Fragment><i className={icon} aria-hidden="true" /> {title}</Fragment>
  } else {
    content = title
  }

  return (
    <button
      onClick={onClick}
      className={className}
      disabled={loading || disabled}
      type={type}
      style={style}
    >
      {content}
    </button>
  )
}

Button.propTypes = {
  loading: PropTypes.bool,
  className: PropTypes.string,
  title: PropTypes.string,
  type: PropTypes.string,
  icon: PropTypes.string, // eslint-disable-line
  style: PropTypes.object, // eslint-disable-line
}

Button.defaultProps = {
  loading: false,
  className: '',
  type: 'button',
}

export default Button
