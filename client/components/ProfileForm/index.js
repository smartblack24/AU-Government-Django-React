import React, { PureComponent } from 'react'
import { get } from 'lodash'
import Form from './Form'

class ProfileForm extends PureComponent {
  componentWillMount() {
    this.initializeProps(this.props)
  }

  componentWillReceiveProps(nextProps) {
    this.initializeProps(nextProps)
  }

  initializeProps = (props) => {
    const { initialValues } = props
    const postalLocation = {
      postalAddress1: get(initialValues, 'postalLocation.address1', ''),
      postalAddress2: get(initialValues, 'postalLocation.address2', ''),
      postalSuburb: get(initialValues, 'postalLocation.suburb', ''),
      postalState: get(initialValues, 'postalLocation.state', 1),
      postalCountry: get(initialValues, 'postalLocation.country', ''),
      postalPostCode: get(initialValues, 'postalLocation.postCode', ''),
    }

    const postalLocationToCompare = { ...initialValues.postalLocation, id: null }
    const locationToCompare = { ...initialValues.location, id: null }

    const addressesEquals =
      JSON.stringify(postalLocationToCompare) === JSON.stringify(locationToCompare)

    this.setState({
      initialValues: {
        ...initialValues.location,
        ...postalLocation,
        ...initialValues,
        country: get(initialValues, 'location.country', 'Australia'),
        postalCountry: get(postalLocation, 'country', 'Australia'),
        addressesEquals,
      },
    })
  }

  render() {
    const { initialValues } = this.state
    const { isStrange } = this.props

    return (
      <div className="card">
        <div className="card-body">
          <Form
            initialValues={initialValues}
            isStrange={isStrange}
          />
        </div>
      </div>
    )
  }
}

export default ProfileForm
