import React from 'react'

export default ComposedComponent =>
  class WithLoading extends React.Component {
    static async getInitialProps(ctx) {
      let composedInitialProps = {}
      if (ComposedComponent.getInitialProps) {
        composedInitialProps = await ComposedComponent.getInitialProps(ctx)
      }

      return { ...composedInitialProps }
    }
    state = {
      isLoading: false,
    }
    changeLoadStatus = isLoading => this.setState({ isLoading })
    render() {
      return (
        <ComposedComponent
          {...this.props}
          changeLoadStatus={this.changeLoadStatus}
          isLoading={this.state.isLoading}
        />
      )
    }
  }
