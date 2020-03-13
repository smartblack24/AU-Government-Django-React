import React from 'react'
import renderer from 'react-test-renderer'
import { ApolloProvider } from 'react-apollo';
import { reducer } from 'redux-form'
import { ApolloClient } from 'apollo-client';
import { createStore } from 'redux';

import Note from '../Note'

/* eslint-disable */
describe('Note', () => {

  const client = new ApolloClient({})
  const store = createStore(reducer)


  it('should render Note with some props', () => {
    const wrapper = renderer.create(
      <ApolloProvider client={client} store={store}>
        <Note
          note={{
            dateTime: '2018-10-02T14:30:00+00:00',
          }}
          form='note1'
        />
      </ApolloProvider>
    )
    expect(wrapper).toMatchSnapshot()
  })

  it('should render Note with full props', () => {
    const wrapper = renderer.create(
      <ApolloProvider client={client} store={store}>
        <Note
          key={1}
          matterId={123123}
          contactId={12312}
          note={{
            dateTime: '2018-10-02T14:30:00+00:00',
            text: 'Test note',
            user: {
              fullName: 'Admin Test',
            },
          }}
          form="note1"
        />
      </ApolloProvider>
    )
    expect(wrapper).toMatchSnapshot()
  })
})
