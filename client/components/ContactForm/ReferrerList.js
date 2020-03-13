import React, { Fragment } from 'react'

import AsyncAutocomplete from 'components/AsyncAutocomplete'

export default ({ referrers, ...props }) => (
  <Fragment>
    <div className="form-group">
      <AsyncAutocomplete link="contact" {...props} />
    </div>
    <div className="table-responsive">
      <table className="table table-bordered">
        <thead>
          <tr>
            <th>People referred by this Contact</th>
          </tr>
        </thead>
        <tbody>
          {referrers.length > 0 ? (
            referrers.map(o => (
              <tr key={o.node.id}>
                <td>
                  <a href={`/contact/${o.node.id}`} target="_blank">
                    {o.node.fullName}
                  </a>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td>No referrers</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  </Fragment>
)
