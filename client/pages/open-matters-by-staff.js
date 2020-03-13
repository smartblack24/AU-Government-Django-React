import React from 'react'

import Page from 'components/Page'
import OpenMatterByStaffChart from 'components/Reporting/OpenMattersByStaffChart'
import withData from 'lib/withData'
import withAuth from 'lib/withAuth'


const OpenMatterByStaff = ({ user }) => (
  <Page user={user} pageTitle="Open matters by Staff by Status"><OpenMatterByStaffChart /></Page>
)

export default withData(withAuth(OpenMatterByStaff))
