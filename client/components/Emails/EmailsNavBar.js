import React from 'react'

const EmailsNavBar = ({ folder, onClick, refresh, handleSearch }) => (
  <div className="col" style={{ marginRight: '-30px' }}>
    <div className="card-body inbox-panel">
      {/* <a
        href=""
        className="btn btn-danger m-b-20 p-10 btn-block waves-effect waves-light"
        onClick={e => e.preventDefault()}
      >
        Compose
      </a> */}
      <ul className="nav nav-pills">
        <li className="nav-item">
          <a
            href=""
            className={folder === 'Inbox' ? 'nav-link active' : 'nav-link'}
            onClick={e => onClick('Inbox', e)}
          >
            <i className="mdi mdi-gmail m-r-10" />Inbox
          </a>
        </li>
        <li className="nav-item">
          <a
            href=""
            className={folder === 'Sent' ? 'nav-link active' : 'nav-link'}
            onClick={e => onClick('Sent', e)}
          >
            {' '}
            <i className="mdi mdi-file-document-box m-r-10" />Sent Mail
          </a>
        </li>
        <li className="nav-item">
          <button type="button" className="btn btn-info ml-3" onClick={refresh}>
            <i className="mdi mdi-reload font-18" />
          </button>
        </li>
        <li className="nav-item ml-auto">
          <input type="text" className="form-control" onChange={handleSearch} name="searchField" placeholder="Search..." />
        </li>
      </ul>
    </div>
  </div>
)

export default EmailsNavBar
