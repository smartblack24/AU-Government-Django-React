import React from 'react'
import { gql, graphql } from 'react-apollo'
import moment from 'moment'
import { filter } from 'graphql-anywhere'
import Router from 'next/router'
import { toast } from 'react-toastify'

import Page from 'components/Page'
import { parseCurrency } from 'utils'
import withData from 'lib/withData'
import withAuth from 'lib/withAuth'
import MatterForm from 'components/MatterForm'
import doc from 'components/MatterForm/doc'
import { matterFragment, clientFragment } from 'fragments'
import { getMatters, getNewMatterReports } from 'queries'

const AddMatter = ({ user, mutate }) => {
  const handleCreateMatter = data =>
    new Promise((resolve, reject) => {
      mutate({
        variables: {
          matterData: filter(doc, {
            ...data,
            entryType: 1,
            budget: data.budget ? parseCurrency(data.budget) : 0,
          }),
        },
        refetchQueries: [{ query: getNewMatterReports }],
        update: (store, { data: { createMatter } }) => {
          // Update matters list
          try {
            const storeData = store.readQuery({ query: getMatters })

            storeData.matters.edges.push({
              node: createMatter.matter,
              cursor: '',
              __typename: 'MatterType',
            })

            store.writeQuery({ query: getMatters, data: storeData })
          } catch (e) {} // eslint-disable-line

          // Update the client to which the matter related
          try {
            const client = store.readFragment({
              id: `ClientType-${createMatter.matter.client.id}`,
              fragment: clientFragment,
              fragmentName: 'Client',
            })

            client.mattersCount += 1

            store.writeFragment({
              id: `ClientType-${createMatter.matter.client.id}`,
              fragment: clientFragment,
              fragmentName: 'Client',
              data: client,
            })
          } catch (e) {} // eslint-disable-line
        },
      }).then((response) => {
        if (response.data.createMatter.errors.length > 0) {
          console.log(response.data.createMatter.errors)
          reject()
        } else {
          const matterId = response.data.createMatter.matter.id
          toast.success('The changes have been saved!')
          Router.push(`/matter?id=${matterId}`, `/matter/${matterId}`)
        }
      })
    })

  return (
    <Page user={user} wrappedByCard={false} pageTitle="Add a matter">
      <MatterForm
        user={user}
        wizard
        initialValues={{
          conflictStatus: '1',
          billingMethod: '1',
          billableStatus: '1',
          createdDate: moment().format(),
        }}
        buttonTitle="Create"
        onSubmit={handleCreateMatter}
      />
    </Page>
  )
}

const createMatter = gql`
  mutation createMatter($matterData: MatterInput!) {
    createMatter(matterData: $matterData) {
      errors
      matter {
        ...Matter
      }
    }
  }
  ${matterFragment}
`

export default withData(withAuth(graphql(createMatter)(AddMatter)))
