import React from 'react'
import renderer from 'react-test-renderer'
import { ApolloProvider } from 'react-apollo';
import { reducer } from 'redux-form'
import { ApolloClient } from 'apollo-client';
import { createStore } from 'redux';
import UserInfoCard from '../UserInfoCard'

/* eslint-disable */
describe('UserInfoCard card', () => {
  const client = new ApolloClient()
  const store = createStore(reducer)
  const profile = {
      id: 'VXNlclR5cGU6NTI=',
      photo: '/image.png',
      fullName: 'Admin Qwe',
      firstName: 'Adin',
      lastName: 'Qwe',
      email: 'qwe@qwe.qwe',
      mobile: '123-12-12',
      location: {
        __typename: "LocationType",
        id: "qweqqwe",
        address1: 'ad1',
        address2: 'ad2',
        stateDisplay: 'SU',
        suburb: '123',
        postCode: '123',
        country: 'co',
      },
  }


  it('should render UserInfoCard', () => {

    const wrapper = renderer.create(
      <ApolloProvider client={client} store={store}>
        <UserInfoCard profile={profile} />
      </ApolloProvider>
    )
    expect(wrapper).toMatchSnapshot()
  })
})
