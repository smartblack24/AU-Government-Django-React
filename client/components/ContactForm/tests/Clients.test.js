import React from 'react'
import renderer from 'react-test-renderer'
import { ApolloProvider } from 'react-apollo';
import { reducer } from 'redux-form'
import { graphql } from 'graphql';
import { ApolloClient } from 'apollo-client';
import { mockNetworkInterfaceWithSchema } from 'apollo-test-utils';
import { createStore } from 'redux';

import schema from './mocks/schema'
import Clients from '../Clients'

/* eslint-disable */
describe('Contact Clients tab', () => {

  const mockNetworkInterface = mockNetworkInterfaceWithSchema({ schema });

  const client = new ApolloClient({
    networkInterface: mockNetworkInterface,
  })

  const store = createStore(reducer, client)

  it('should render Clients tab without data', () => {

    const wrapper = renderer.create(
      <ApolloProvider client={client} store={store} >
        <Clients contactId={1}/>
      </ApolloProvider>
    )

    expect(wrapper).toMatchSnapshot()
  })

  it('should render Clients tab with data', () => {

    const wrapper = mount(
      <ApolloProvider client={client} store={store} >
        <Clients contactId={1}/>
      </ApolloProvider>
    )

    expect(wrapper).toMatchSnapshot()
  })

  it('should return contact data from mock server ',  () => {
    const Contact = `
    query ContactClients {
      contact(id:6){
        id
        clients {
          edges {
            cursor
            node {
              id
              name
            }
          }
        }
        secondClients {
          edges {
            cursor
            node {
              id
              name
            }
          }
        }
      }
    }
    `
    return graphql(schema, Contact).then(res => {
      expect(res.data).toMatchSnapshot();
    });
  })
});
