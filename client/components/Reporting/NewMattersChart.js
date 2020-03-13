import React from 'react'
import { graphql, gql } from 'react-apollo'
import {
  AreaChart,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Area,
  ResponsiveContainer,
  linearGradient,
} from 'recharts'

import LoadSpinner from 'components/LoadSpinner'
import RefetchComponent from 'components/RefetchComponent'

class NewMattersChart extends RefetchComponent {
  render() {
    const { data } = this.props
    if (data.loading) {
      return <LoadSpinner />
    }

    return (
      <ResponsiveContainer width="100%" height={400}>
        <AreaChart
          data={data.newMattersReports}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <defs>
            <linearGradient id="newMattersGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="green" stopOpacity={0.8} />
              <stop offset="95%" stopColor="green" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" domain={['dataMin', 'dataMax']} />
          <YAxis />
          <Tooltip />
          <Area type="monotone" dataKey="count" stroke="green" fillOpacity={1} fill="url(#newMattersGradient)" />
        </AreaChart>
      </ResponsiveContainer>
    )
  }
}

const getNewMatters = gql`
  query newMattersReports {
    newMattersReports {
      id
      date
      count
    }
  }
`

export default graphql(getNewMatters)(NewMattersChart)
