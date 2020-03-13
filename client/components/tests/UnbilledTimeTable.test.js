import React from 'react'
import renderer from 'react-test-renderer'
import { ApolloProvider } from 'react-apollo'
import { reducer } from 'redux-form'
import { ApolloClient } from 'apollo-client'
import { createStore } from 'redux'
import moment from 'moment'
import UnbilledTimeTable from '../UnbilledTimeTable'

/* eslint-disable */
describe('UnbilledTimeTable', () => {
  const client = new ApolloClient()
  const store = createStore(reducer)
  const unbilledTime = {
    unbilledTime: [
      {
        __typename: "TymeEntryType",
        id: 12312,
        date: moment(),
        staffMember: {
          fullName: 'qwe qwe',
        },
        statusDisplay: 'Non billable',
        units: 2,
        unitsToBill: 12,
        rate: 12,
        cost: 12,
      },
      {
        __typename: "TymeEntryType",
        id: 12123312,
        date: moment(),
        staffMember: {
          fullName: 'qwe qwe',
        },
        statusDisplay: 'Billable',
        units: 2,
        unitsToBill: 12,
        rate: 12,
        cost: 12,
      }
  ]
  }

  it('should render UnbilledTimeTable', () => {
    const wrapper = renderer.create(
      <ApolloProvider client={client} store={store}>
        <UnbilledTimeTable
          unbilledTime={unbilledTime.unbilledTime}
        />
      </ApolloProvider>
    )
    expect(wrapper).toMatchSnapshot()
  })
})
