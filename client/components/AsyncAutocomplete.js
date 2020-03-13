import React from 'react'
import PropTypes from 'prop-types'
import { Async } from 'react-select'

import Icon from 'components/Icon'

class AsyncAutocomplete extends React.Component {
  static propTypes = {
    fieldName: PropTypes.string.isRequired,
    placeholder: PropTypes.string,
    value: PropTypes.shape({
      id: PropTypes.string,
    }),
    accessor: PropTypes.string,
    link: PropTypes.string,
    error: PropTypes.string,
    onEdit: PropTypes.func,
    editable: PropTypes.bool,
    className: PropTypes.string,
  }
  static defaultProps = {
    placeholder: '',
    error: null,
    onEdit: undefined,
    value: null,
    editable: true,
    accessor: null,
    link: null,
    className: '',
  }
  constructor(props) {
    super(props)

    this.state = {
      editMode: !props.value || (props.value && !props.value[props.accessor]),
    }
  }
  componentWillReceiveProps(nextProps) {
    // check value field changes and change editMode flag
    if (nextProps.value && nextProps.value[nextProps.accessor]) {
      this.setState({ editMode: false })
    } else if (!nextProps.value) {
      this.setState({ editMode: true })
    } else if (nextProps.value && !nextProps.value[nextProps.accessor]) {
      this.setState({ editMode: true })
    }
  }
  handleEditIconClick = () => {
    const { onEdit } = this.props
    if (onEdit) onEdit(this.props.fieldName)
    this.setState({ editMode: true })
  }
  handleOnSelect = option => this.props.onSelect(option, this.props.fieldName)
  render() {
    const {
      getOptions,
      value,
      accessor,
      label,
      fieldName,
      error,
      placeholder,
      link,
      editable,
      className,
      ...props
    } = this.props
    const { editMode } = this.state
    return (
      <div>
        {label && <label htmlFor={fieldName}>{label}</label>}
        {editMode ? (
          <div>
            <Async
              cache={false}
              id={fieldName}
              autoload
              className={className}
              name={`${fieldName}-search-input`}
              placeholder={placeholder}
              style={error && { borderColor: 'red' }}
              onChange={this.handleOnSelect}
              loadOptions={getOptions}
              {...props}
            />
          </div>
        ) : (
          <div style={{ marginTop: 10 }}>
            {/* display selected value */}
            <strong>
              {value.id ? (
                <a href={`/${link}/${value.id}`} target="_blank">
                  {value[accessor]}
                </a>
              ) : (
                value[accessor]
              )}
            </strong>{' '}
            {editable && <Icon name="edit" onClick={this.handleEditIconClick} />}
          </div>
        )}
        {error && (
          <div>
            <span style={{ color: 'red', fontSize: '80%', fontWeight: 400 }}>{error}</span>
          </div>
        )}
      </div>
    )
  }
}

export default AsyncAutocomplete
