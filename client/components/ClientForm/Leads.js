import React from 'react'
import { reduxForm, Field, reset, change } from 'redux-form'
import { connect } from 'react-redux'
import { graphql, gql, compose } from 'react-apollo'
import { filter } from 'graphql-anywhere'
import moment from 'moment'

import Modal from 'components/Modal'
import LeadForm from 'components/LeadForm'
import { matterFragment, clientFragment } from 'fragments'
import { getNewMatterReports } from 'queries'
import { closeModalWindow, parseCurrency } from 'utils'
import doc from 'components/LeadForm/doc'

const createMatterMutation = gql`
  mutation createMatter($matterData: MatterInput!) {
    createMatter(matterData: $matterData) {
      errors
      matter {
        ...Matter
        entryType
        leadStatus
        leadStatusDisplay
        leadDate
      }
    }
  }
  ${matterFragment}
`

class Leads extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      loading: false,
      leadStatus: 0,
    }
  }
  handleMatterStatusChange = event =>
    this.setState({ leadStatus: parseInt(event.target.value, 10) })
  handleAddMatter = values =>
    new Promise(async (resolve) => {
      const { form, dispatch } = this.props

      const { data } = await this.props.mutate({
        variables: {
          matterData: filter(doc, {
            ...values,
            entryType: 2,
            budget: values.budget ? parseCurrency(values.budget) : 0,
          }),
        },
        refetchQueries: [{ query: getNewMatterReports }],
        update: (store, { data: { createMatter } }) => {
          const cache = store.readFragment({
            id: `ClientType-${form.id}`,
            fragment: clientFragment,
            fragmentName: 'Client',
          })

          cache.matters.edges = cache.matters.edges.concat({
            cursor: '',
            node: createMatter.matter,
            __typename: 'MatterType',
          })

          store.writeFragment({
            id: `ClientType-${form.id}`,
            fragment: clientFragment,
            fragmentName: 'Client',
            data: cache,
          })
        },
      })

      if (data.createMatter.errors.length > 0) {
        console.log(data.createMatter.errors)
      }

      dispatch(change('clientForm', 'matters', { edges: form.matters.edges }))

      closeModalWindow()
      resolve()
      dispatch(reset('leadForm'))
    })
  render() {
    const { leadStatus } = this.state
    const { form } = this.props
    const onlyMatters = form.matters.edges.filter(({ node }) => node.entryType === 2)
    let leads = onlyMatters.filter(({ node }) => node.leadStatus === leadStatus)
    if (leadStatus === 0) {
      leads = onlyMatters
    }
    return [
      <form key={1} className="form-horizontal">
        <Field component="input" type="hidden" name="matters" />
        <div className="col-md-12">
          <div className="form-group">
            <div className="row mb-3 justify-content-between">
              <div className="col col-auto form-inline">
                <label htmlFor="matterStatus" className="mr-1">
                  Lead status
                </label>
                <select
                  id="leadStatus"
                  value={leadStatus}
                  className="form-control"
                  onChange={this.handleMatterStatusChange}
                >
                  <option value={0}>All</option>
                  <option value={1}>To be contacted</option>
                  <option value={2}>Nurturing</option>
                  <option value={3}>Quoting</option>
                  <option value={4}>Waiting for response</option>
                  <option value={5}>Lost</option>
                </select>
              </div>
              <button
                type="button"
                className="btn btn-primary"
                data-toggle="modal"
                data-target="#leadFormModal"
              >
                Add
              </button>
            </div>
            <div className="table-responsive">
              <table className="table table-bordered table-striped">
                <thead>
                  <tr>
                    <th>Matters</th>
                    <th>Lead Status</th>
                  </tr>
                </thead>
                <tbody>
                  {leads.length > 0 ? (
                    leads.map(({ node }) => (
                      <tr key={node.id} className="node-item">
                        <td>
                          <a target="_blank" href={`/lead/${node.id}`}>
                            {node.name}
                          </a>
                        </td>
                        <td>{node.leadStatusDisplay}</td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td>No lead</td>
                      <td />
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </form>,
      <Modal
        key={3}
        id="leadFormModal"
        title="Add lead"
        size="lg"
        bodyStyle={{ padding: 0, height: 790 }}
      >
        <LeadForm
          wizard
          buttonTitle="Add lead"
          initialValues={{
            client: this.props.initialValues,
            conflictStatus: '1',
            billingMethod: 1,
            billableStatus: 1,
            matterType: {},
            createdDate: moment().format(),
          }}
          onSubmit={this.handleAddMatter}
        />
      </Modal>,
    ]
  }
}

export default compose(
  reduxForm({
    form: 'clientForm',
    destroyOnUnmount: false,
    enableReinitialize: true,
    keepDirtyOnReinitialize: true,
  }),
  connect(state => ({ form: state.form.clientForm.values })),
  graphql(createMatterMutation),
)(Leads)
