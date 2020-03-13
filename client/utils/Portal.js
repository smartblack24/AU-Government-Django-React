import React from 'react'
import ReactDOM from 'react-dom'

export default class Portal extends React.PureComponent {
  componentWillUnmount() {
    if (this.element) {
      document.body.removeChild(this.element)
    }
    this.element = null
  }
  render() {
    if (!this.element) {
      this.element = document.createElement('div')
      document.body.appendChild(this.element)
    }
    return ReactDOM.createPortal(this.props.children, this.element)
  }
}
