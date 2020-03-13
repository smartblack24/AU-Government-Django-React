import React from 'react'

import { gql, graphql } from 'react-apollo'
import Gauge from 'react-svg-gauge'
import RefetchComponent from 'components/RefetchComponent'
import LoadSpinner from 'components/LoadSpinner'

const colors = ['#ff0000', '#00ff00', '#0000ff', '#FFA500']

class GaugesList extends RefetchComponent {
  render() {
    if (this.props.data.loading) {
      return (
        <div className="row">
          <div className="col-lg-12">
            <LoadSpinner />
          </div>
        </div>
      )
    }
    return (
      <div className="row justify-content-center">
        {this.props.data.legal.edges.map(({ node }) => (
          <div className="col-auto" key={node.id}>
            <div className="card">
              <div className="card-body" style={{ padding: 0 }}>
                <Gauge
                  min={0}
                  max={10}
                  width={380}
                  topLabelStyle={{ fontSize: 20, fontWeight: 'bold' }}
                  value={node.pointer}
                  label={node.fullName}
                  key={node.id}
                  color={colors[node.id % 4]}
                  valueLabelStyle={{ display: 'none' }}
                />
              </div>
            </div>
          </div>
        ))}
      </div>
    )
  }
}

const users = gql`
  query legal {
    legal {
      edges {
        node {
          id
          fullName
          pointer
        }
      }
    }
  }
`

export default graphql(users)(GaugesList)
