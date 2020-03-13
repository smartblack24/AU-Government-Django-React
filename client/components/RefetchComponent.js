import React from 'react'


class RefetchComponent extends React.Component {
  componentWillReceiveProps(nextProps) {
    if (nextProps.shouldRefetch) {
      this.refetchData()
    }
  }
  refetchData = () => this.props.data.refetch()
}

export default RefetchComponent
