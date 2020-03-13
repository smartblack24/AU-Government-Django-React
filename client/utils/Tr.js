import React from 'react'
import PropTypes from 'prop-types'

const Tr = (props) => {
  const _onClick = () => props.onClick(props.value)

  return (
    <tr {...props} onClick={_onClick}>
      {props.children}
      <style jsx>{`
        tr {
          cursor: pointer;
        }
      `}</style>
    </tr>
  )
}

Tr.propTypes = {
  onClick: PropTypes.func.isRequired,
}

export default Tr
