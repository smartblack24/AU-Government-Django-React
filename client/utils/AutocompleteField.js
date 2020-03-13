import React, { Fragment } from 'react'
import Select from 'react-select'

export default ({ input, meta: { touched, error }, ...props }) => (
  <Fragment>
    <Select
      {...input}
      {...props}
      value={props.autocompleteValue}
      className={`${props.className} ${touched && error ? 'has-error' : ''}`}
    />
    {touched && error && <small style={{ color: 'red' }}>{error}</small>}
  </Fragment>
)
