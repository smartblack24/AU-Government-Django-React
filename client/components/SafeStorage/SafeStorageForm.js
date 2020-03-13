import React from 'react'
import { graphql, gql, compose } from 'react-apollo'
import { reduxForm, Field, change, reset } from 'redux-form'
import { Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap'
import { connect } from 'react-redux'
import moment from 'moment'

import { getSections } from 'queries'
import { documentFragment } from 'fragments'
import { getDocuments } from 'components/SafeStorage'
import { renderSelect, renderTextarea } from 'utils'
import Button from 'components/Button'
import CustomDatePicker from 'components/DatePicker'

class SafeStorageForm extends React.Component {
  state = {
    loading: false,
  }
  componentWillReceiveProps(nextProps) {
    if (!nextProps.modal && this.props.modal) {
      this.props.dispatch(reset('safeStorageForm'))
    }
  }
  handleDateChange = (date) => {
    this.props.dispatch(change('safeStorageForm', 'date', date.format('YYYY-MM-DD')))
  }
  handleDateRemovedChange = (dateRemoved) => {
    this.props.dispatch(change('safeStorageForm', 'dateRemoved', dateRemoved.format('YYYY-MM-DD')))
  }
  handleDocumentStatusChange = (event) => {
    const value = parseInt(event.target.value, 10)

    if (value !== 2) {
      this.props.dispatch(change('safeStorageForm', 'dateRemoved', null))
    } else {
      this.props.dispatch(change('safeStorageForm', 'dateRemoved', moment()))
    }
  }
  handleSubmit = (values) => {
    if (this.props.editMode) {
      this.handleUpdateDocument(values)
    } else {
      this.handleCreateDocument(values)
    }
  }
  handleCreateDocument = async (values) => {
    this.setState({ loading: true })
    let sectionId = null
    const { data } = await this.props.addDocument({
      variables: {
        document: {
          ...values,
          andrewExecutor: values.andrewExecutor === 'true',
          contactId: this.props.contactId,
          organisationId: this.props.organisationId,
          chargingClause: values.andrewExecutor === 'true' ? values.chargingClause : null,
        },
      },
      update: (store, { data: { createDocument } }) => {
        const documentsCache = store.readQuery({
          query: getDocuments,
          variables: this.props.documentListVariables,
        })

        documentsCache.documents.edges.push({
          cursor: '',
          node: createDocument.document,
          __typename: 'DocumentTypeEdge',
        })
        sectionId = values.sectionId

        store.writeQuery({
          query: getDocuments,
          variables: this.props.documentListVariables,
          data: documentsCache,
        })

        if (!this.props.initialValues.sectionId) {
          const sectionsCache = store.readQuery({ query: getSections })
          sectionsCache.sections.push(createDocument.document.section)
          store.writeQuery({ query: getSections, data: sectionsCache })
        }
      },
    })

    if (data.createDocument.errors.length > 0) {
      console.log(data.createDocument.errors)
    } else {
      this.props.toggleModal()
      this.props.changeSection(sectionId)
    }

    this.setState({ loading: false })
  }
  handleUpdateDocument = async (values) => {
    this.setState({ loading: true })

    const { data } = await this.props.updateDocument({
      variables: {
        document: {
          documentId: values.id,
          date: values.date,
          dateRemoved: values.dateRemoved,
          status: values.status,
          notes: values.notes,
          documentTypeId: values.documentTypeId !== 0 ? values.documentTypeId : null,
          nominatedType: values.nominatedType,
          nominatedNames: values.nominatedNames,
          andrewExecutor: values.andrewExecutor === 'true',
          contactId: this.props.contactId,
          sectionId: values.sectionId,
          organisationId: this.props.organisationId,
          chargingClause: values.andrewExecutor === 'true' ? values.chargingClause : null,
        },
      },
    })

    if (data.updateDocument.errors.length > 0) {
      console.log(data.updateDocument.errors)
    } else {
      this.props.toggleModal()
    }

    this.setState({ loading: false })
  }

  render() {
    let isWill = false
    if (this.props.data.documentTypes) {
      isWill =
        this.props.data.documentTypes.find(
          doc => parseInt(doc.id, 10) === parseInt(this.props.form.documentTypeId, 10),
        ).name === 'Will'
    }
    return (
      <Modal isOpen={this.props.modal} toggle={this.props.toggleModal}>
        <ModalHeader toggle={this.props.toggleModal}>
          {this.props.editMode ? 'Edit the Document' : 'Add a Document'}
        </ModalHeader>
        <form onSubmit={this.props.handleSubmit(this.handleSubmit)}>
          <Field component="input" type="hidden" name="date" />
          <Field component="input" type="hidden" name="dateRemoved" />
          {/* <Field component="input" type="hidden" name="sectionId" /> */}
          <Field component="input" type="hidden" name="id" />
          <ModalBody>
            <div className="form-group">
              <label htmlFor="section">Section</label>
              <Field
                component={renderSelect}
                name="sectionId"
                id="sectionId"
                className="form-control"
              >
                {this.props.data.loading ? (
                  <option>Loading...</option>
                ) : (
                  this.props.sectionsData &&
                  this.props.sectionsData.map(section => (
                    <option key={section.id} value={section.id}>
                      {section.number} {section.office.shortName}
                    </option>
                  ))
                )}
              </Field>
            </div>
            <div className="form-group">
              <label htmlFor="date">Date</label>
              <CustomDatePicker
                id="date"
                selected={moment(this.props.form.date)}
                onChange={this.handleDateChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="status">Document Status</label>
              <Field
                component={renderSelect}
                name="status"
                id="status"
                className="form-control"
                onChange={this.handleDocumentStatusChange}
              >
                <option value={1}>Original held by Andreyev Lawyers</option>
                <option value={2}>Removed</option>
                <option value={3}>Not Returned</option>
                <option value={4}>Transit Money held by Andreyev Lawyers</option>
                <option value={5}>Scanned</option>
              </Field>
            </div>
            <div className="form-group">
              <label htmlFor="dateRemoved">Date removed</label>
              <CustomDatePicker
                id="dateRemoved"
                selected={this.props.form.dateRemoved ? moment(this.props.form.dateRemoved) : null}
                onChange={this.handleDateRemovedChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="documentTypeId">Document Type</label>
              <Field
                component={renderSelect}
                name="documentTypeId"
                id="documentTypeId"
                className="form-control"
              >
                {this.props.data.loading ? (
                  <option>Loading...</option>
                ) : (
                  this.props.data.documentTypes.map(documentType => (
                    <option key={documentType.id} value={documentType.id}>
                      {documentType.name}
                    </option>
                  ))
                )}
              </Field>
            </div>
            <div className="form-group">
              <label htmlFor="notes">Document Notes</label>
              <Field component={renderTextarea} name="notes" id="notes" className="form-control" />
            </div>
            <div className="form-group">
              <label htmlFor="nominatedType">Nominated Type</label>
              <Field
                component={renderSelect}
                name="nominatedType"
                id="nominatedType"
                className="form-control"
              >
                <option value={1}>Executor</option>
                <option value={2}>Attorney</option>
                <option value={3}>Guardian</option>
                <option value={4}>Donee</option>
                <option value={5}>Substitute Decision Maker</option>
                <option value={6}>Beneficiary</option>
                <option value={7}>Other</option>
                <option value={8}>No selection</option>
              </Field>
            </div>
            <div className="form-group">
              <label htmlFor="nominatedNames">Nominated Name/s</label>
              <Field
                component={renderTextarea}
                name="nominatedNames"
                id="nominatedNames"
                className="form-control"
              />
            </div>
            {isWill && (
              <div className="form-group">
                <label htmlFor="andrewExecutor" className="mr-3">
                  Will, Andrew Executor
                </label>
                <label className="mr-3">
                  <Field
                    component="input"
                    type="radio"
                    id="andrewExecutor"
                    name="andrewExecutor"
                    value="true"
                    className="mr-1"
                  />
                  Yes
                </label>
                <label>
                  <Field
                    component="input"
                    type="radio"
                    id="andrewExecutor"
                    name="andrewExecutor"
                    value="false"
                    className="mr-1"
                  />
                  No
                </label>
              </div>
            )}
            {isWill &&
              this.props.form.andrewExecutor === 'true' && (
                <div className="form-group">
                  <label htmlFor="chargingClause">Will – Charging Clause</label>
                  <div>
                    <label className="mr-3">
                      <Field
                        component="input"
                        type="radio"
                        id="chargingClause"
                        name="chargingClause"
                        className="mr-1"
                        value="1"
                      />
                      Yes - Signed
                    </label>
                    <label className="mr-3">
                      <Field
                        component="input"
                        type="radio"
                        id="chargingClause"
                        name="chargingClause"
                        value="2"
                        className="mr-1"
                      />
                      n/a
                    </label>
                    <label>
                      <Field
                        component="input"
                        type="radio"
                        id="chargingClause"
                        name="chargingClause"
                        value="3"
                        className="mr-1"
                      />
                      Not returned
                    </label>
                  </div>
                </div>
              )}
          </ModalBody>
          <ModalFooter>
            <Button
              title="Save"
              loading={this.state.loading}
              className="btn btn-success"
              type="submit"
              style={{ width: 80 }}
            />
          </ModalFooter>
        </form>
      </Modal>
    )
  }
}

const addDocument = gql`
  mutation createDocument($document: DocumentInput!) {
    createDocument(document: $document) {
      document {
        ...Document
      }
      errors
    }
  }
  ${documentFragment}
`

const updateDocument = gql`
  mutation updateDocument($document: DocumentInput!) {
    updateDocument(document: $document) {
      document {
        ...Document
      }
      errors
    }
  }
  ${documentFragment}
`

const getDocumentTypes = gql`
  query documentTypes {
    documentTypes {
      id
      name
    }
  }
`

export default reduxForm({ form: 'safeStorageForm', enableReinitialize: true })(
  compose(
    graphql(addDocument, { name: 'addDocument' }),
    graphql(updateDocument, { name: 'updateDocument' }),
    graphql(getDocumentTypes),
    connect(state => ({ form: state.form.safeStorageForm.values })),
  )(SafeStorageForm),
)
