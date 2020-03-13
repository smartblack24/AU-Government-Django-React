import React from 'react'
import renderer from 'react-test-renderer'
import { ApolloProvider } from 'react-apollo';
import { reducer } from 'redux-form'
import { ApolloClient } from 'apollo-client';
import { mockNetworkInterfaceWithSchema } from 'apollo-test-utils';
import { createStore } from 'redux';

import schema from './mocks/schema'
import Children from '../Children'

/* eslint-disable */
describe('Contact Children tab', () => {

  const mockNetworkInterface = mockNetworkInterfaceWithSchema({ schema });
  const client = new ApolloClient({
    networkInterface: mockNetworkInterface,
  })
  const store = createStore(reducer)

  it('should render Children tab without data', () => {

    const wrapper = renderer.create(
      <ApolloProvider client={client} store={store}>
        <Children/>
      </ApolloProvider>
    )
    expect(wrapper).toMatchSnapshot()
  })

  it('should render Children tab with passed data ', () => {

    const childrenList =[
      {'id':1,
       'fullName':':LongName1'},
      {'id':2,
       'fullName':':LongName2'}
    ]

    const wrapper = renderer.create(
      <ApolloProvider client={client} store={store}>
        <Children childrenList={childrenList}/>
      </ApolloProvider>
    )
    expect(wrapper).toMatchSnapshot()
  })
});
