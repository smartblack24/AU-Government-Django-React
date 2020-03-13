import React from 'react'
import { graphql } from 'react-apollo'
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
import { getNewMatterReports } from 'queries'
import Page from 'components/Page'
import LoadSpinner from 'components/LoadSpinner'
import withData from 'lib/withData'
import withAuth from 'lib/withAuth'


const NewMatters = ({ user, data }) => {
  if (data.loading) {
    return <Page user={user}><LoadSpinner /></Page>
  }

  return (
    <Page user={user} pageTitle="New Matters by year by month">
      <ResponsiveContainer width="100%" height={600}>
        <LineChart
          data={data.mattersPerYearReports}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Legend align="right" verticalAlign="middle" wrapperStyle={{ right: -5 }} layout="vertical" />
          {data.mattersPerYearReports[0].years.map(year => (
            <Line
              key={year.name}
              type="monotone"
              name={year.name}
              dataKey={(item) => {
                const index = item.years.findIndex(y => y.name === year.name)

                return item.years[index].count
              }}
              stroke={randomColorHex()}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </Page>
  )
}

export default withData(withAuth(graphql(getNewMatterReports)(NewMatters)))
