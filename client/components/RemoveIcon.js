import React from 'react'

export default ({ value, onClick }) => {
  const _onClick = (event) => {
    event.stopPropagation()
    onClick(value)
  }
  return (
    <span>
      <i onClick={_onClick} className="fa fa-times remove" aria-hidden="true" />
      <style jsx>{`
        .remove:hover {
          color: red;
        }
        .fa {
          cursor: pointer;
        }
      `}</style>
    </span>
  )
}
