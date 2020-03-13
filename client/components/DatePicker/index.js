import React, { Fragment } from 'react'
import DatePicker from 'react-datepicker'
import MaskedInput from 'react-text-mask'

import stylesheet from 'styles/datepicker.css'

export default class CustomDatePicker extends React.PureComponent {
  render() {
    return (
      <Fragment>
        <style key={1} dangerouslySetInnerHTML={{ __html: stylesheet }} />
        <DatePicker
          key={2}
          className="form-control"
          customInput={
            <MaskedInput
              type="text"
              guide={false}
              mask={[/\d/, /\d/, '/', /\d/, /\d/, '/', /\d/, /\d/, /\d/, /\d/]}
            />
          }
          dateFormat="DD/MM/YYYY"
          selected={this.props.selected}
          onChange={this.props.onChange}
          {...this.props}
        />
      </Fragment>
    )
  }
}
