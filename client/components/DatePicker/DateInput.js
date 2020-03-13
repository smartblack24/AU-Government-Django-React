import React from 'react'

export default class extends React.PureComponent {
  render() {
    return (
      <input
        id={this.props.id}
        className="form-control"
        onChange={() => {}}
        onClick={this.props.onClick}
        value={this.props.value}
      />
    )
  }
}
