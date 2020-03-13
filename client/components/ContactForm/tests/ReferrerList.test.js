import React from 'react'
import renderer from 'react-test-renderer'
import { ApolloProvider } from 'react-apollo';
import { reducer } from 'redux-form'
import { ApolloClient } from 'apollo-client';
import { mockNetworkInterfaceWithSchema } from 'apollo-test-utils';
import { createStore } from 'redux';

import schema from './mocks/schema'
import ReferrerList from '../ReferrerList'

/* eslint-disable */
describe('Contact ReferrerList tab', () => {

  const mockNetworkInterface = mockNetworkInterfaceWithSchema({ schema });
  const client = new ApolloClient({
    networkInterface: mockNetworkInterface,
  })
  const store = createStore(reducer)

  it('should render ReferrerList tab without data', () => {

    const wrapper = renderer.create(
      <ApolloProvider client={client} store={store}>
        <ReferrerList
          label="This contact was introduced by"
          fieldName="referrer"
          onEdit={jest.fn()}
          onSelect={jest.fn()}
          getOptions={jest.fn()}
          value={{ name: 'text' }}
          accessor="fullName"
          placeholder="Search for contact"
          referrers
        />
      </ApolloProvider>
    )
    expect(wrapper).toMatchSnapshot()
  })

});
