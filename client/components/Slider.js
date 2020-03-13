import React from 'react'

const SliderTrigger = ({ id, title, hasError }) => {
  const toggleSlider = () => {
    const slider = document.querySelector(`#${id}`)
    const caret = document.querySelector(`#${id}-container .arrow`)
    caret.classList.toggle('fa-caret-left')
    caret.classList.toggle('fa-caret-down')
    slider.classList.toggle('hidden-xs-up')
  }
  return (
    <button
      onClick={toggleSlider}
      type="button"
      className={`btn ${hasError ? 'btn-danger' : 'btn-success'} slider-trigger`}
    >
      {title} <i className="fa fa-caret-left arrow" aria-hidden="true" />
      <style jsx>{`
        .slider-trigger {
          width: 100%;
          text-align: left;
        }
      `}</style>
    </button>
  )
}

export default ({ id, children, title, initialState = 'closed', hasError = false }) => (
  <div>
    <div id={`${id}-container`} className="slider">
      <SliderTrigger id={id} title={title} hasError={hasError} />
      <div id={id} className={`slider-body p-3 ${initialState === 'closed' ? 'hidden-xs-up' : ''}`}>
        {children}
      </div>
    </div>
  </div>
)
