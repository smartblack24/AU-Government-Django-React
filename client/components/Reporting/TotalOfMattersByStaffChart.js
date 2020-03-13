import React from 'react'
import {
  LineChart,
  CartesianGrid,
  XAxis,
  Legend,
  YAxis,
  Line,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'

import { randomColorHex } from 'utils'
import LoadSpinner from 'components/LoadSpinner'


const TotalOfMattersByStaff = ({ data }) => {
  if (data.loading) {
    return <LoadSpinner />
  }

  return (
    <ResponsiveContainer width="100%" height={600}>
      <LineChart
        data={data.totalOfMattersByStaffReports}
        margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Legend align="right" verticalAlign="middle" wrapperStyle={{ right: -5 }} layout="vertical" />
        {data.totalOfMattersByStaffReports[0].staffMembers.map(staffMember => (
          <Line
            key={staffMember.id}
            type="monotone"
            name={staffMember.name}
            dataKey={item => item.staffMembers.find(m => m.name === staffMember.name).count}
            stroke={randomColorHex()}
          />
        ))}
      </LineChart>
    </ResponsiveContainer>
  )
}


export default TotalOfMattersByStaff
