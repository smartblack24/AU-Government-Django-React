import React from 'react'
import { reduxForm, Field } from 'redux-form'
import { graphql, gql } from 'react-apollo'
import { toast } from 'react-toastify'

import Button from 'components/Button'
import LocationForms from 'components/Location'
import { getOrganisation } from 'queries'

class LocationForm extends React.Component {
  state = {
    loading: false,
  }
  onSubmitFunc = (data) => {
    this.setState({ loading: true })

    if (this.props.onSubmitFunc) {
      if (this.props.wizard) {
        this.props.onSubmitFunc(data)
      } else {
        this.props
          .onSubmitFunc(data)
          .then(() => toast.success('The changes have been saved!'))
          .catch(() => toast.error('Something went wrong!'))
      }
    } else {
      this.updateLocation(data)
        .then(() => toast.success('The changes have been saved!'))
        .catch(() => toast.error('Something went wrong!'))
    }

    this.setState({ loading: false })
  }
  updateLocation = data =>
    new Promise((resolve, reject) => {
      this.props
        .mutate({
          variables: {
            id: data.id,
            address1: data.address1,
            address2: data.address2,
            state: data.state,
            country: data.country,
            postCode: data.postCode,
            suburb: data.suburb,
            postalAddress1: data.postalAddress1,
            postalAddress2: data.postalAddress2,
            postalState: data.postalState,
            postalCountry: data.postalCountry,
            postalPostCode: data.postalPostCode,
            postalSuburb: data.postalSuburb,
            addressesAreEquals: data.addressesAreEquals,
          },
          update: (store) => {
            const cache = store.readQuery({ query: getOrganisation, variables: { id: data.id } })

            cache.organisation.location.address1 = data.address1
            cache.organisation.location.address2 = data.address2
            cache.organisation.location.state = data.state
            cache.organisation.location.suburb = data.suburb
            cache.organisation.location.country = data.country
            cache.organisation.location.postCode = data.postCode

            cache.organisation.postalLocation.postalAddress1 = data.postalAddress1
            cache.organisation.postalLocation.postalAddress2 = data.postalAddress2
            cache.organisation.postalLocation.postalState = data.postalState
            cache.organisation.postalLocation.postalSuburb = data.postalSuburb
            cache.organisation.postalLocation.postalCountry = data.postalCountry
            cache.organisation.postalLocation.postalPostCode = data.postalPostCode

            store.writeQuery({ query: getOrganisation, variables: { id: data.id }, data: cache })
          },
        })
        .then((response) => {
          if (response.data.updateOrganisationLocation.errors.length > 0) {
            console.log(response.data.updateOrganisationLocation.errors)
            reject()
          } else {
            resolve()
          }
        })
    })
  render() {
    return (
      <form
        className="form-horizontal form-control-line"
        onSubmit={this.props.handleSubmit(this.onSubmitFunc)}
      >
        <Field component="input" type="hidden" name="id" />
        <LocationForms
          fieldsRequired={false}
          formName="organisationForm"
          initialValues={this.props.initialValues}
        />
        <div className="form-group">
          <div className="col-sm-12">
            <Button
              loading={this.state.loading}
              className="btn btn-success"
              type="submit"
              title={this.props.buttonTitle}
            />
          </div>
        </div>
        <style jsx>{`
          #saveButton {
            margin-right: 15px;
          }
        `}</style>
      </form>
    )
  }
}

const updateOrganisationLocation = gql`
  mutation updateOrganisationLocation(
    $id: ID!
    $address1: String
    $address2: String
    $state: Int
    $country: String
    $postCode: String
    $suburb: String
    $postalAddress1: String
    $postalAddress2: String
    $postalState: Int
    $postalCountry: String
    $postalPostCode: String
    $postalSuburb: String
    $addressesAreEquals: Boolean
  ) {
    updateOrganisationLocation(
      id: $id
      address1: $address1
      address2: $address2
      state: $state
      country: $country
      postCode: $postCode
      suburb: $suburb
      postalAddress1: $postalAddress1
      postalAddress2: $postalAddress2
      postalState: $postalState
      postalCountry: $postalCountry
      postalPostCode: $postalPostCode
      postalSuburb: $postalSuburb
      addressesAreEquals: $addressesAreEquals
    ) {
      errors
    }
  }
`

export default reduxForm({
  form: 'organisationForm',
  destroyOnUnmount: false,
  enableReinitialize: true,
  keepDirtyOnReinitialize: true,
})(graphql(updateOrganisationLocation)(LocationForm))
