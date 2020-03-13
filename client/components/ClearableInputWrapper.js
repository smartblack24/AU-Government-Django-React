import React from 'react'
import ClearableInput from 'components/ClearableInput'
import { formatDate } from 'utils'

const ClearableInputWrapper = ({ name, type, onChange, onClear, ...props }) => {
  const handleOnChange = (event) => {
    const { value } = event.target

    if (type === 'number') {
      if (!isNaN(value)) {
        // handle change only if number is entered
        // with 1 minimum symbol requried for search
        onChange(value, name, 1)
      }
    } else if (type === 'date') {
      // format input to be date
      const date = formatDate(value)
      // handle change with 10 minimum symbols requried for search
      onChange(date, name, 10)
    } else {
      onChange(value, name)
    }
  }
  const handleOnClear = () => onClear(name)

  return (
    <ClearableInput
      className="form-control"
      {...props}
      onClear={handleOnClear}
      onChange={handleOnChange}
    />
  )
}

export default ClearableInputWrapper
