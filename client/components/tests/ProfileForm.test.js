import React from 'react'
import renderer from 'react-test-renderer'
import { ApolloProvider } from 'react-apollo';
import { reducer } from 'redux-form'
import { ApolloClient } from 'apollo-client';
import { createStore } from 'redux';
import ProfileForm from '../ProfileForm'

/* eslint-disable */

jest.mock('react-text-mask', () => props => <input type="text" {...{ ...props }} />)

describe('ProfileForm', () => {
  const client = new ApolloClient()
  const store = createStore(reducer)
  const initialValues = {
      id: 'VXNlclR5cGU6NTI=',
      photo: '/image.png',
      fullName: 'Admin Qwe',
      firstName: 'Adin',
      lastName: 'Qwe',
      email: 'qwe@qwe.qwe',
      salutation: 1,
      mobile: '123-12-12',
      id: "qweqqwe",
      address1: 'ad1',
      address2: 'ad2',
      stateDisplay: 'SU',
      admissionDate: '2018-11-11',
      suburb: '123',
      postCode: '123',
      country: 'co',
      location: {
        id: "qweqqwe",
        address1: 'ad1',
        address2: 'ad2',
        stateDisplay: 'SU',
        suburb: '123',
        postCode: '123',
        country: 'co',
      },
  }


  it('should render ProfileForm if stranger', () => {
    const wrapper = renderer.create(
      <ApolloProvider client={client} store={store}>
        <ProfileForm
          initialValues={initialValues}
          isStrange={true}
        />
      </ApolloProvider>
    )
    expect(wrapper).toMatchSnapshot()
  })

  it('should render ProfileForm if current user', () => {
    const wrapper = renderer.create(
      <ApolloProvider client={client} store={store}>
        <ProfileForm
          initialValues={initialValues}
          isStrange={false}
        />
      </ApolloProvider>
    )
    expect(wrapper).toMatchSnapshot()
  })
})
