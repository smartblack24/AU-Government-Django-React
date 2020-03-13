import React from 'react'
import PropTypes from 'prop-types'

class EditableTd extends React.Component {
  static propTypes = {
    fieldName: PropTypes.string.isRequired,
    onChange: PropTypes.func.isRequired,
    children: PropTypes.number.isRequired,
  }
  constructor(props) {
    super(props)

    this.state = {
      flip: false,
      value: props.children,
    }
  }
  handleOnClick = (e) => {
    this.stopPropagation(e)
    this.setState(state => ({ flip: !state.flip }))
  }
  handleOnBlur = () => {
    this.setState((state) => {
      if (state.value || state.value === 0) {
        return { flip: false }
      }

      return null
    })
  }
  handleOnChange = (event) => {
    const { value } = event.target

    if (!isNaN(value)) {
      this.setState({ value })
      this.props.onChange(this.props.id, value)
    } else {
      this.props.onChange(this.props.id, this.props.children)
    }
  }
  stopPropagation = e => e.stopPropagation()
  render() {
    /* eslint-disable */
    return (
      <td onClick={this.handleOnClick}>
        {this.state.flip ? (
          <input
            onChange={this.handleOnChange}
            onClick={this.stopPropagation}
            onBlur={this.handleOnBlur}
            name={this.props.fieldName}
            value={this.state.value}
            type="text"
          />
        ) : (
          this.props.children
        )}
      </td>
    )
  }
}

export default EditableTd
