import React from 'react'
import renderer from 'react-test-renderer'
import { ApolloProvider } from 'react-apollo';
import { reducer } from 'redux-form'
import { ApolloClient } from 'apollo-client';
import { createStore } from 'redux';
import Modal from '../Modal'

/* eslint-disable */
describe('Modal', () => {
  const client = new ApolloClient()
  const store = createStore(reducer)
  const initialValues = {
    id: 123,
    title: "Test Modal",
    children: <div>Test content</div>,
    footer: "Test Footer",
    size: 'lg',
    bodyStyle: {color: 'red'},
  }

  it('should render Modal without props', () => {
    const wrapper = renderer.create(
      <ApolloProvider client={client} store={store}>
        <Modal
        />
      </ApolloProvider>
    )
    expect(wrapper).toMatchSnapshot()
  })
  it('should render Modal with props', () => {
    const wrapper = renderer.create(
      <ApolloProvider client={client} store={store}>
        <Modal
          id={initialValues.id}
          title={initialValues.title}
          children={initialValues.children}
          footer={initialValues.footer}
          size={initialValues.size}
          bodyStyle={initialValues.bodyStyle}
        />
      </ApolloProvider>
    )
    expect(wrapper).toMatchSnapshot()
  })
})
