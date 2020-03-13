import React, { PureComponent, Fragment } from 'react'
import PropTypes from 'prop-types'
import ReactTable from 'react-table'
import checkboxHOC from 'react-table/lib/hoc/selectTable'

const CheckboxTable = checkboxHOC(ReactTable)

export default class EmailTable extends PureComponent {
  static contextTypes = {
    pageNumber: PropTypes.number.isRequired,
    totalPages: PropTypes.number.isRequired,
    items: PropTypes.array,
    fetchMoreData: PropTypes.func.isRequired,
    isLoading: PropTypes.bool.isRequired,
    updateSelection: PropTypes.func,
  }

  toggleSelection = (key) => {
    let selection = [...this.props.selection]
    const keyIndex = selection.indexOf(key)

    if (keyIndex >= 0) {
      selection = [
        ...selection.slice(0, keyIndex),
        ...selection.slice(keyIndex + 1),
      ]
    } else {
      selection.push(key)
    }

    this.props.updateSelection({ selection })
  }

  toggleAll = () => {
    const selectAll = !this.props.selectAll
    const selection = []

    if (selectAll) {
      const wrappedInstance = this.checkboxTable.getWrappedInstance()
      const currentRecords = wrappedInstance.getResolvedState().sortedData

      currentRecords.forEach((item) => {
        selection.push(item._original.id)
      })
    }

    this.props.updateSelection({ selectAll, selection })
  }

  isSelected = key => this.props.selection.includes(key)

  render() {
    const { isLoading, items, pageNumber, totalPages, fetchMoreData } = this.context
    const { selectAll } = this.props

    return (
      <Fragment>
        <CheckboxTable
          data={items}
          page={pageNumber}
          pages={totalPages}
          onPageChange={fetchMoreData}
          loading={isLoading}
          showPageJump={false}
          defaultPageSize={15}
          showPageSizeOptions={false}
          className="-striped -highlight"
          keyField="id"
          selectType="checkbox"
          selectAll={selectAll}
          isSelected={this.isSelected}
          toggleSelection={this.toggleSelection}
          toggleAll={this.toggleAll}
          ref={(r) => { this.checkboxTable = r }}
          getTrProps={() => ({
            style: { paddign: 0, backgroundColor: 'transparent', cursor: 'pointer' },
          })}
          getTheadThProps={() => ({
            style: { fontWeight: 500, padding: '0.5rem', textAlign: 'left' },
          })}
          {...this.props}
        />
        <style jsx>{`
          tr {
            cursor: pointer;
          }
          .autocomplete-item {
            cursor: pointer;
            padding: 10px;
          }
          .text-centered {
            text-align: center;
          }
          .with-padding {
            padding: 10px;
            cursor: pointer;
          }
        `}</style>
      </Fragment>
    )
  }
}
