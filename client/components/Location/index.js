import React from 'react'
import { Field, change } from 'redux-form'
import { connect } from 'react-redux'

import { capitalize } from 'utils'
import withData from 'lib/withData'
import LocationInputs from './LocationInputs'

const locationFields = ['address1', 'address2', 'state', 'country', 'postCode', 'suburb']
const prefix = 'postal'

class Location extends React.PureComponent {
  static defaultProps = {
    fieldsRequired: true,
  }
  onFieldChange = (fieldName, value, isPostal) => {
    if (isPostal) {
      this.props.dispatch(
        change(this.props.formName, fieldName.toLowerCase().split('postal')[1], value),
      )
    } else {
      this.props.dispatch(change(this.props.formName, `${prefix}${capitalize(fieldName)}`, value))
    }
  }
  onCheckboxChange = (event) => {
    if (!event.target.value) {
      locationFields.map(field =>
        this.props.dispatch(
          change(this.props.formName, `${prefix}${capitalize(field)}`, this.props.values[field]),
        ),
      )
    } else {
      locationFields.map(field =>
        this.props.dispatch(
          change(
            this.props.formName,
            `${prefix}${capitalize(field)}`,
            this.props.initialValues[field],
          ),
        ),
      )
    }
  }
  stub = () => ({})
  render() {
    return (
      <div className="row">
        <div className="col-sm-12">
          <div className="form-group">
            <label htmlFor="">Is Street address is the same as Postal address?</label>
            <div className="switch" style={{ display: 'inline-block', height: 30 }}>
              <label>
                <Field
                  component="input"
                  type="checkbox"
                  name="addressesAreEquals"
                  onChange={this.onCheckboxChange}
                />
                <span className="lever switch-col-light-blue" />
              </label>
            </div>
          </div>
        </div>
        <div className="col-sm-6">
          <div className="form-group">
            <h3>Street address</h3>
          </div>
          <LocationInputs
            fieldsRequired={this.props.fieldsRequired}
            onFieldChange={this.props.values.addressesAreEquals ? this.onFieldChange : this.stub}
          />
        </div>
        <div className="col-sm-6">
          <div className="form-group">
            <h3>Postal address</h3>
          </div>
          <LocationInputs
            fieldsRequired={this.props.fieldsRequired}
            onFieldChange={this.props.values.addressesAreEquals ? this.onFieldChange : this.stub}
            prefix={prefix}
          />
        </div>
      </div>
    )
  }
}

export default withData(
  connect((state, ownProps) => {
    if (ownProps.formState) {
      return { values: ownProps.formState.values }
    }

    return { values: state.form[ownProps.formName].values }
  })(Location),
)
