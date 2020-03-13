import React from 'react'

import Page from 'components/Page'
import ClientInvoiceValueChart from 'components/Reporting/ClientInvoiceValueChart'
import withData from 'lib/withData'
import withAuth from 'lib/withAuth'

const renderRefetchButton = onClick => (
  <button onClick={onClick} className="btn btn-info">
    Update
  </button>
)

class ClientInvoiceValuePage extends React.Component {
  state = { shouldRefetch: false }
  refetchData = () =>
    this.setState({ shouldRefetch: true }, () => this.setState({ shouldRefetch: false }))
  render() {
    return (
      <Page
        user={this.props.user}
        pageTitle="Client Invoice Value"
        renderRight={renderRefetchButton(this.refetchData)}
      >
        <ClientInvoiceValueChart shouldRefetch={this.state.shouldRefetch} />
      </Page>
    )
  }
}

export default withData(withAuth(ClientInvoiceValuePage))
