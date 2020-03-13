import React from 'react'
import { reduxForm, Field } from 'redux-form'
import { graphql, gql } from 'react-apollo'
import { toast } from 'react-toastify'
import { filter } from 'graphql-anywhere'

import Button from 'components/Button'
import LocationForms from 'components/Location'
import { contactFragment } from 'fragments'
import doc from './doc'

class LocationForm extends React.Component {
  state = {
    loading: false,
  }
  onSubmitFunc = (data) => {
    this.setState({ loading: true })

    if (this.props.onSubmitFunc) {
      if (this.props.wizard) {
        this.props.onSubmitFunc(this.props.formNumber + 1)
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
            contactId: this.props.initialValues.id,
            contactData: filter(doc, {
              data,
              location: {
                address1: data.address1,
                address2: data.address2,
                suburb: data.suburb,
                state: data.state === 0 ? null : data.state,
                postCode: data.postCode,
                country: data.country === 0 ? null : data.country,
              },
              postalLocation: {
                address1: data.postalAddress1,
                address2: data.postalAddress2,
                suburb: data.postalSuburb,
                state: data.postalState === 0 ? null : data.postalState,
                postCode: data.postalPostCode,
                country: data.postalCountry === 0 ? null : data.postalCountry,
              },
            }),
          },
        })
        .then((response) => {
          if (response.data.updateContact.errors.length > 0) {
            console.log(response.data.updateContact.errors)
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
          formName="contactForm"
          initialValues={this.props.initialValues}
        />
        <div className="form-group">
          <div className="col-sm-12">
            <Button
              loading={this.state.loading}
              className="btn btn-success"
              type="submit"
              style={{ width: 120 }}
              title={this.props.buttonTitle}
            />
          </div>
        </div>
      </form>
    )
  }
}

const updateContact = gql`
  mutation updateContact($contactId: ID!, $contactData: ContactInput!) {
    updateContact(contactId: $contactId, contactData: $contactData) {
      errors
      contact {
        ...Contact
      }
    }
  }
  ${contactFragment}
`

export default reduxForm({
  form: 'contactForm',
  destroyOnUnmount: false,
  enableReinitialize: true,
  keepDirtyOnReinitialize: true,
})(graphql(updateContact)(LocationForm))
