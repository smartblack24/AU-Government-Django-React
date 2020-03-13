import React from 'react'
import Head from 'next/head'
import moment from 'moment'
import Picker from 'react-month-picker'

import withData from 'lib/withData'
import withAuth from 'lib/withAuth'
import Page from 'components/Page'
import AverageInvoiceReport from 'components/Reporting/AverageInvoiceReport'

class AverageInvoicePage extends React.Component {
  state = {
    fromDate: moment().startOf('year'),
    toDate: moment().endOf('year'),
    mrange: { from: { year: moment().year(), month: 1 }, to: { year: moment().year(), month: 12 } },
    monthRangeValue: `January ${moment().year()} - December ${moment().year()}`,
  }
  handleMonthRangeFocus = () => this.pickAMonth.show()
  handleMonthRangeDismiss = (mrange) => {
    const fromDate = moment().month(mrange.from.month - 1).year(mrange.from.year)
    const toDate = moment().month(mrange.to.month - 1).year(mrange.to.year)
    const monthRangeValue = `${fromDate.format('MMMM YYYY')} - ${toDate.format('MMMM YYYY')}`

    this.setState({ mrange, fromDate, toDate, monthRangeValue })
    this.child.refetchData({
      fromDate: fromDate.format('MM/DD/YYYY'),
      toDate: toDate.format('MM/DD/YYYY'),
    })
  }
  createChildRef = (element) => {
    this.child = element
  }
  render() {
    const pickerLang = {
      months: ['Jan', 'Feb', 'Mar', 'Spr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
      from: 'From',
      to: 'To',
    }
    const { mrange } = this.state
    const fromDate = moment().month(mrange.from.month - 1).year(mrange.from.year)
    const toDate = moment().month(mrange.to.month - 1).year(mrange.to.year)
    return (
      <Page user={this.props.user} pageTitle="Average Invoice report">
        <Head>
          <link rel="stylesheet" href="/static/css/month-picker.css" />
        </Head>
        <div className="row mb-sm-3 justify-content-start">
          <div className="col col-md-auto">
            <Picker
              ref={(ref) => { this.pickAMonth = ref; }}
              range={this.state.mrange}
              years={{ min: 2000 }}
              lang={pickerLang.months}
              onDismiss={this.handleMonthRangeDismiss}
            >
              <input
                type="text"
                style={{ minWidth: 300, opacity: 1 }}
                onFocus={this.handleMonthRangeFocus}
                className="form-control"
                readOnly
                value={this.state.monthRangeValue}
              />
            </Picker>
          </div>
        </div>
        <AverageInvoiceReport
          fromDate={fromDate}
          toDate={toDate}
          onRef={this.createChildRef}
        />
      </Page>
    )
  }
}

export default withData(withAuth(AverageInvoicePage))
