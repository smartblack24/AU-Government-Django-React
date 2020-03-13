import React from 'react'
import Loader from 'components/Loader'

export default ComposedComponent =>
  class WithPreloader extends React.PureComponent {
    static async getInitialProps(ctx) {
      let composedInitialProps = {}
      if (ComposedComponent.getInitialProps) {
        composedInitialProps = await ComposedComponent.getInitialProps(ctx)
      }

      return { ...composedInitialProps }
    }
    componentDidMount() {
      document.querySelector('.preloader').style.display = 'none'
    }
    render() {
      return (
        <div>
          <Loader />
          <ComposedComponent {...this.props} />
        </div>
      )
    }
  }
