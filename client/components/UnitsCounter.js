import React from 'react'
import { graphql, gql } from 'react-apollo'

import withData from 'lib/withData'
import withAuth from 'lib/withAuth'
import { userFragment } from 'fragments'
import LineLoader from 'components/LineLoader'

const getUser = gql`
  query me {
    me {
      ...User
    }
  }
${userFragment}
`

class UnitsCounter extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      user: null,
    }
  }
  render() {
    if (this.props.userData.loading) {
      return (<LineLoader />)
    }
    return (
      <div className="row mt-2 mb-3">
        <div className="col text-center">
          User Units Today: {this.props.userData.me.unitsToday}
        </div>
        <div
          className="col text-center"
          style={{ marginLeft: 'auto', borderLeft: 'solid 1px #adb0c6', borderRight: 'solid 1px #adb0c6' }}
        >
          User Units this week: {this.props.userData.me.unitsWeek}
        </div>
        <div className="col text-center" style={{ marginLeft: 'auto' }}>
          User Units this month: {this.props.userData.me.unitsMonth}
        </div>
      </div>
    )
  }
}

export default withData(
  withAuth(
    graphql(getUser, { name: 'userData', options: { fetchPolicy: 'network-only', skip: false } })(
      UnitsCounter,
    ),
  ),
)
