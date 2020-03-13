import React from 'react'
import renderer from 'react-test-renderer'
import { ApolloProvider } from 'react-apollo';
import { reducer } from 'redux-form'
import { ApolloClient } from 'apollo-client';
import { createStore } from 'redux';
import ClearableInput from '../ClearableInput'

/* eslint-disable */
describe('ClearableInput', () => {
  const client = new ApolloClient()
  const store = createStore(reducer)
  const onChange = jest.fn()
  const onClear = jest.fn()

  it('should render ClearableInput', () => {
    const wrapper = renderer.create(
      <ApolloProvider client={client} store={store}>
        <ClearableInput
          onClear={onClear}
          onChange={onChange}
          value="qwe"
        />
      </ApolloProvider>
    )
    expect(wrapper).toMatchSnapshot()
  })

  it('should render ClearableInput without value', () => {
    const wrapper = renderer.create(
      <ApolloProvider client={client} store={store}>
        <ClearableInput
          onClear={onClear}
          onChange={onChange}
          />
      </ApolloProvider>
    )
    expect(wrapper).toMatchSnapshot()
  })
})
