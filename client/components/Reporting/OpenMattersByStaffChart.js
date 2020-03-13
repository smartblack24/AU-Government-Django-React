import React, { Fragment } from 'react'
import { graphql, gql } from 'react-apollo'
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  LabelList,
} from 'recharts'

import LoadSpinner from 'components/LoadSpinner'

const getColorByStatus = (status) => {
  switch (status) {
    case 'Active - High (70+ units)':
      return '#fc6b57'
    case 'Active - Moderate (30-70 units)':
      return '#fed47f'
    case 'Active - Low (0-30 units)':
      return '#8dc78c'
    case 'Waiting for Internal review':
      return '#9ec3e4'
    case 'Waiting for AA review':
      return '#8dcdfd'
    case 'Waiting for external party to respond':
      return '#6483fb'
    case 'Ad hoc Work':
      return '#4268ae'
    case 'Need to be billed':
      return '#caa5fd'
    case 'Matter Closed':
      return '#FF0035'
    case 'Business Building':
      return '#FFCC0F'
    default:
      return '#000';
  }
}

const OpenMattersByStaffChart = ({ data }) => {
  const refetchData = () => data.refetch()

  if (data.loading) {
    return <LoadSpinner />
  }

  return (
    <Fragment>
      <div className="row justify-content-end">
        <div className="col col-md-auto">
          <button className="btn btn-info" onClick={refetchData}>Update</button>
        </div>
      </div>
      <ResponsiveContainer width="100%" height={600}>
        <BarChart
          data={data.openMattersByStaffReports}
          layout="vertical"
          margin={{ top: 20, right: 30, left: 100, bottom: 5 }}
        >
          <XAxis type="number" />
          <YAxis type="category" dataKey="staffMember" />
          <CartesianGrid strokeDasharray="3 3" />
          <Tooltip />
          <Legend />
          {
            data.openMattersByStaffReports[0].matterStatuses.map(status => (
              <Bar
                key={status.id}
                name={status.name}
                dataKey={item => item.matterStatuses.find(s => s.name === status.name).count}
                stackId="a"
                fill={getColorByStatus(status.name)}
                layout="vertical"
              >
                <LabelList dataKey={item => item.matterStatuses.find(s => s.name === status.name).count} position="inside" />
              </Bar>
            ))
          }
        </BarChart>
      </ResponsiveContainer>
    </Fragment>
  )
}

const getOpenMatters = gql`
  query openMattersByStaffReports {
    openMattersByStaffReports {
    id
    staffMember
    matterStatuses {
      id
      name
      count
    }
  }
}
`

export default graphql(getOpenMatters)(OpenMattersByStaffChart)
