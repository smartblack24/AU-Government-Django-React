import React from 'react'
import { reduxForm, Field, reset } from 'redux-form'
import { connect } from 'react-redux'
import { graphql, gql, compose } from 'react-apollo'
import { filter } from 'graphql-anywhere'
import moment from 'moment'

import Modal from 'components/Modal'
import MatterForm from 'components/MatterForm'
import { matterFragment, clientFragment } from 'fragments'
import { getNewMatterReports } from 'queries'
import { closeModalWindow, parseCurrency } from 'utils'
import doc from 'components/MatterForm/doc'

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

class Matters extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      loading: false,
      billableStatus: 1,
    }
  }
  handleMatterStatusChange = event =>
    this.setState({ billableStatus: parseInt(event.target.value, 10) })
  handleAddMatter = values =>
    new Promise(async (resolve) => {
      const { form, dispatch } = this.props

      const { data } = await this.props.mutate({
        variables: {
          matterData: filter(doc, {
            ...values,
            entryType: 1,
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

      // dispatch(change('clientForm', 'matters', { edges: matters }))

      closeModalWindow()
      resolve()
      dispatch(reset('matterForm'))
    })
  render() {
    const { billableStatus } = this.state
    const { form } = this.props
    const matters = form.matters.edges.filter(({ node }) => node.billableStatus === billableStatus)
    const onlyMatters = matters.filter(({ node }) => node.entryType === 1)
    return [
      <form key={1} className="form-horizontal">
        <Field component="input" type="hidden" name="matters" />
        <div className="col-md-12">
          <div className="form-group">
            <div className="row mb-3 justify-content-between">
              <div className="col col-auto form-inline">
                <label htmlFor="matterStatus" className="mr-1">
                  Matter status
                </label>
                <select
                  id="matterStatus"
                  value={billableStatus}
                  className="form-control"
                  onChange={this.handleMatterStatusChange}
                >
                  <option value={1}>Open</option>
                  <option value={2}>Suspended</option>
                  <option value={3}>Closed</option>
                </select>
              </div>
              <button
                type="button"
                className="btn btn-primary"
                data-toggle="modal"
                data-target="#matterFormModal"
              >
                Add
              </button>
            </div>
            <div className="table-responsive">
              <table className="table table-bordered table-striped">
                <thead>
                  <tr>
                    <th>Matters</th>
                    <th>Billable Status</th>
                  </tr>
                </thead>
                <tbody>
                  {onlyMatters.length > 0 ? (
                    onlyMatters.map(({ node }) => (
                      <tr key={node.id} className="node-item">
                        <td>
                          <a target="_blank" href={`/matter/${node.id}`}>
                            {node.name}
                          </a>
                        </td>
                        <td>{node.billableStatusDisplay}</td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td>No matters</td>
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
        key={2}
        id="matterFormModal"
        title="Add matter"
        size="lg"
        bodyStyle={{ padding: 0, height: 790 }}
      >
        <MatterForm
          wizard
          buttonTitle="Add matter"
          initialValues={{
            client: this.props.initialValues,
            conflictStatus: '1',
            billingMethod: '1',
            billableStatus: '1',
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
)(Matters)
