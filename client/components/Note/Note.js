import React from 'react'
import { graphql, compose } from 'react-apollo'
import gql from 'graphql-tag'
import moment from 'moment'
import { reduxForm, Field, change } from 'redux-form'

import { getMatter } from 'queries'
import CustomDatePicker from 'components/DatePicker'
// import { noteFragment } from 'fragments'
import { renderTextarea } from 'utils'

class Note extends React.PureComponent {
  constructor(props) {
    super(props)

    this.state = {
      editMode: false,
      date: moment(props.note.dateTime),
    }
  }
  handleOnSave = async (values) => {
    const noteId = this.props.note.id
    const { user } = this.props
    const { data } = await this.props.updateNote({
      variables: { ...values, noteId: this.props.note.id, userId: user.id },
      update: (store, { data: { updateNote } }) => {
        const storeData = store.readQuery({
          query: getMatter,
          variables: { id: this.props.matterId },
        })
        const index = storeData.matter.notes.findIndex(note => note.id === noteId)

        if (index > -1) {
          storeData.matter.notes[index] = updateNote.note
        }
        store.writeQuery({
          query: getMatter,
          variables: { id: this.props.matterId },
          data: storeData,
        })
      },
      optimisticResponse: {
        __typename: 'Mutation',
        updateNote: {
          errors: [],
          __typename: 'UpdateNoteMutation',
          note: {
            __typename: 'NoteType',
            id: noteId,
            dateTime: values.dateTime,
            text: values.text,
            user: {
              id: user.id,
              fullName: user.fullName,
              __typename: 'UserType',
            },
          },
        },
      },
    })

    if (data.updateNote.errors.length > 0) {
      console.log(data.updateNote.errors)
    } else {
      this.setState({ editMode: false })
    }
  }
  handleDateChange = (date) => {
    this.props.dispatch(change(this.props.form, 'dateTime', date.format()))
    this.setState({ date })
  }
  enterEditMote = () => {
    this.props.dispatch(change(this.props.form, 'text', this.props.note.text))
    this.props.dispatch(change(this.props.form, 'dateTime', this.props.note.dateTime))
    this.setState({ editMode: true })
  }
  leaveEditMode = () => this.setState({ editMode: false })
  renderDateTime = () => {
    if (this.state.editMode) {
      return (
        <div>
          <Field component="input" type="hidden" name="dateTime" />
          <CustomDatePicker selected={this.state.date} onChange={this.handleDateChange} />
        </div>
      )
    }

    return (
      <div onClick={this.enterEditMote} tabIndex={0} role="button" className="col">
        {moment(this.props.note.dateTime).format('MMM Do YYYY')}
      </div>
    )
  }
  renderNoteText = () => {
    if (this.state.editMode) {
      return [
        <div key={1} className="col">
          <Field component={renderTextarea} formGroup={false} name="text" />
        </div>,
        <div key={2} className="col-sm-auto align-self-start btn-group">
          <button
            type="button"
            onClick={this.props.handleSubmit(this.handleOnSave)}
            className="btn btn-success"
          >
            <i className="fa fa-check" />
          </button>
          <button type="button" onClick={this.leaveEditMode} className="btn btn-success">
            <i className="fa fa-times" />
          </button>
        </div>,
      ]
    }

    return (
      <div onClick={this.enterEditMote} tabIndex={0} role="button" className="col">
        {this.props.note.text}
      </div>
    )
  }
  render() {
    return (
      <tr>
        <td style={{ width: 200, textAlign: 'center' }}>{this.renderDateTime()}</td>
        <td>
          <div className="row">{this.renderNoteText()}</div>
        </td>
        <td>{this.props.note.user && this.props.note.user.fullName}</td>
        <style jsx>{`
          tr:hover {
            cursor: pointer;
          }
        `}</style>
      </tr>
    )
  }
}

const updateNote = gql`
  mutation updateNote($noteId: ID!, $text: String!, $dateTime: String!, $userId: ID!) {
    updateNote(noteId: $noteId, text: $text, dateTime: $dateTime, userId: $userId) {
      errors
      note {
        id
        text
        dateTime
        user {
          id
          fullName
        }
      }
    }
  }
`

export default reduxForm({})(
  compose(graphql(updateNote, { name: 'updateNote' }))(
    Note,
  ),
)
