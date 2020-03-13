import React, { Fragment } from 'react'
import { reduxForm, Field, change } from 'redux-form'
import { connect } from 'react-redux'
import { compose, gql, graphql } from 'react-apollo'
import { filter } from 'graphql-anywhere'
import swal from 'sweetalert'

import AsyncAutocomplete from 'components/AsyncAutocomplete'
import Button from 'components/Button'
import { renderInput, renderSelect, onlyNums } from 'utils'
import { organisationFragment } from 'fragments'
import { getIndustries, getMails } from 'queries'
import doc from './doc'

const getOrganisations = gql`
  query organisationOrganisation($name: String, $skip: Boolean!) {
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

class Details extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      loading: false,
    }
  }
  onSubmit = (data) => {
    this.setState({ loading: true })

    if (this.props.onSubmitFunc) {
      if (this.props.wizard) {
        this.props.onSubmitFunc(this.props.formNumber + 1)
      } else {
        this.props
          .onSubmitFunc(data)
          .then(() => {
            swal({ text: 'The changes have been saved!', icon: 'success' })
          })
          .catch(() => {
            swal({ text: 'Something went wrong!', icon: 'error' })
          })
      }
    } else {
      this.updateOrganisation(data)
        .then(() => {
          swal({ text: 'The changes have been saved!', icon: 'success' })
        })
        .catch(() => {
          swal({ text: 'Something went wrong!', icon: 'error' })
        })
    }

    this.setState({ loading: false })
  }
  onGroupStatusChange = (event) => {
    const {
      form: { values },
    } = this.props
    const { value } = event.target
    if (value === '1') {
      this.props.dispatch(
        change('organisationForm', 'groupParent', { id: values.id, name: values.name }),
      )
    } else if (value === '2') {
      this.props.dispatch(change('organisationForm', 'groupParent', null))
    }
  }
  getOptions = async (input, callback) => {
    const { organisationsData } = this.props
    if (input.length > 2) {
      // fetch organisations filtered by name
      const response = await organisationsData.refetch({ skip: false, name: input })
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
  handleNameChange = (event) => {
    const { value } = event.target
    const {
      form: { values },
    } = this.props
    if (parseInt(values.groupStatus, 10) === 1) {
      this.props.dispatch(change('organisationForm', 'groupParent', { id: values.id, name: value }))
    }
  }
  handleGroupParentSelect = ({ value, label }) => {
    this.props.dispatch(change('organisationForm', 'groupParent', { id: value, name: label }))
  }
  handleGroupParentEdit = fieldName =>
    this.props.dispatch(change('organisationForm', fieldName, null))
  updateOrganisation = values =>
    new Promise((resolve, reject) => {
      const contacts = values.contacts.map(({ node }) => node.id)
      this.props
        .mutate({
          variables: {
            organisationData: filter(doc, { ...values, contacts }),
            organisationId: values.id,
          },
          refetchQueries: [{ query: getMails, variables: { organisationId: values.id } }],
        })
        .then((response) => {
          if (response.data.updateOrganisationDetails.errors.length > 0) {
            console.log(response.data.updateOrganisationDetails.errors)
            reject()
          } else {
            resolve()
          }
        })
    })
  render() {
    const { industriesData, form } = this.props
    let errors = {}

    if (form.syncErrors) {
      errors = form.syncErrors
    }
    return (
      <form
        className="form-horizontal form-control-line"
        onSubmit={this.props.handleSubmit(this.onSubmit)}
      >
        <Field component="input" type="hidden" name="groupParent" />
        <div className="row">
          <div className="col">
            <label htmlFor="name">Name</label>
            <Field
              id="name"
              component={renderInput}
              onChange={this.handleNameChange}
              name="name"
              type="text"
            />
          </div>
          <div className="col">
            <label htmlFor="groupStatus">Group status</label>
            <div className="form-group">
              <Field
                component="select"
                id="groupStatus"
                onChange={this.onGroupStatusChange}
                className="form-control"
                name="groupStatus"
              >
                <option value={1}>Parent</option>
                <option value={2}>Group member</option>
              </Field>
            </div>
          </div>
          <div className="col">
            {/* Async autocomplete */}
            <AsyncAutocomplete
              label="Group parent"
              editable={parseInt(form.values.groupStatus, 10) === 2}
              fieldName="groupParent"
              link="organisation"
              error={errors.groupParent}
              onSelect={this.handleGroupParentSelect}
              onEdit={this.handleGroupParentEdit}
              value={form.values.groupParent}
              accessor="name"
              placeholder="Search for organisation"
              getOptions={this.getOptions}
            />
          </div>
        </div>
        <div className="row">
          <div className="col">
            <label htmlFor="mainLine">Main line</label>
            <Field
              id="mainLine"
              component={renderInput}
              normalize={onlyNums}
              name="mainLine"
              type="text"
            />
          </div>
          <div className="col">
            <label className="col-md-12" htmlFor="website">
              Website
            </label>
            <div className="col-md-12">
              <Field id="website" component={renderInput} name="website" type="text" />
            </div>
          </div>
          <div className="col">
            <label htmlFor="industry">Industry</label>
            <Field
              component={renderSelect}
              id="industry"
              className="form-control"
              name="industryId"
            >
              {industriesData.loading ? (
                <option>Loading...</option>
              ) : (
                <Fragment>
                  <option value={null}>--------</option>
                  {industriesData.industries.map(industry => (
                    <option key={industry.id} value={industry.id}>
                      {industry.name}
                    </option>
                  ))}
                </Fragment>
              )}
            </Field>
          </div>
        </div>
        <div className="row">
          <div className="col-md-8">
            <label htmlFor="businessSearchWords">Business search words</label>
            <div className="form-group">
              <Field
                id="businessSearchWords"
                component="textarea"
                className="form-control"
                name="businessSearchWords"
                type="text"
              />
            </div>
          </div>
          {this.props.canLinkMails && <div className="col-md-4">
            <div>
              <label htmlFor="linkMails">Link emails?</label>
            </div>
            <div className="switch mt-3" style={{ display: 'inline-block', height: 30 }}>
              <label>
                <Field component="input" type="checkbox" name="linkMails" />
                <span className="lever switch-col-light-blue" />
              </label>
            </div>
          </div>}
        </div>
        <div className="row">
          <div className="col-md-12">
            <div className="form-group">
              <Button
                title={this.props.buttonTitle}
                loading={this.state.loading}
                className="btn btn-success"
                type="submit"
                style={{ width: 120 }}
              />
            </div>
          </div>
        </div>
      </form>
    )
  }
}

const updateOrganisation = gql`
  mutation updateOrganisation($organisationId: ID!, $organisationData: OrganisationInput) {
    updateOrganisationDetails(
      organisationId: $organisationId
      organisationData: $organisationData
    ) {
      errors
      organisation {
        ...Organisation
      }
    }
  }
  ${organisationFragment}
`

const validate = (values) => {
  const errors = {}

  if (!values.name) {
    errors.name = 'Organisation name is required'
  }
  if (!values.industryId) {
    errors.industryId = 'Please select an industry'
  }

  return errors
}

// const warn = (values, ownProps) => {
//   const warnings = {}

//   if (ownProps.organisations.map(org => org.name).includes(values.name)) {
//     warnings.name = `Organisation "${values.name}" already exists!`
//   }

//   return warnings
// }

export default compose(
  reduxForm({
    form: 'organisationForm',
    validate,
    // warn,
    destroyOnUnmount: false,
    enableReinitialize: true,
    keepDirtyOnReinitialize: true,
  }),
  connect(state => ({ form: state.form.organisationForm })),
  graphql(updateOrganisation),
  graphql(getIndustries, { name: 'industriesData' }),
  graphql(getOrganisations, { name: 'organisationsData', options: { variables: { skip: true } } }),
)(Details)
