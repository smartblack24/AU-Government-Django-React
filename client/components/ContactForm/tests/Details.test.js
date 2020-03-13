import React from 'react'
import renderer from 'react-test-renderer'
import { ApolloProvider } from 'react-apollo';
import { reducer } from 'redux-form'
import { graphql } from 'graphql';
import { ApolloClient } from 'apollo-client';
import { mockNetworkInterfaceWithSchema } from 'apollo-test-utils';
import { createStore } from 'redux';

import schema from './mocks/schema'
import Details from '../Details'

/* add apollo-test-utils */

/* eslint-disable */

jest.mock('react-text-mask', () => props => <input type="text" {...{ ...props }} />)

describe('Contact Details tab', () => {

  const onSubmit = jest.fn()
  const mutate = jest.fn()
  const mockNetworkInterface = mockNetworkInterfaceWithSchema({ schema });
  const client = new ApolloClient({
    networkInterface: mockNetworkInterface,
  })
  const store = createStore(reducer, client)

  it('should render Details tab with init data', () => {

    const wrapper = renderer.create(
      <ApolloProvider client={client} store={store}>
        <Details/>
      </ApolloProvider>
    )
    expect(wrapper).toMatchSnapshot()
  })

  it('should render Details tab with passed data ', () => {

    const wrapper = renderer.create(
      <ApolloProvider client={client} store={store} handleSubmit={onSubmit}>
        <Details mutate={mutate}/>
      </ApolloProvider>
    )
    expect(wrapper).toMatchSnapshot()
  })

  it('should return occupations data from mock server ', () => {
    const Occupations = `
      query Occupations {
        occupations {
            id
            name
        }
      }
    `
    return graphql(schema, Occupations).then(res => {
      expect(res.data).toMatchSnapshot();
    });
  })

  it('should return occupation data from mock server ', () => {
    const Occupation = `
      query Occupation {
        occupation{
          id
          name
        }
      }
    `
    return graphql(schema, Occupation).then(res => {
      expect(res.data).toMatchSnapshot();
    });
  })
});
