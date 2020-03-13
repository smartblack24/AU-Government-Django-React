import React from 'react'
import { reduxForm, Field, change, reset } from 'redux-form'
import { connect } from 'react-redux'
import { gql, graphql, compose } from 'react-apollo'
import { toast } from 'react-toastify'

import AsyncAutocomplete from 'components/AsyncAutocomplete'
import Button from 'components/Button'
import RemoveIcon from 'components/RemoveIcon'
import { contactFragment } from 'fragments'
import { getOrganisation } from 'queries'

const updateAssociaton = gql`
  mutation updateAssociaton($organisationId: ID!, $contacts: [ID]!) {
    updateOrganisationAssociation(organisationId: $organisationId, contacts: $contacts) {
      errors
    }
  }
`

const getContacts = gql`
  query contactsAndClients($fullName: String, $skip: Boolean!) {
    contacts(fullName: $fullName) @skip(if: $skip) {
      edges {
        cursor
        node {
          id
          fullName
        }
      }
    }
  }
`

class ContactsAndClients extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      loading: false,
      error: null,
    }
  }
  onSubmit = (data) => {
    this.setState({ loading: true, error: null })

    if (this.props.onSubmitFunc) {
      this.props
        .onSubmitFunc(data)
        .then(() => {
          this.props.dispatch(reset('organisationForm'))
          if (this.props.resetAfterSubmit) {
            this.props.dispatch(reset('organisationForm'))
          }

          toast.success('The changes have been saved!')
        })
        .catch(() => toast.error('Something went wrong!'))
    } else {
      this.updateAssociaton(data)
        .then(() => {
          if (this.props.resetAfterSubmit) {
            this.props.dispatch(reset('organisationForm'))
          }

          toast.success('The changes have been saved!')
        })
        .catch(() => toast.error('Something went wrong!'))
    }

    this.setState({ loading: false })
  }
  getContacts = async (input, callback) => {
    const { data } = this.props
    if (input.length > 2) {
      // fetch contacts filtered by full name
      const response = await data.refetch({ skip: false, fullName: input })
      if (response.data.contacts.edges.length) {
        // transform to react-select format
        const options = response.data.contacts.edges.map(contact => ({
          value: contact.node.id,
          label: contact.node.fullName,
        }))

        // callback with fetched data
        callback(null, { options })
      }
    }
  }
  handleAutocompleteSelect = ({ value, label }) => {
    const { form, dispatch } = this.props
    const selectedContacts = form.contacts.map(({ node }) => node.id)

    if (!selectedContacts.includes(value)) {
      dispatch(
        change(
          'organisationForm',
          'contacts',
          form.contacts.concat({ node: { id: value, fullName: label } }),
        ),
      )
    }
  }
  handleRemoveContact = (contactId) => {
    const { form, dispatch } = this.props

    dispatch(
      change(
        'organisationForm',
        'contacts',
        form.contacts.filter(({ node }) => node.id !== contactId),
      ),
    )
  }
  updateAssociaton = values =>
    new Promise((resolve, reject) => {
      const contacts = values.contacts.map(({ node }) => node.id)
      this.props
        .mutate({
          variables: {
            organisationId: this.props.initialValues.id,
            contacts,
          },
          refetchQueries: [
            { query: getOrganisation, variables: { id: this.props.initialValues.id } },
          ],
          update: (store) => {
            contacts.forEach((contactId) => {
              try {
                const contact = store.readFragment({
                  id: `ContactType-${contactId}`,
                  fragmentName: 'Contact',
                  fragment: contactFragment,
                })

                contact.organisations.edges = contact.organisations.edges
                  .filter(({ node }) => node.id !== this.props.initialValues.id)
                  .concat({
                    node: {
                      id: this.props.initialValues.id,
                      name: this.props.initialValues.name,
                      cursor: '',
                    },
                  })

                store.writeFragment({
                  id: `ContactType-${contactId}`,
                  fragmentName: 'Contact',
                  fragment: contactFragment,
                  data: contact,
                })
              } catch (e) {} //eslint-disable-line
            })
          },
        })
        .then((response) => {
          if (response.data.updateOrganisationAssociation.errors.length > 0) {
            response.data.updateOrganisationAssociation.errors.forEach((item) => {
              if (isNaN(item)) {
                this.setState({ error: item })
              }
            })
            reject()
          } else {
            resolve()
          }
        })
    })
  renderContactList = () => {
    const { form } = this.props
    if (form.contacts.length > 0) {
      return form.contacts.map(({ node }) => (
        <tbody>
          <tr key={node.fullName} className="contact-item">
            <td>
              <RemoveIcon value={node.id} onClick={this.handleRemoveContact} />
              <a href={`/contact/${node.id}`} target="_blank">
                {node.fullName}
              </a>
            </td>
          </tr>
        </tbody>
      ))
    }

    return (
      <tr>
        <td>No associations</td>
      </tr>
    )
  }
  render() {
    return (
      <form className="form-horizontal" onSubmit={this.props.handleSubmit(this.onSubmit)}>
        <Field component="input" type="hidden" name="contacts" />
        <div className="col-md-12">
          <div className="form-group">
            {/* Async autocomplete */}
            <AsyncAutocomplete
              fieldName="contact"
              onSelect={this.handleAutocompleteSelect}
              placeholder="Search for contact"
              getOptions={this.getContacts}
            />
          </div>
        </div>
        <div className="col-md-12">
          <div className="form-group">
            <div className="table-responsive">
              <table className="table table-bordered">
                <thead>
                  <tr>
                    <th>Associations</th>
                  </tr>
                </thead>
                {this.renderContactList()}
              </table>
            </div>
          </div>
        </div>
        <div className="form-group">
          <div className="col-sm-12">
            <span className="text-danger">{this.state.error}</span>
          </div>
        </div>
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
          .contact-item {
            cursor: pointer;
          }
          td {
            cursor: pointer;
          }
          .remove:hover {
            color: red;
          }
        `}</style>
      </form>
    )
  }
}

export default compose(
  reduxForm({
    form: 'organisationForm',
    destroyOnUnmount: false,
    enableReinitialize: true,
    keepDirtyOnReinitialize: true,
  }),
  connect(state => ({ form: state.form.organisationForm.values })),
  graphql(updateAssociaton),
  graphql(getContacts, { options: { variables: { skip: true } } }),
)(ContactsAndClients)
