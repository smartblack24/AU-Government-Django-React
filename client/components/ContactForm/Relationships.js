import React from 'react'
import { gql, graphql, compose } from 'react-apollo'
import { reduxForm, change, Field } from 'redux-form'
import { connect } from 'react-redux'
import { toast } from 'react-toastify'

import { contactFragment } from 'fragments'
import Button from 'components/Button'
import AsyncAutocomplete from 'components/AsyncAutocomplete'
import ReferrerList from './ReferrerList'
import Children from './Children'

const updateReferrer = gql`
  mutation updateReferrer($relationship: RelationshipInput) {
    updateReferrer(relationship: $relationship) {
      errors
      contact {
        ...Contact
      }
      referrer {
        ...Contact
      }
      spouse {
        ...Contact
      }
      mother {
        ...Contact
      }
    }
  }
  ${contactFragment}
`

const getContacts = gql`
  query contactRelationShip($fullName: String, $skip: Boolean!) {
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

class Relationships extends React.Component {
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
        this.props.onSubmitFunc(data).catch(() => toast.error('Something went wrong!'))
      }
    } else {
      this.updateReferrer(data)
        .then(() => {
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
  updateReferrer = (values) => {
    const {
      initialValues: { spouse },
    } = this.props
    const refetchQueries = []

    // if the contact had a spouse then refetch the spouse contact
    if (spouse) {
      refetchQueries.push({
        query: gql`
          query updateCache($id: ID!) {
            contact(id: $id) {
              ...Contact
            }
          }
          ${contactFragment}
        `,
        variables: { id: spouse.id },
      })
    }
    return new Promise((resolve, reject) => {
      this.props
        .mutate({
          variables: {
            relationship: {
              contactId: this.props.initialValues.id,
              referrerId: values.referrer && values.referrer.id,
              spouseId: values.spouse && values.spouse.id,
              motherId: values.mother && values.mother.id,
              fatherId: values.father && values.father.id,
            },
          },
          refetchQueries,
        })
        .then((response) => {
          if (response.data.updateReferrer.errors.length > 0) {
            console.log(response.data.updateReferrer.errors)
            reject()
          } else {
            resolve()
          }
        })
    })
  }
  handleRelatedContactSelect = ({ value, label }, fieldName) => {
    const { dispatch } = this.props

    dispatch(change('contactForm', fieldName, { id: value, fullName: label }))
  }
  handleRelatedContactRemove = fieldName =>
    this.props.dispatch(change('contactForm', fieldName, null))
  render() {
    const { form } = this.props
    let errors = {}

    if (form.syncErrors) {
      errors = form.syncErrors
    }
    return (
      <form className="form-horizontal" onSubmit={this.props.handleSubmit(this.onSubmit)}>
        <Field component="input" type="hidden" name="referrer" />
        <Field component="input" type="hidden" name="spouse" />
        <Field component="input" type="hidden" name="father" />
        <Field component="input" type="hidden" name="mother" />
        <div className="form-group">
          <ReferrerList
            label="This contact was introduced by"
            fieldName="referrer"
            onEdit={this.handleRelatedContactRemove}
            onSelect={this.handleRelatedContactSelect}
            getOptions={this.getContacts}
            error={errors.referrer}
            value={form.values.referrer}
            accessor="fullName"
            placeholder="Search for contact"
            referrers={form.values.referrers}
          />
        </div>
        <div className="row">
          <div className="col col-md-4 form-group">
            <AsyncAutocomplete
              label="Spouse"
              fieldName="spouse"
              link="contact"
              error={errors.spouse}
              onSelect={this.handleRelatedContactSelect}
              onEdit={this.handleRelatedContactRemove}
              value={form.values.spouse}
              accessor="fullName"
              placeholder="Search for contact"
              getOptions={this.getContacts}
            />
          </div>
          <div className="col col-md-4  form-group">
            <AsyncAutocomplete
              label="Mother"
              fieldName="mother"
              link="contact"
              error={errors.mother}
              onSelect={this.handleRelatedContactSelect}
              onEdit={this.handleRelatedContactRemove}
              value={form.values.mother}
              accessor="fullName"
              placeholder="Search for contact"
              getOptions={this.getContacts}
            />
          </div>
          <div className="col col-md-4  form-group">
            <AsyncAutocomplete
              label="Father"
              fieldName="father"
              link="contact"
              error={errors.father}
              onSelect={this.handleRelatedContactSelect}
              onEdit={this.handleRelatedContactRemove}
              value={form.values.father}
              accessor="fullName"
              placeholder="Search for contact"
              getOptions={this.getContacts}
            />
          </div>
        </div>
        <Children childrenList={this.props.initialValues.children} />
        <div className="form-group">
          <div className="col-sm-12">
            <Button
              loading={this.state.loading}
              className="btn btn-success"
              type="submit"
              style={{ width: 120 }}
              title="Save"
            />
          </div>
        </div>
        <style jsx>{`
          a {
            color: gray;
          }
          a:hover {
            color: #000;
          }
        `}</style>
      </form>
    )
  }
}

const validate = (values, ownProps) => {
  const errors = {}

  if (values.referrer && values.referrer.id === ownProps.initialValues.id) {
    errors.referrer = 'Contact can not introduce themself'
  }
  if (!values.referrer) {
    errors.referrer = 'Referrer is required'
  }
  if (values.spouse && values.spouse.id === ownProps.initialValues.id) {
    errors.spouse = 'Contact can not be spouse of themself'
  } else if (values.spouse && values.father && values.spouse.id === values.father.id) {
    errors.spouse = 'Contact can not be spouse and father simultaneously'
    errors.father = 'Contact can not be spouse and father simultaneously'
  } else if (values.spouse && values.mother && values.spouse.id === values.mother.id) {
    errors.spouse = 'Contact can not be spouse and mother simultaneously'
    errors.mother = 'Contact can not be spouse and mother simultaneously'
  }
  if (values.father && values.father.id === ownProps.initialValues.id) {
    errors.father = 'Contact can not be father for themself'
  } else if (values.father && values.mother && values.father.id === values.mother.id) {
    errors.father = 'Contact can not be father and mother simultaneously'
    errors.mother = 'Contact can not be father and mother simultaneously'
  }
  if (values.mother && values.mother.id === ownProps.initialValues.id) {
    errors.mother = 'Contact can not be mother for themself'
  }

  return errors
}

export default compose(
  reduxForm({
    form: 'contactForm',
    validate,
    destroyOnUnmount: false,
    enableReinitialize: true,
    keepDirtyOnReinitialize: true,
  }),
  connect(state => ({ form: state.form.contactForm })),
  graphql(updateReferrer),
  graphql(getContacts, { options: { variables: { skip: true } } }),
)(Relationships)
