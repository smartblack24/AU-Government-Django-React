import React from 'react'

import Modal from 'components/Modal'
import NoteForm from './NoteForm'
import NoteList from './NoteList'

export default ({ matterId, contactId, notes, user }) => [
  <Modal id="addNoteModal" title="Add a note" key={1}>
    <NoteForm matterId={matterId} contactId={contactId} user={user} />
  </Modal>,
  <div key={2} className="table-responsive">
    <div className="dt-buttons float-right col-xs-12">
      <button className="dt-button buttons-html5" data-toggle="modal" data-target="#addNoteModal">
        <span>Add</span>
      </button>
    </div>
    <NoteList notes={notes} user={user} matterId={matterId} contactId={contactId} />
    <style jsx>{`
      button {
        cursor: pointer;
      }
    `}</style>
  </div>,
]
