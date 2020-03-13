import React, { Fragment } from 'react'

export default ({ children }) => (
  <Fragment>
    <pre>{children}</pre>
    <style jsx>{`
      pre {
        box-shadow: none;
        color: #67757f;
      }
    `}</style>
  </Fragment>
)
