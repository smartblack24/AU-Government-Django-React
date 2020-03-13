import React from 'react'

export default ({ id, title, children, footer, size, bodyStyle = {} }) => {
  const modalSize = `modal-${size}`
  return (
    <div className="modal fade" tabIndex="-1" role="dialog" id={id}>
      <div className={`modal-dialog ${size ? modalSize : ''}`} role="document">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">{title}</h5>
            <button
              id="modalCloseButton"
              type="button"
              className="close"
              data-dismiss="modal"
              aria-label="Close"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div className="modal-body" style={bodyStyle}>
            {children}
          </div>
          {footer && <div className="modal-footer">{footer}</div>}
        </div>
      </div>
      <style jsx>{`
        .close {
          cursor: pointer;
        }
      `}</style>
    </div>
  )
}
