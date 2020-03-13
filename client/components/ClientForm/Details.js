import React from 'react'
import { reduxForm, Field, change } from 'redux-form'
import { gql, graphql, compose } from 'react-apollo'
import { connect } from 'react-redux'
import { filter } from 'graphql-anywhere'
import { toast } from 'react-toastify'

import { renderInput, onlyNums, normalizePhone } from 'utils'
import Button from 'components/Button'
import { clientFragment } from 'fragments'
import AsyncAutocomplete from 'components/AsyncAutocomplete'
import AsyncAutocompleteField from 'utils/AsyncAutocompleteField'
import AutocompleteField from 'utils/AutocompleteField'
import doc from './doc'

const getOrganisations = gql`
  query clientOrganisation($name: String, $skip: Boolean!) {
    organisations(name_Icontains: $name) @skip(if: $skip) {
      edges {
        cursor
        node {
          id
          name
        }
      }
    }
  }
`

const getContacts = gql`
  query clientContacts($fullName: String, $skip: Boolean!) {
    contacts(fullName: $fullName) @skip(if: $skip) {
      edges {
        cursor
        node {
          id
          fullName
          mobile
        }
      }
    }
  }
`

const updateDetails = gql`
  mutation updateDetails($clientData: ClientInput!) {
    updateClientDetails(clientData: $clientData) {
      errors
      client {
        ...Client
      }
    }
  }
  ${clientFragment}
`

const getOffices = gql`
  query offices {
    offices {
      id
      suburb
    }
  }
`

class Details extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      loading: false,
    }
  }
  onSubmit = (data) => {
    this.setState({ loading: true })

    if (this.props.onSubmit) {
      this.props.onSubmit(data).catch(() => toast.error('Something went wrong!'))
    } else {
      this.updateDetails(data)
        .then(() => toast.success('The changes have been saved!'))
        .catch(() => toast.error('Something went wrong!'))
    }
    this.setState({ loading: false })
  }
  getOrganisations = async (input, callback) => {
    const { organisationsData } = this.props
    if (input.length > 2) {
      // fetch organisations filtered by name
      const response = await organisationsData.refetch({ skip: false, name: input })
      if (response.data.organisations.edges.length) {
        // transform to react-select format
        const options = response.data.organisations.edges.map(({ node }) => ({
          value: node.id,
          label: node.name,
        }))

        // callback with fetched data
        callback(null, { options })
      }
    }
  }
  getContacts = async (input, callback) => {
    const { contactsData } = this.props
    if (input.length > 2) {
      const response = await contactsData.refetch({ skip: false, fullName: input })
      if (response.data.contacts.edges.length) {
        // transform to react-select format
        const options = response.data.contacts.edges.map(({ node }) => ({
          value: node.id,
          label: node.fullName,
        }))

        // callback with fetched data
        callback(null, { options })
      }
    }
  }
  handleOnAutocompleteEdit = (fieldName) => {
    this.props.dispatch(change('clientForm', fieldName, null))
  }
  handleOnOrganisationSelect = ({ value, label }) => {
    this.props.dispatch(change('clientForm', 'organisation', { id: value, name: label }))
  }
  handleOnContactSelect = ({ value, label }) => {
    const { contactsData, dispatch } = this.props
    const contact = contactsData.contacts.edges.find(({ node }) => node.id === value)

    if (contact) {
      dispatch(
        change('clientForm', 'contact', {
          id: value,
          fullName: label,
          mobile: contact.node.mobile,
        }),
      )
    } else {
      dispatch(change('clientForm', 'contact', { id: value, fullName: label }))
    }
  }
  handleOnSecondContactSelect = ({ value, label }) => {
    const { contactsData, dispatch } = this.props
    const contact = contactsData.contacts.edges.find(({ node }) => node.id === value)
    if (contact) {
      dispatch(
        change('clientForm', 'secondContact', {
          id: value,
          fullName: label,
          mobile: contact.node.mobile,
        }),
      )
    } else {
      dispatch(change('clientForm', 'secondContact', { id: value, fullName: label }))
    }
  }
  handleOnOfficeChange = (option) => {
    if (option.value) {
      this.props.dispatch(
        change('clientForm', 'office', { id: option.value, suburb: option.label }),
      )
    } else {
      this.props.dispatch(change('clientForm', 'office', null))
    }
  }
  updateDetails = data =>
    new Promise((resolve, reject) => {
      this.props
        .mutate({
          variables: {
            clientData: filter(doc, data),
          },
        })
        .then((response) => {
          if (response.data.updateClientDetails.errors.lengh > 0) {
            console.log(response.data.updateClientDetails.errors)
            reject()
          } else {
            resolve()
          }
        })
    })
  render() {
    const { form, officesData } = this.props
    let office = null

    if (form.values.office) {
      office = { value: form.values.office.id, label: form.values.office.suburb }
    }

    let offices = []
    if (!officesData.loading) {
      offices = officesData.offices.map(o => ({ value: o.id, label: o.suburb }))
    }

    return (
      <form
        className="form-horizontal form-control-line"
        onSubmit={this.props.handleSubmit(this.onSubmit)}
      >
        <div className="row form-group" style={{ overflow: 'visible' }}>
          {!this.props.addingMode && (
            <div className="col">
              <label htmlFor="name">Name</label>
              <div className="mt-3">
                <pre>{this.props.initialValues.name}</pre>
              </div>
            </div>
          )}
          <div className="col">
            <AsyncAutocomplete
              label="Organisation"
              fieldName="organisation"
              link="organisation"
              editable={this.props.editable}
              className="is-borderless"
              onSelect={this.handleOnOrganisationSelect}
              onEdit={this.handleOnAutocompleteEdit}
              value={form.values.organisation}
              accessor="name"
              placeholder="Search for organisation"
              getOptions={this.getOrganisations}
            />
          </div>
          <div className="col">
            <label htmlFor="office">Office</label>
            <Field
              name="officeName"
              component={AutocompleteField}
              className="is-borderless"
              autocompleteValue={office}
              loading={officesData.loading}
              onChange={this.handleOnOfficeChange}
              placeholder="Select an Office"
              options={offices}
            />
          </div>
        </div>
        <div className="row">
          <div className="col">
            <Field
              name="contact.fullName"
              component={AsyncAutocompleteField}
              label="Contact"
              fieldName="contact"
              editable={this.props.editable}
              link="contact"
              className="is-borderless"
              onSelect={this.handleOnContactSelect}
              onEdit={this.handleOnAutocompleteEdit}
              autocompleteValue={form.values.contact}
              accessor="fullName"
              placeholder="Search for contact"
              getOptions={this.getContacts}
            />
          </div>
          <div className="col">
            <label htmlFor="contactRole">Role</label>
            <Field id="contactRole" component={renderInput} name="contact.role" type="text" />
          </div>
          <div className="col">
            <label htmlFor="contactPhone">Contact phone</label>
            <Field
              id="contactPhone"
              normalize={normalizePhone}
              component={renderInput}
              name="contact.mobile"
              type="text"
            />
          </div>
          <div className="col">
            <AsyncAutocomplete
              label="Second contact"
              fieldName="secondContact"
              link="contact"
              className="is-borderless"
              onSelect={this.handleOnSecondContactSelect}
              onEdit={this.handleOnAutocompleteEdit}
              value={form.values.secondContact}
              accessor="fullName"
              placeholder="Search for contact"
              getOptions={this.getContacts}
            />
          </div>
          <div className="col">
            <label htmlFor="secondContactRole">Second Contact Role</label>
            <Field
              id="secondContactRole"
              component={renderInput}
              name="secondContact.role"
              type="text"
            />
          </div>
          <div className="col">
            <label htmlFor="secondContactPhone">Second Contact phone</label>
            <Field
              id="secondContactPhone"
              normalize={normalizePhone}
              component={renderInput}
              name="secondContact.mobile"
              type="text"
            />
          </div>
        </div>
        {!this.props.addingMode && (
          <div className="row">
            <div className="col">
              <label htmlFor="invoicingAddress">Full Invoicing address</label>
              <div className="mt-3">
                <pre>{this.props.initialValues.invoicingAddress}</pre>
              </div>
            </div>
            <div className="col">
              <label htmlFor="streetAddress">Full Street address</label>
              <div className="mt-3">
                <pre>{this.props.initialValues.streetAddress}</pre>
              </div>
            </div>
          </div>
        )}
        <div className="row">
          <div className="col">
            <label htmlFor="organisationPhone">Organisation main phone</label>
            <Field
              id="organisationPhone"
              component={renderInput}
              normalize={onlyNums}
              name="organisation.mainLine"
              type="text"
            />
          </div>
          <div className="col">
            <label htmlFor="orgWebsite">Organisation website</label>
            <Field
              id="orgWebsite"
              component={renderInput}
              name="organisation.website"
              type="text"
            />
          </div>
        </div>
        <div className="col-md-12">
          <div className="form-group">
            <label className="col-md-2" style={{ display: 'inline-block' }} htmlFor="isActive">
              Active status
            </label>
            <div className="switch" style={{ display: 'inline-block', height: 30 }}>
              <label>
                <Field component="input" type="checkbox" name="isActive" />
                <span className="lever switch-col-light-blue" />
              </label>
            </div>
          </div>
        </div>
        <Button
          title={this.props.buttonTitle}
          loading={this.state.loading}
          className="btn btn-success"
          type="submit"
          style={{ width: 120 }}
        />
        <style jsx>{`
          pre {
            box-shadow: none;
          }
        `}</style>
      </form>
    )
  }
}

const validate = (values) => {
  const errors = {
    contact: {},
  }

  const contact = values.contact || {}

  if (!contact.fullName) {
    errors.contact.fullName = 'This field is requried!'
  }
  // if (!contact.mobile) {
  //   errors.contact.mobile = 'This field is requried!'
  // }
  if (!values.office) {
    errors.officeName = 'This field is requried!'
  }

  return errors
}

export default compose(
  reduxForm({
    form: 'clientForm',
    validate,
    destroyOnUnmount: false,
    enableReinitialize: true,
    keepDirtyOnReinitialize: true,
  }),
  connect(state => ({ form: state.form.clientForm })),
  graphql(getOffices, { name: 'officesData' }),
  graphql(getOrganisations, { name: 'organisationsData', options: { variables: { skip: true } } }),
  graphql(getContacts, { name: 'contactsData', options: { variables: { skip: true } } }),
  graphql(updateDetails),
)(Details)
