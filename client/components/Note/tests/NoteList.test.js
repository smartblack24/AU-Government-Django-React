import React from 'react'
import renderer from 'react-test-renderer'
import { ApolloProvider } from 'react-apollo';
import { reducer } from 'redux-form'
import { ApolloClient } from 'apollo-client';
import { createStore } from 'redux';

import NoteList from '../NoteList'

/* eslint-disable */
describe('Note', () => {

  const client = new ApolloClient({})
  const store = createStore(reducer)

  it('should render Note with full props', () => {
    const wrapper = renderer.create(
      <ApolloProvider client={client} store={store}>
        <NoteList
          matterId={123123}
          contactId={12312}
          user={{
            fullName: 'Test Test',
          }}
          notes={[
            0: {
              __typename: "NoteType",
              id: '1',
              key: '1',
              dateTime: '2018-10-02T14:30:00+00:00',
              text: 'Test note',
              user: {
                fullName: 'Admin Test',
              },
            },
            1: {
              __typename: "NoteType",
              id: '2',
              key: '2',
              dateTime: '2018-11-02T14:30:00+00:00',
              text: 'Test second note',
              user: {
                fullName: 'Admin Test',
              },
            },
          ]}
        />
      </ApolloProvider>
    )
    expect(wrapper).toMatchSnapshot()
  })

  it('should render Note without data', () => {
    const wrapper = renderer.create(
      <ApolloProvider client={client} store={store}>
        <NoteList
          matterId={123123}
          contactId={12312}
          user={{
            fullName: 'Test Test',
          }}
          notes={[]}
        />
      </ApolloProvider>
    )
    expect(wrapper).toMatchSnapshot()
  })
})
