import React from 'react'
import { graphql, gql } from 'react-apollo'
import Router from 'next/router'
import { filter } from 'graphql-anywhere'

import Page from 'components/Page'
import withData from 'lib/withData'
import withAuth from 'lib/withAuth'
import OrganisationForm from 'components/OrganisationForm'
import { contactFragment, organisationFragment } from 'fragments'
import { getOrganisations } from 'pages/organisations'
import doc from 'components/OrganisationForm/doc'

const createOrganisationMutation = gql`
  mutation createOrganisation($organisationData: OrganisationInput!) {
    createOrganisation(organisationData: $organisationData) {
      errors
      organisation {
        ...Organisation
      }
    }
  }
  ${organisationFragment}
`

const AddOrganisation = (props) => {
  const onSubmit = data =>
    new Promise((resolve, reject) => {
      const contacts = data.contacts.map(({ node }) => node.id)
      props
        .mutate({
          variables: {
            organisationData: filter(doc, {
              ...data,
              contacts,
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
          },
          update: (store, { data: { createOrganisation } }) => {
            contacts.map((contactId) => {
              try {
                const cache = store.readFragment({
                  id: `ContactType-${contactId}`,
                  fragmentName: 'Contact',
                  fragment: contactFragment,
                })

                cache.organisations.edges = cache.organisations.edges
                  .filter(({ node }) => node.id !== createOrganisation.organisation.id)
                  .concat({
                    node: createOrganisation.organisation,
                    cursor: '',
                    __typename: 'OrganisationType',
                  })

                store.writeFragment({
                  id: `ContactType-${contactId}`,
                  fragmentName: 'Contact',
                  fragment: contactFragment,
                  data: cache,
                })
              } catch (e) {} // eslint-disable-line
            })

            try {
              const cache = store.readQuery({ query: getOrganisations })

              cache.organisations.edges.push(createOrganisation.organisation)

              store.writeQuery({ query: getOrganisations, data: cache })
            } catch (e) {} //eslint-disable-line
          },
        })
        .then((response) => {
          if (response.data.createOrganisation.errors.length > 0) {
            console.log(response.data.createOrganisation.errors)
            reject()
          } else {
            const { organisation } = response.data.createOrganisation
            Router.push(`/organisation?id=${organisation.id}`, `/organisation/${organisation.id}`)
            resolve()
          }
        })
    })
  return (
    <Page user={props.user} wrappedByCard={false} pageTitle="Add an organisation">
      <OrganisationForm
        wizard
        buttonTitle="Add organisation"
        onSubmitFunc={onSubmit}
        initialValues={{
          groupParent: {},
          groupStatus: 1,
          industry: 1,
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
          state: null,
          postalState: null,
        }}
      />
    </Page>
  )
}

export default withData(withAuth(graphql(createOrganisationMutation)(AddOrganisation)))
