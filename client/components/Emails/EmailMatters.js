import React, { PureComponent } from 'react'
import PropTypes from 'prop-types'
import { Modal, ModalBody, ModalHeader } from 'reactstrap'
import { compose, gql, graphql } from 'react-apollo'
import { uniqBy } from 'lodash'
import Button from 'components/Button'
import LoadSpinner from 'components/LoadSpinner'
import withData from 'lib/withData'
import { MatterOptions, swalCreator } from 'utils'

class EmailMatters extends PureComponent {
  static propTypes = {
    selection: PropTypes.arrayOf(PropTypes.string),  //eslint-disable-line
    toggleModal: PropTypes.func,
  }

  constructor(props) {
    super(props)

    this.state = {
      selectedMatter: 'no_matter',
    }
  }

  get uniqMatters() {
    const { availableMattersOfMails } = this.props.data

    if (!availableMattersOfMails || availableMattersOfMails.length === 0) {
      return []
    }

    const matters = availableMattersOfMails.reduce((acc, { availableMatters }) => {
      acc = acc.concat(availableMatters)
      return acc
    }, [])

    return uniqBy(matters, 'id')
  }


  handleMatterChange = (evt) => {
    this.setState({ selectedMatter: evt.target.value })
  }

  handleUpdateMailsMatter = async () => {
    const { selection } = this.props
    const { selectedMatter } = this.state
    const res = await this.props.updateMailsMatter({ variables: { mails: selection, matterId: selectedMatter } })
    const { success, errors } = res.data.updateMailsMatter

    const successMsg = selectedMatter === 'no_matter' ? 'Successfully removed matter from selected emails' : 'Successfully set matter on selected emails'

    swalCreator({ success, errors, successMsg }).then(this.props.toggleModal)
  }

  renderComponents = () => {
    const { data } = this.props
    const matters = this.uniqMatters

    if (data.loading) {
      return <LoadSpinner margin="small" />
    } else if (matters.length > 0) {
      return (
        <div>
          <select className="form-control w-50" style={{ height: 'auto' }} onChange={this.handleMatterChange}>
            <MatterOptions matters={matters} />
          </select>
          <Button title="Save" className="btn btn-success ml-3" onClick={this.handleUpdateMailsMatter} />
        </div>
      )
    }
    return <div>No matters to select</div>
  }

  render() {
    const { isOpen, toggleModal } = this.props

    return (
      <Modal key={3} size="lg" isOpen={isOpen} toggle={toggleModal}>
        <ModalHeader toggle={toggleModal} className="email-modal-header" style={{ padding: '1.25rem calc(1.25rem + 15px)' }}>
          Update matter
        </ModalHeader>
        <ModalBody>
          <div className="card-body" style={{ position: 'relative' }}>
            {this.renderComponents()}
          </div>
        </ModalBody>
      </Modal>
    )
  }
}

const getAvailableMattersOfMails = gql`
  query availableMattersOfMails($mails: [ID]!) {
    availableMattersOfMails(mails: $mails) {
      availableMatters {
        id
        name
        billableStatusDisplay
      }
    }
  }
`

const updateMailsMatter = gql`
  mutation updateMailsMatter($mails: [ID]!, $matterId: String!) {
    updateMailsMatter(mails: $mails, matterId: $matterId) {
      success
      errors
    }
  }
`

export default withData(
  compose(
    graphql(getAvailableMattersOfMails, {
      options: ({ selection }) => ({
        variables: { mails: selection },
        fetchPolicy: 'cache-and-network',
      }),
    }),
    graphql(updateMailsMatter, { name: 'updateMailsMatter' }),
  )(EmailMatters),
)
