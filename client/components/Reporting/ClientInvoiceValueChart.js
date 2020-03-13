import React from 'react'
import { graphql, gql } from 'react-apollo'
import { PieChart, Pie, Cell, Legend, ResponsiveContainer } from 'recharts'

import LoadSpinner from 'components/LoadSpinner'
import { randomColorHex } from 'utils'
import RefetchComponent from 'components/RefetchComponent'

const COLORS = [
  '#4674c1',
  '#eb7d3c',
  '#a5a5a5',
  '#fdbe2e',
  '#81afd9',
  '#72ac4d',
  '#294776',
  '#b88162',
  '#636363',
]

const RADIAN = Math.PI / 180
const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }) => {
  const radius = innerRadius + (outerRadius - innerRadius) * 0.5
  const x = cx + radius * Math.cos(-midAngle * RADIAN)
  const y = cy + radius * Math.sin(-midAngle * RADIAN)

  return (
    <text x={x} y={y} fill="white" textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central">
      {`${(percent * 100).toFixed(0)}%`}
    </text>
  )
}

class ClientInvoiceValueChart extends RefetchComponent {
  render() {
    const { data } = this.props
    if (data.loading) {
      return <LoadSpinner />
    }
    return (
      <ResponsiveContainer width="100%" height={600}>
        <PieChart>
          <Legend verticalAlign="middle" align="right" layout="vertical" />
          <Pie
            data={data.clientInvoiceValue}
            dataKey="count"
            nameKey="title"
            labelLine={false}
            label={renderCustomizedLabel}
            fill={randomColorHex()}
          >
            {data.clientInvoiceValue.map((entry, index) => (
              <Cell key={entry.id} fill={COLORS[index]} />
            ))}
          </Pie>
        </PieChart>
      </ResponsiveContainer>
    )
  }
}

const clientInvoiceValueReports = gql`
  query clientInvoiceValueReports {
    clientInvoiceValue {
      id
      title
      count
    }
  }
`

export default graphql(clientInvoiceValueReports)(ClientInvoiceValueChart)
