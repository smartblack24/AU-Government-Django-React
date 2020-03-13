import React, { Fragment } from 'react'

import AsyncAutocomplete from 'components/AsyncAutocomplete'

export default ({ meta: { touched, error }, ...props }) => (
  <Fragment>
    <AsyncAutocomplete
      {...props}
      value={props.autocompleteValue}
      className={`${props.className} ${touched && error ? 'has-error' : ''}`}
    />
    {touched && error && <small style={{ color: 'red' }}>{error}</small>}
  </Fragment>
)
