import React from 'react'

export default ({ childrenList }) => (
  <div className="table-responsive">
    <table className="table table-bordered">
      <thead>
        <tr>
          <th>Children</th>
        </tr>
      </thead>
      <tbody>
        {childrenList && childrenList.length > 0 ? (
          childrenList.map(child => (
            <tr key={child.id}>
              <td>
                <a href={`/contact/${child.id}`} target="_blank">
                  {child.fullName}
                </a>
              </td>
            </tr>
          ))
        ) : (
          <tr>
            <td>No children</td>
          </tr>
        )}
      </tbody>
    </table>
  </div>
)
