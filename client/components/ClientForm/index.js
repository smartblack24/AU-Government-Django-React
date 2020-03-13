import React from 'react'
import { connect } from 'react-redux'
import { destroy } from 'redux-form'

import { Tab } from 'utils'
import Details from './Details'
import Matters from './Matters'
import Leads from './Leads'

class ClientForm extends React.PureComponent {
  constructor(props) {
    super(props)

    this.state = {
      form: 1,
      availableForms: props.wizard ? [] : [1],
    }
  }
  componentWillUnmount() {
    this.props.dispatch(destroy('clientForm'))
  }
  selectForm = form =>
    this.setState({ form, availableForms: this.state.availableForms.concat(form) })
  render() {
    return (
      <div className="card">
        <ul className="nav nav-tabs profile-tab" role="tablist">
          <Tab number={1} currentNumber={this.state.form} onClick={this.selectForm}>
            Details
          </Tab>
          <Tab
            number={2}
            currentNumber={this.state.form}
            onClick={this.selectForm}
            disabled={this.props.addingMode}
          >
            Matters
          </Tab>
          <Tab
            number={3}
            currentNumber={this.state.form}
            onClick={this.selectForm}
            disabled={this.props.addingMode}
          >
            Leads
          </Tab>
        </ul>
        <div className="card-body">
          {this.state.form === 1 && (
            <Details
              editable={this.props.editable}
              addingMode={this.props.addingMode}
              onSubmit={this.props.onSubmit}
              initialValues={this.props.initialValues}
              buttonTitle={this.props.buttonTitle}
            />
          )}
          {this.state.form === 2 && (
            <Matters
              buttonTitle={this.props.buttonTitle}
              initialValues={this.props.initialValues}
            />
          )}
          {this.state.form === 3 && (
            <Leads
              buttonTitle={this.props.buttonTitle}
              initialValues={this.props.initialValues}
            />
          )}
        </div>
      </div>
    )
  }
}

ClientForm.defaultProps = {
  addingMode: false,
}

export default connect()(ClientForm)
