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

class ActiveMattersChart extends RefetchComponent {
  render() {
    const { data } = this.props

    if (data.loading) {
      return <LoadSpinner />
    }

    return (
      <ResponsiveContainer width="100%" height={400}>
        <AreaChart
          data={data.activeMattersReports}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <defs>
            <linearGradient id="activeMattersGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#288ae2" stopOpacity={0.8} />
              <stop offset="95%" stopColor="#288ae2" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Area
            type="monotone"
            dataKey="count"
            stroke="#288ae2"
            fillOpacity={1}
            fill="url(#activeMattersGradient)"
          />
        </AreaChart>
      </ResponsiveContainer>
    )
  }
}

const getActiveMatters = gql`
  query activeMattersReports {
    activeMattersReports {
      id
      date
      count
    }
  }
`

export default graphql(getActiveMatters)(ActiveMattersChart)
