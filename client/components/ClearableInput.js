import React from 'react'
import PropTypes from 'prop-types'

const ClearableInput = ({ onClear, onChange, value, ...props }) => (
  <div style={{ position: 'relative' }}>
    <input value={value} onChange={onChange} type="text" {...props} />
    <i onClick={onClear} tabIndex="-1" role="button" className="fa fa-times clear" />
    <style jsx>{`
      .clear {
        display: ${value ? 'inline' : 'none'};
        position: absolute;
        right: 15px;
        top: 10px;
        cursor: pointer;
      }
    `}</style>
  </div>
)

ClearableInput.propTypes = {
  onClear: PropTypes.func.isRequired,
  onChange: PropTypes.func.isRequired,
  value: PropTypes.string,
}

ClearableInput.defaultProps = {
  value: '',
}

export default ClearableInput
