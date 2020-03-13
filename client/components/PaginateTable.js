import React, { Fragment } from 'react'
import PropTypes from 'prop-types'
import ReactTable from 'react-table'
import Router from 'next/router'

const PaginateTable = (
  { detailPageAccessor, ...props },
  { isLoading, items, pageNumber, totalPages, fetchMoreData },
) => (
  <Fragment>
    <ReactTable
      data={items}
      page={pageNumber}
      pages={totalPages}
      onPageChange={fetchMoreData}
      loading={isLoading}
      showPageJump={false}
      defaultPageSize={15}
      showPageSizeOptions={false}
      headerStyle={{ display: 'none' }}
      className="-striped -highlight"
      getTrProps={() => ({
        style: { padding: 10, cursor: 'pointer' },
      })}
      getTheadThProps={() => ({
        style: { fontWeight: 500, textAlign: 'left', padding: '0.5rem' },
      })}
      getTdProps={(state, rowInfo) => ({
        style: { padding: 10 },
        onClick: () => {
          Router.push(
            `/${detailPageAccessor}?id=${rowInfo.original.id}`,
            `/${detailPageAccessor}/${rowInfo.original.id}`,
          )
        },
      })}
      {...props}
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

PaginateTable.propTypes = {
  detailPageAccessor: PropTypes.string.isRequired,
}

PaginateTable.contextTypes = {
  pageNumber: PropTypes.number.isRequired,
  totalPages: PropTypes.number.isRequired,
  items: PropTypes.array,
  fetchMoreData: PropTypes.func.isRequired,
  isLoading: PropTypes.bool.isRequired,
}

export default PaginateTable
