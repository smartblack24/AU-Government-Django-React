import React, { Fragment } from 'react'

export default ({ name, onClick, dataTarget, dataToggle, value }) => {
  const _onClick = (event) => {
    event.stopPropagation()
    onClick(value)
  }
  return (
    <Fragment>
      <i
        onClick={_onClick}
        role="button"
        tabIndex="-1"
        data-target={dataTarget}
        data-toggle={dataToggle}
        className={`fa fa-${name}`}
      />
      <style jsx>{`
        i {
          cursor: pointer;
        }
      `}</style>
    </Fragment>
  )
}
