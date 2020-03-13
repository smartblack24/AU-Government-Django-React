import React from 'react'
import { reduxForm, Field, change } from 'redux-form'
import { gql, graphql, compose } from 'react-apollo'
import { connect } from 'react-redux'
import { Async } from 'react-select'
import { toast } from 'react-toastify'
import { filter } from 'graphql-anywhere'

import { contactFragment } from 'fragments'
import { closeModalWindow } from 'utils'
import { createOrganisationMutation } from 'mutations'
import Button from 'components/Button'
import RemoveIcon from 'components/RemoveIcon'
import Modal from 'components/Modal'
import { getOrganisations } from 'pages/organisations'
import OrganisationForm from 'components/OrganisationForm'
import doc from './organisationsDoc'

const getContactOrganisations = gql`
  query contactOrganisation($name: String, $skip: Boolean!) {
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

const updateOrganisations = gql`
  mutation updateOrganisations($contactId: ID!, $organisations: [ID]!) {
    updateOrganisations(contactId: $contactId, organisations: $organisations) {
      errors
      contact {
        ...Contact
      }
    }
  }
  ${contactFragment}
`

class Organisations extends React.Component {
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
      if (this.props.wizard) {
        this.props.onSubmitFunc(this.props.formNumber + 1)
      } else {
        this.props
          .onSubmitFunc(data)
          .then(() => toast.success('The changes have been saved!'))
          .catch(() => toast.error('Something went wrong!'))
      }
    } else {
      this.updateOrganisations(data)
        .then(() => toast.success('The changes have been saved!'))
        .catch(() => toast.error('Something went wrong!'))
    }

    this.setState({ loading: false })
  }
  getOptions = async (input, callback) => {
    const { data } = this.props
    if (input.length > 2) {
      // fetch organisations filtered by name
      const response = await data.refetch({ skip: false, name: input })
      if (response.data.organisations.edges.length) {
        // transform to react-select format
        const options = response.data.organisations.edges.map(org => ({
          value: org.node.id,
          label: org.node.name,
        }))

        // callback with fetched data
        callback(null, { options })
      }
    }
  }
  handleAddOrganisation = data =>
    new Promise((resolve, reject) => {
      this.props
        .createOrganisation({
          variables: {
            organisationData: filter(doc, {
              ...data,
              location: {
                address1: data.address1,
                address2: data.address2,
                suburb: data.suburb,
                state: data.state,
                postCode: data.postCode,
                country: data.country,
              },
              postalLocation: {
                address1: data.postalAddress1,
                address2: data.postalAddress2,
                suburb: data.postalSuburb,
                state: data.postalState,
                postCode: data.postalPostCode,
                country: data.postalCountry,
              },
            }),
          },
          update: (store, { data: { createOrganisation } }) => {
            try {
              const cache = store.readQuery({ query: getOrganisations })

              cache.organisations.edges.push({ node: createOrganisation.organisation })

              store.writeQuery({ query: getOrganisations, data: cache })
            } catch (e) {} // eslint-disable-line
          },
        })
        .then((response) => {
          if (response.data.createOrganisation.errors.length > 0) {
            console.log(response.data.createOrganisation.errors)
            reject()
          } else {
            resolve()
            closeModalWindow()
            this.handleSelectOrganisation({
              value: response.data.createOrganisation.organisation.id,
              label: response.data.createOrganisation.organisation.name,
            })
          }
        })
    })
  updateOrganisations = async () => {
    const { organisations } = this.props.form
    return new Promise((resolve, reject) => {
      this.props
        .updateOrganisations({
          variables: {
            contactId: this.props.contactId,
            organisations: organisations.map(o => o.node.id),
          },
        })
        .then((response) => {
          if (response.data.updateOrganisations.errors.length > 0) {
            const errorIndex = response.data.updateOrganisations.errors.findIndex(
              error => error.indexOf('Some Clients') > -1,
            )

            const organisationIds = response.data.updateOrganisations.errors.filter(
              error => error.indexOf('Some Clients') === -1,
            )

            organisationIds.forEach((organisationId) => {
              const organisation = this.props.initialValues.organisations.find(
                ({ node }) => node.id === organisationId,
              )
              this.handleSelectOrganisation({
                value: organisation.node.id,
                label: organisation.node.name,
              })
            })

            this.setState({ error: response.data.updateOrganisations.errors[errorIndex] })
            reject()
          } else {
            resolve()
          }
        })
    })
  }
  handleRemoveOrganisation = (organisationId) => {
    const {
      form: { organisations },
      dispatch,
    } = this.props

    const index = organisations.findIndex(org => org.node.id === organisationId)

    if (index > -1) {
      const newOrganisation = organisations
        .slice(0, index)
        .concat(organisations.slice(index + 1, organisations.length))
      dispatch(change('contactForm', 'organisations', newOrganisation))
    }
  }
  handleSelectOrganisation = ({ value, label }) => {
    const {
      form: { organisations },
      dispatch,
    } = this.props
    const selectedOrganisations = organisations.map(org => org.node.id)

    if (!selectedOrganisations.includes(value)) {
      dispatch(
        change(
          'contactForm',
          'organisations',
          organisations.concat({ node: { id: value, name: label } }),
        ),
      )
    }
  }
  renderSelectedOrganisationsList = () => {
    const { organisations } = this.props.form

    if (!organisations.length) {
      return (
        <tr>
          <td>No organisations</td>
        </tr>
      )
    }

    return organisations.map(org => (
      <tr key={org.node.name} className="org-item">
        <td>
          <RemoveIcon value={org.node.id} onClick={this.handleRemoveOrganisation} />{' '}
          <a href={`/organisation/${org.node.id}`} target="_blank">
            {org.node.name}
          </a>
        </td>
      </tr>
    ))
  }
  render() {
    return [
      <form key={1} className="form-horizontal" onSubmit={this.props.handleSubmit(this.onSubmit)}>
        <Field component="input" type="hidden" name="organisations" />
        <div className="col-md-12">
          <div className="form-group">
            <div className="row">
              <div className="col-sm">
                {/* Async autocomplete */}
                <Async
                  cache={false}
                  autoload={false}
                  name="organisation-search-input"
                  placeholder="Search for organisation"
                  onChange={this.handleSelectOrganisation}
                  loadOptions={this.getOptions}
                />
              </div>
              <div className="col-sm-auto">
                <button
                  type="button"
                  className="btn btn-primary"
                  data-toggle="modal"
                  data-target="#organisationFormModal"
                >
                  Add
                </button>
              </div>
            </div>
          </div>
        </div>
        <div className="col-md-12">
          <div className="form-group">
            <div className="table-responsive">
              <table className="table table-bordered">
                <thead>
                  <tr>
                    <th>Organisations</th>
                  </tr>
                </thead>
                <tbody>{this.renderSelectedOrganisationsList()}</tbody>
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
              style={{ width: 120 }}
              title={this.props.buttonTitle}
            />
          </div>
        </div>
        <style jsx>{`
          .autocomplete-item {
            cursor: pointer;
            padding: 10px;
          }
          #selectedOrgs {
            border: 1px solid rgba(0, 0, 0, 0.15);
            padding: 5px;
          }
          .org-item {
            cursor: pointer;
          }
          .remove:hover {
            color: red;
          }
        `}</style>
      </form>,
      <Modal
        key={2}
        id="organisationFormModal"
        title="Add organisation"
        size="lg"
        bodyStyle={{ padding: 0, height: 790 }}
      >
        <OrganisationForm
          wizard
          buttonTitle="Add organisation"
          onSubmitFunc={this.handleAddOrganisation}
          availableTabs={[1, 2]}
          resetAfterSubmit
          initialValues={{
            groupParent: {},
            groupStatus: 1,
            address1: '',
            address2: '',
            suburb: '',
            postCode: '',
            country: '',
            postalAddress1: '',
            postalAddress2: '',
            postalSuburb: '',
            postalPostCode: '',
            postalCountry: '',
            state: null,
            postalState: null,
          }}
        />
      </Modal>,
    ]
  }
}

export default compose(
  reduxForm({
    form: 'contactForm',
    destroyOnUnmount: false,
    enableReinitialize: true,
    keepDirtyOnReinitialize: true,
  }),
  connect(state => ({ form: state.form.contactForm.values })),
  graphql(getContactOrganisations, { options: { variables: { skip: true } } }),
  graphql(updateOrganisations, { name: 'updateOrganisations' }),
  graphql(createOrganisationMutation, { name: 'createOrganisation' }),
)(Organisations)
