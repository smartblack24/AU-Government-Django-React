import React from 'react'
import renderer from 'react-test-renderer'
import { ApolloProvider } from 'react-apollo';
import { reducer } from 'redux-form'
import { ApolloClient } from 'apollo-client';
import { createStore } from 'redux';
import RequireResetPasswordForm from '../RequireResetPasswordForm'

/* eslint-disable */
describe('RequireResetPasswordForm', () => {
  const client = new ApolloClient()
  const store = createStore(reducer)
  const onChange = jest.fn()
  const mutate = jest.fn()
  const onClear = jest.fn()

  it('should render RequireResetPasswordForm', () => {
    const wrapper = renderer.create(
      <ApolloProvider client={client} store={store}>
        <RequireResetPasswordForm
          mutate={mutate}
        />
      </ApolloProvider>
    )
    expect(wrapper).toMatchSnapshot()
  })
})
