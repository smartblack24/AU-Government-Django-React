import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { graphql } from 'react-apollo'
import { toast } from 'react-toastify'
import moment from 'moment'
import Page from 'components/Page'
import ContactForm from 'components/ContactForm'
import LoadSpinner from 'components/LoadSpinner'
import withData from 'lib/withData'
import withAuth from 'lib/withAuth'
import { getContact } from 'queries'

class Contact extends Component {
  static propTypes = {
    user: PropTypes.shape({
      id: PropTypes.string,
      photo: PropTypes.string,
      fullName: PropTypes.string,
      firstName: PropTypes.string,
      lastName: PropTypes.string,
    }).isRequired,
    data: PropTypes.shape({
      loading: PropTypes.bool.isRequired,
      contact: PropTypes.shape({
        id: PropTypes.string,
        photo: PropTypes.string,
        fullName: PropTypes.string,
        firstName: PropTypes.string,
        lastName: PropTypes.string,
      }),
    }),
  }

  static defaultProps = {
    data: {
      loading: true,
      contact: {},
    },
  }

  componentDidMount() {
    if (this.props.url.query.created) {
      toast.success('The changes have been saved!')
    }
  }

  render() {
    const { data, user } = this.props

    if (data.loading) {
      return (
        <Page user={user} pageTitle=" " wrappedByCard={false}>
          <LoadSpinner />
        </Page>
      )
    }

    const initialValues = {
      ...data.contact,
      dateOfBirth: data.contact.dateOfBirth && moment(data.contact.dateOfBirth).format('DDMMYYYY'),
      dateOfDeath: data.contact.dateOfDeath && moment(data.contact.dateOfDeath).format('DDMMYYYY'),
    }

    return (
      <Page user={user} pageTitle={data.contact.fullName} wrappedByCard={false}>
        <ContactForm initialValues={initialValues} buttonTitle="Save" />
      </Page>
    )
  }
}

export default withData(
  withAuth(
    graphql(getContact, {
      options: ({ url }) => ({
        variables: { id: url.query.id },
      }),
    })(Contact),
  ),
)
