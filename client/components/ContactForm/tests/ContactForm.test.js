import React from 'react'
import renderer from 'react-test-renderer'
import { ApolloProvider } from 'react-apollo';
import { reducer } from 'redux-form'
import { ApolloClient } from 'apollo-client';
import { mockNetworkInterfaceWithSchema } from 'apollo-test-utils';
import { createStore } from 'redux';

import schema from './mocks/schema'
import ContactForm from '../index'

const initialValues = {
  firstName: '',
  lastName: '',
  mobile: '',
  email: '',
  secondaryEmail: '',
  skype: '',
  beverage: '',
  directLine: '',
  voi: false,
  address1: '',
  address2: '',
  suburb: '',
  postCode: '',
  country: '',
  postalAddress1: '',
  postalAddress2: '',
  postalSuburb: '',
  postalPostCode: '',
  postalCountry: '',
  state: 0,
  postalState: 0,
  occupation: 1,
  isActive: true,
}

/* eslint-disable */
jest.mock('react-text-mask', () => props => <input type="text" {...{ ...props }} />)
describe('Contact Organisations tab', () => {

  const mockNetworkInterface =
    mockNetworkInterfaceWithSchema({ schema });
  const handleContactCreation = jest.fn()
  const client = new ApolloClient({
    networkInterface: mockNetworkInterface,
  })
  const store = createStore(reducer, client)


  it('should render Organisations tab without data', () => {

    const wrapper = renderer.create(
      <ApolloProvider client={client} store={store}>
        <ContactForm/>
      </ApolloProvider>
    )
    expect(wrapper).toMatchSnapshot()
  })


  it('should render Organisations tab with data', () => {

    const wrapper = renderer.create(
      <ApolloProvider client={client} store={store}>
        <ContactForm
          buttonTitle="Add contact"
          initialValues={initialValues}
          onSubmitFunc={handleContactCreation}
      />
      </ApolloProvider>
    )
    expect(wrapper).toMatchSnapshot()
  })
});
