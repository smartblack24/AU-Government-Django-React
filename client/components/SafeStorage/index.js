import React from 'react'
import { graphql, compose, gql } from 'react-apollo'
import moment from 'moment'
import { getNominatedTypeDisplay } from 'utils'
import Searchable from 'components/Searchable'
import PaginateTable from 'components/PaginateTable'
import { sectionFragment } from 'fragments'
import { getSections, getOffices } from 'queries'
import SafeStorageForm from './SafeStorageForm'

const pureDocument = {
  documentTypeId: 1,
  status: 1,
  nominatedType: 8,
  date: moment().format('YYYY-MM-DD'),
  dateRemoved: null,
  notes: '',
  nominatedNames: '',
  andrewExecutor: 'false',
  chargingClause: 1,
}

export const getDocuments = gql`
  query documents($after: String, $contactId: ID, $organisationId: ID) {
    documents(first: 15, after: $after, contactId: $contactId, organisationId: $organisationId) {
      totalPages
      edges {
        cursor
        node {
          id
          contact {
            id
            fullName
          }
          organisation {
            id
            name
          }
          owner {
            id
            fullName
          }
          section {
            ...Section
          }
          documentType {
            id
            name
          }
          date
          dateRemoved
          status
          statusDisplay
          notes
          nominatedType
          nominatedTypeDisplay
          nominatedNames
          andrewExecutor
          chargingClause
          chargingClauseDisplay
        }
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
  ${sectionFragment}
`

const updateSectionMutation = gql`
  mutation updateSection($sectionId: ID!, $officeId: ID!, $documentIds: [ID]) {
    updateSection(sectionId: $sectionId, officeId: $officeId, documentIds: $documentIds) {
      errors
      section {
        ...Section
      }
    }
  }
  ${sectionFragment}
`

class SafeStorage extends React.Component {
  constructor(props) {
    super(props)

    let sectionId = null
    let officeId = null

    if (props.documentsData.documents && props.documentsData.documents.length) {
      sectionId = props.documentsData.documents[0].section.id
      officeId = props.documentsData.documents[0].section.office.id
    }

    this.state = {
      modal: false,
      document: { ...pureDocument, sectionId },
      editMode: false,
      officeId,
    }
  }
  componentWillReceiveProps(nextProps) {
    if (!nextProps.documentsData.loading && nextProps.documentsData.documents.edges.length > 0) {
      this.setState(state => ({
        document: {
          ...state.document,
          sectionId: nextProps.documentsData.documents.edges[0].node.section.id,
        },
        officeId: nextProps.documentsData.documents.edges[0].node.section.office.id,
      }))
    }
  }
  toggleModal = () => this.setState({ modal: !this.state.modal })
  openForm = () =>
    this.setState(state => ({
      document: { ...pureDocument, sectionId: state.document.sectionId },
      modal: true,
      editMode: false,
    }))
  handleDocumentClick = instance =>
    this.setState(
      {
        document: {
          ...instance,
          dateRemoved: instance.dateRemoved,
          sectionId: instance.section.id,
          chargingClause: instance.chargingClause && instance.chargingClause.toString(),
          documentTypeId: instance.documentType.id,
          andrewExecutor: instance.andrewExecutor ? 'true' : 'false',
        },
        editMode: true,
      },
      this.toggleModal,
    )
  changeSection = sectionId =>
    new Promise((resolve) => {
      this.setState({ document: { ...this.state.document, sectionId } }, resolve)
    })
  changeOffice = officeId =>
    new Promise((resolve) => {
      this.setState({ officeId }, resolve)
    })
  handleSectionChange = ({ target: { value } }) => {
    const section = this.props.sectionsData.sections.find(s => s.id === value)

    if (section) {
      this.changeOffice(section.office.id).then(() => {
        this.changeSection(value)

        if (this.props.documentsData.documents.length) {
          this.updateSection(value, this.state.officeId)
        }
      })
    }
  }
  handleOfficeChange = ({ target: { value } }) => {
    this.changeOffice(value)
    if (this.props.documentsData.documents.length) {
      this.updateSection(this.state.document.sectionId, value)
    }
  }
  updateSection = (sectionId, officeId) => {
    const { contactId, organisationId } = this.props
    const documentIds = this.props.documentsData.documents.map(doc => doc.id)

    this.props.mutate({
      variables: { sectionId, officeId, documentIds },
      update: (store, { data: { updateSection } }) => {
        const cache = store.readQuery({
          query: getDocuments,
          variables: { contactId, organisationId },
        })

        cache.documents.map((doc) => {
          doc.section = updateSection.section
          return doc
        })

        store.writeQuery({
          query: getDocuments,
          variables: { contactId, organisationId },
          data: cache,
        })
      },
    })
  }
  render() {
    const { documentsData } = this.props
    return (
      <div>
        <SafeStorageForm
          editMode={this.state.editMode}
          modal={this.state.modal}
          toggleModal={this.toggleModal}
          contactId={this.props.contactId}
          organisationId={this.props.organisationId}
          initialValues={this.state.document}
          changeSection={this.changeSection}
          documentListVariables={documentsData.variables}
          sectionsData={this.props.sectionsData.sections}
        />
        <div className="row">
          <div className="col">
            {/* <div className="form-inline mb-3">
              <label htmlFor="section" className="mr-3">
                <strong>Section</strong>
              </label>
              <select
                className="form-control mr-3"
                onChange={this.handleSectionChange}
                value={this.state.document.sectionId || undefined}
              >
                {this.props.sectionsData.loading || this.props.documentsData.loading ? (
                  <option>Loading...</option>
                ) : (
                  <Fragment>
                    {this.props.documentsData.documents.edges.length === 0 && (
                      <option>Create new</option>
                    )}
                    {this.props.sectionsData.sections.map(section => (
                      <option key={section.id} value={section.id}>
                        {section.number}
                      </option>
                    ))}
                  </Fragment>
                )}
              </select>
              <select
                className="form-control mr-3"
                onChange={this.handleOfficeChange}
                value={this.state.officeId || undefined}
              >
                {this.props.officesData.loading ? (
                  <option>Loading...</option>
                ) : (
                  this.props.officesData.offices.map(office => (
                    <option key={office.id} value={office.id}>
                      {office.shortName}
                    </option>
                  ))
                )}
              </select>
            </div> */}
          </div>
          <div className="col-auto">
            <button onClick={this.openForm} className="btn btn-info">
              Add
            </button>
          </div>
        </div>
        <Searchable data={documentsData} dataKey="documents">
          {() => (
            <PaginateTable
              detailPageAccessor=""
              getTdProps={(state, rowInfo) => ({
                onClick: () => this.handleDocumentClick(rowInfo.original),
              })}
              columns={[
                {
                  Header: 'Date',
                  accessor: 'date',
                  headerStyle: { fontWeight: 500, textAlign: 'left', padding: '0.75rem' },
                  Cell: ({ original }) => moment(original.date).format('DD/MM/YYYY'),
                },
                {
                  Header: 'Type',
                  id: 'documentType',
                  accessor: item => item.documentType.name,
                  headerStyle: { fontWeight: 500, textAlign: 'left', padding: '0.75rem' },
                },
                {
                  Header: 'Status',
                  accessor: 'statusDisplay',
                  headerStyle: { fontWeight: 500, textAlign: 'left', padding: '0.75rem' },
                },
                {
                  Header: 'Notes',
                  accessor: 'notes',
                  headerStyle: { fontWeight: 500, textAlign: 'left', padding: '0.75rem' },
                },
                {
                  Header: 'Nominated Type',
                  id: 'nominatedType',
                  accessor: item => getNominatedTypeDisplay(item.nominatedType),
                  headerStyle: { fontWeight: 500, textAlign: 'left', padding: '0.75rem' },
                },
                {
                  Header: 'Nominated Name/s',
                  accessor: 'nominatedNames',
                  headerStyle: { fontWeight: 500, textAlign: 'left', padding: '0.75rem' },
                },
                {
                  Header: 'Section',
                  id: 'section',
                  accessor: item => [item.section.number, ' ', item.section.office.shortName],
                  headerStyle: { fontWeight: 500, textAlign: 'left', padding: '0.75rem' },
                  style: { paddingLeft: '1rem' },
                },
              ]}
              defaultSorted={[
                {
                  id: 'date',
                  desc: true,
                },
              ]}
            />
          )}
        </Searchable>
      </div>
    )
  }
}

export default compose(
  graphql(getSections, { name: 'sectionsData' }),
  graphql(getOffices, { name: 'officesData' }),
  graphql(updateSectionMutation),
  graphql(getDocuments, {
    name: 'documentsData',
    options: ({ contactId, organisationId }) => ({
      variables: { contactId, organisationId },
      notifyOnNetworkStatusChange: true,
    }),
  }),
)(SafeStorage)
