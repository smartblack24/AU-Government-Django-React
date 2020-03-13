import React from 'react'
import { graphql } from 'react-apollo'
import gql from 'graphql-tag'
import { reduxForm, Field, reset } from 'redux-form'
import { connect } from 'react-redux'
import moment from 'moment'

import { noteFragment } from 'fragments'
import { getMatter, getContact } from 'queries'
import withLoading from 'lib/withLoading'
import { renderTextarea, closeModalWindow } from 'utils'
import Button from 'components/Button'

const getMatters = gql`
  query myMatterReportMatter($after: String, $staffName: String) {
    matters(first: 15, after: $after, staffName: $staffName) {
      edges {
        cursor
        node {
          id
          name
          totalTimeValue
          totalTimeInvoiced
          wip
          billableStatusDisplay
          matterStatusDisplay
          daysOpen
          matterStatus
          budget
          description
          billingMethod
          client {
            id
            name
          }
          principal {
            id
          }
          manager {
            id
          }
          matterType {
            id
          }
          matterSubType {
            id
          }
          lastNote {
            id
            text
          }
        }
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
`

const NoteForm = ({
  matterId,
  contactId,
  mutate,
  matters,
  changeLoadStatus,
  isLoading,
  handleSubmit,
  dispatch,
  user,
}) => {
  const onSubmit = async (values) => {
    changeLoadStatus(true)
    if (matterId) {
      const response = await mutate({
        variables: {
          ...values,
          id: matterId,
          userId: user.id,
          dateTime: moment().format('YYYY-MM-DD'),
        },
        update: (store, { data: { createNote } }) => {
          if (matters) {
            const data = store.readQuery({
              query: getMatters,
              variables: { staffName: user.fullName },
            })
            data.matters.edges.find(({ node }) => node.id === matterId).node.lastNote =
              createNote.note
            store.writeQuery({
              query: getMatters,
              variables: { staffName: user.fullName },
              data,
            })
          } else {
            const data = store.readQuery({ query: getMatter, variables: { id: matterId } })
            data.matter.notes.unshift(createNote.note)
            store.writeQuery({
              query: getMatter,
              variables: { id: matterId },
              data,
            })
          }
        },
      })
      if (response.data.createNote.errors.length > 0) {
        console.log(response.data.createNote.errors)
      } else {
        dispatch(reset('notesForm'))
        closeModalWindow()
      }
    } else {
      const response = await mutate({
        variables: {
          ...values,
          id: contactId,
          userId: user.id,
          dateTime: moment().format('YYYY-MM-DD'),
        },
        update: (store, { data: { createNote } }) => {
          const data = store.readQuery({ query: getContact, variables: { id: contactId } })
          data.contact.notes.unshift(createNote.note)
          store.writeQuery({
            query: getContact,
            variables: { id: contactId },
            data,
          })
        },
      })
      if (response.data.createNote.errors.length > 0) {
        console.log(response.data.createNote.errors)
      } else {
        dispatch(reset('notesForm'))
        closeModalWindow()
      }
    }

    changeLoadStatus(false)
  }
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Field name="id" component="input" type="hidden" />
      <Field
        style={{ minHeight: 200 }}
        component={renderTextarea}
        name="text"
        placeholder="Type a note..."
        id="text"
      />
      <Button
        title="Save"
        loading={isLoading}
        className="btn btn-success pull-right"
        type="submit"
        style={{ width: 120 }}
      />
    </form>
  )
}

const createNote = gql`
  mutation createNote($id: ID!, $text: String!, $userId: ID!, $dateTime: String!) {
    createNote(id: $id, text: $text, userId: $userId, dateTime: $dateTime) {
      errors
      note {
        ...Note
      }
    }
  }
  ${noteFragment}
`

export default reduxForm({
  form: 'notesForm',
  enableReinitialize: true,
})(graphql(createNote)(withLoading(connect()(NoteForm))))
