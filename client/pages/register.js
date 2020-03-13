import React from 'react'

import withPreloader from 'lib/withPreloader'
import RegisterForm from 'components/RegisterForm'

export default withPreloader(() => (
  <section id="wrapper">
    <div className="login-register" style={{ backgroundColor: '#F8F8F8' }}>
      <div className="login-box card">
        <div className="card-body">
          <RegisterForm />
        </div>
      </div>
    </div>
  </section>
))
