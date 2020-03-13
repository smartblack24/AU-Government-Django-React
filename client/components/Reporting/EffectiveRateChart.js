import React from 'react'
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

const EffectiveRateChart = ({ data }) => {
  if (data.loading) {
    return <LoadSpinner />
  }

  return (
    <ResponsiveContainer width="100%" height={400}>
      <AreaChart
        data={data.effectiveRateReports}
        margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
      >
        <defs>
          <linearGradient id="effectiveRateGradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#0018F8" stopOpacity={0.8} />
            <stop offset="95%" stopColor="#0018F8" stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Area
          type="monotone"
          dataKey="value"
          stroke="#0018F8"
          fillOpacity={1}
          fill="url(#effectiveRateGradient)"
        />
      </AreaChart>
    </ResponsiveContainer>
  )
}

export default EffectiveRateChart
