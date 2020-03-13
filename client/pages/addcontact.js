import React from 'react'
import { gql, graphql } from 'react-apollo'
import { filter } from 'graphql-anywhere'
import Router from 'next/router'
import moment from 'moment'

import Page from 'components/Page'
import withData from 'lib/withData'
import withAuth from 'lib/withAuth'
import ContactForm from 'components/ContactForm'
import { contactFragment, organisationFragment } from 'fragments'
import { getContacts } from 'pages/contacts'
import doc from 'components/ContactForm/doc'

const AddContact = ({ user, mutate }) => {
  const handleContactCreation = data =>
    new Promise((resolve, reject) => {
      const organisations = data.organisations.map(({ node }) => node.id)
      mutate({
        variables: {
          contactData: {
            ...filter(doc, {
              ...data,
              location: {
                address1: data.address1,
                address2: data.address2,
                suburb: data.suburb,
                state: data.state,
                postCode: data.postCode,
                country: data.country,
              },
              postalLocation: {
                address1: data.postalAddress1,
                address2: data.postalAddress2,
                suburb: data.postalSuburb,
                state: data.postalState,
                postCode: data.postalPostCode,
                country: data.postalCountry,
              },
            }),
            organisations,
            referrerId: data.referrer && data.referrer.id,
            spouseId: data.spouse && data.spouse.id,
            motherId: data.mother && data.mother.id,
            fatherId: data.father && data.father.id,
            dateOfBirth:
              data.dateOfBirth && moment(data.dateOfBirth).format('YYYY-MM-DD'),
            dateOfDeath:
              data.dateOfDeath && moment(data.dateOfDeath).format('YYYY-MM-DD'),
          },
        },
        update: (store, { data: { createContact } }) => {
          organisations.map((organisationId) => {
            try {
              const cache = store.readFragment({
                id: `OrganisationType-${organisationId}`,
                fragmentName: 'Organisation',
                fragment: organisationFragment,
              })

              cache.contacts.edges = cache.contacts.edges
                .filter(({ node }) => node.id !== organisationId)
                .concat({ node: createContact.contact, cursor: '', __typename: 'ContactType' })

              store.writeFragment({
                id: `OrganisationType-${organisationId}`,
                fragmentName: 'Organisation',
                fragment: organisationFragment,
                data: cache,
              })
            } catch (e) {} // eslint-disable-line
          })

          try {
            const cache = store.readQuery({ query: getContacts })

            cache.contacts.edges.push(createContact.contact)

            store.writeQuery({ query: getContacts, data: cache })
          } catch (e) {} //eslint-disable-line
        },
      }).then((response) => {
        if (response.data.createContact.errors.length > 0) {
          console.log(response.data.createContact.errors)
          reject()
        } else {
          Router.push(
            `/contact?id=${response.data.createContact.contact.id}&created=true`,
            `/contact/${response.data.createContact.contact.id}`,
          )
          resolve()
        }
      })
    })
  return (
    <Page user={user} wrappedByCard={false} pageTitle="Add a contact">
      <ContactForm
        buttonTitle="Add contact"
        initialValues={{
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
        }}
        onSubmitFunc={handleContactCreation}
        wizard
      />
    </Page>
  )
}

const createContact = gql`
  mutation createContact($contactData: ContactInput) {
    createContact(contactData: $contactData) {
      errors
      contact {
        ...Contact
      }
    }
  }
  ${contactFragment}
`

export default withData(withAuth(graphql(createContact)(AddContact)))
