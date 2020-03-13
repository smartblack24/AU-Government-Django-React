import React from 'react'
import { Field } from 'redux-form'

import { renderInput, renderSelect } from 'utils'
import countries from './countries'

const isRequired = value => (value ? undefined : 'This field is required')
const isNotRequired = () => undefined

const InputField = ({ isPostal, ...props }) => {
  const onChange = (event) => {
    props.onChange(props.name, event.target.value, isPostal)
  }
  return <Field {...props} onChange={onChange} />
}

const LocationForm = ({ prefix, fieldsRequired, onFieldChange }) => (
  <div>
    <label className="col-md-12" htmlFor="address1">
      Address Line 1
    </label>
    <div className="col-md-12">
      <InputField
        id={prefix ? `${prefix}Address1` : 'address1'}
        isPostal={!!prefix}
        validate={[fieldsRequired ? isRequired : isNotRequired]}
        component={renderInput}
        onChange={onFieldChange}
        name={prefix ? `${prefix}Address1` : 'address1'}
        type="text"
      />
    </div>
    <label className="col-md-12" htmlFor="address2">
      Address Line 2
    </label>
    <div className="col-md-12">
      <InputField
        id={prefix ? `${prefix}Address2` : 'address2'}
        isPostal={!!prefix}
        component={renderInput}
        onChange={onFieldChange}
        name={prefix ? `${prefix}Address2` : 'address2'}
        type="text"
      />
    </div>
    <label className="col-md-12" htmlFor="suburb">
      Suburb
    </label>
    <div className="col-md-12">
      <InputField
        id={prefix ? `${prefix}Suburb` : 'suburb'}
        isPostal={!!prefix}
        validate={[fieldsRequired ? isRequired : isNotRequired]}
        component={renderInput}
        onChange={onFieldChange}
        name={prefix ? `${prefix}Suburb` : 'suburb'}
        type="text"
      />
    </div>
    <div className="form-group">
      <label className="col-md-12" htmlFor="state">
        State
      </label>
      <div className="col-md-12">
        <InputField
          component={renderSelect}
          isPostal={!!prefix}
          validate={[fieldsRequired ? isRequired : isNotRequired]}
          name={prefix ? `${prefix}State` : 'state'}
          id={prefix ? `${prefix}State` : 'state'}
          onChange={onFieldChange}
          className="form-control"
        >
          <option value={0}>----------</option>
          <option value={1}>SA</option>
          <option value={2}>NSW</option>
          <option value={3}>VIC</option>
          <option value={4}>WA</option>
          <option value={5}>QLD</option>
          <option value={6}>TAS</option>
          <option value={7}>NT</option>
          <option value={8}>ACT</option>
        </InputField>
      </div>
    </div>
    <label className="col-md-12" htmlFor="postCode">
      Post code
    </label>
    <div className="col-md-12">
      <InputField
        id={prefix ? `${prefix}PostCode` : 'postCode'}
        isPostal={!!prefix}
        validate={[fieldsRequired ? isRequired : isNotRequired]}
        component={renderInput}
        onChange={onFieldChange}
        name={prefix ? `${prefix}PostCode` : 'postCode'}
        type="text"
      />
    </div>
    <label className="col-md-12" htmlFor="country">
      Country
    </label>
    <div className="col-md-12 form-group">
      <InputField
        component={renderSelect}
        isPostal={!!prefix}
        validate={[fieldsRequired ? isRequired : isNotRequired]}
        name={prefix ? `${prefix}Country` : 'country'}
        id={prefix ? `${prefix}Country` : 'country'}
        onChange={onFieldChange}
        className="form-control"
      >
        <option value={0}>----------</option>
        {countries.map(country => (
          <option key={country} value={country}>
            {country}
          </option>
        ))}
      </InputField>
    </div>
  </div>
)

LocationForm.defaultProps = {
  prefix: '',
  fieldsRequired: true,
  onFieldChange: () => ({}),
}

export default LocationForm
