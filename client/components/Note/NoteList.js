import React from 'react'

import Note from './Note'

export default ({ notes, matterId, contactId, user }) => {
  if (notes.length > 0) {
    return (
      <table id="mainTable" className="table table-bordered table-striped m-b-0">
        <thead>
          <tr>
            <th>Date time</th>
            <th width="70%">Note</th>
            <th>Staff member</th>
          </tr>
        </thead>
        <tbody>
          {notes.map(note => (
            <Note
              key={note.id}
              matterId={matterId}
              contactId={contactId}
              user={user}
              form={`note${note.id}`}
              note={note}
            />
          ))}
        </tbody>
        <style jsx global>{`
          .delete {
            width: 10px;
            text-align: center;
          }
        `}</style>
      </table>
    )
  }

  return <div>No notes</div>
}
