import React from 'react'
import PropTypes from 'prop-types'
import ClearableInputWrapper from 'components/ClearableInputWrapper'

class Searchable extends React.Component {
  static propTypes = {
    filterInputPlaceholder: PropTypes.string,
    searchableField: PropTypes.string,
    searchableFields: PropTypes.oneOfType([
      PropTypes.arrayOf(PropTypes.string),
      PropTypes.arrayOf(
        PropTypes.shape({
          name: PropTypes.string,
          type: PropTypes.oneOf(['string', 'number', 'date']),
        }),
      ),
    ]),
    data: PropTypes.shape({
      loading: PropTypes.bool.isRequired,
      refetch: PropTypes.func.isRequired,
    }).isRequired,
    dataKey: PropTypes.string.isRequired,
    changePage: PropTypes.func,
    fetchedPages: PropTypes.arrayOf(PropTypes.number),
    resetPages: PropTypes.func,
    manual: PropTypes.bool,
    value: PropTypes.string.isRequired,
    values: PropTypes.arrayOf(PropTypes.string.isRequired),
  }
  static defaultProps = {
    searchableFields: [],
    changePage: null,
    fetchedPages: [0],
    manual: false,
    filterInputPlaceholder: '',
    searchableField: null,
    resetPages: () => {},
    value: '',
    values: [],
  }
  constructor(props) {
    super(props)

    const values = {}
    props.searchableFields.map((field, index) => {
      const name = typeof field === 'string' ? field : field.name
      values[name] = props.values[index]
      return 0
    })

    this.state = {
      ...values,
      [props.searchableField]: props.value,
      fetchedPages: props.fetchedPages,
      pageNumber: 0,
      value: props.value,
    }
  }
  getChildContext() {
    const { data, dataKey } = this.props
    let items = []
    let totalPages = 1
    if (data[dataKey]) {
      items = data[dataKey].edges.map(item => item.node)
      totalPages = data[dataKey].totalPages
    }
    return {
      pageNumber: this.state.pageNumber,
      fetchMoreData: this.fetchMoreData,
      items,
      totalPages,
      isLoading: data.loading,
    }
  }
  changePage = pageNumber => this.setState({ pageNumber })
  resetData = (name) => {
    this.props.data.refetch({ [name]: null, after: '' })
  }
  handleOnChange = (value, name, minSymbols = 3) => {
    if (value && value.length >= minSymbols) {
      if (this.props.manual) {
        this.props.changePage(0)
      } else {
        this.changePage(0)
      }
      this.props.data.refetch({ [name]: value })
    } else if (!value) {
      this.resetData(name)
    }
    this.props.resetPages()
    this.setState({ [name]: value, fetchedPages: [0], pageNumber: 0 })
  }
  clearQuery = (name) => {
    this.setState({ [name]: '', fetchedPages: [0], pageNumber: 0 })
    this.props.resetPages()
    this.resetData(name)
  }
  fetchMoreData = (pageNumber) => {
    const { data, dataKey, manual, changePage } = this.props
    let fetchedPages = this.state.fetchedPages

    if (manual) {
      fetchedPages = this.props.fetchedPages
    }

    if (!fetchedPages.includes(pageNumber) && data[dataKey].pageInfo.hasNextPage) {
      data.fetchMore({
        variables: {
          after: data[dataKey].pageInfo.endCursor,
        },
        updateQuery: (previousResult, { fetchMoreResult }) => {
          if (!fetchMoreResult[dataKey]) {
            return previousResult
          }

          const previousEdges = previousResult[dataKey].edges
          const newEdges = fetchMoreResult[dataKey].edges
          const newPageInfo = fetchMoreResult[dataKey].pageInfo
          const previousPageInfo = previousResult[dataKey].pageInfo

          if (!manual) {
            this.setState({ fetchedPages: this.state.fetchedPages.concat(pageNumber) })
          }

          return {
            [dataKey]: {
              totalPages: fetchMoreResult[dataKey].totalPages,
              edges: [...previousEdges, ...newEdges],
              pageInfo: { ...previousPageInfo, ...newPageInfo },
              __typename: fetchMoreResult[dataKey].__typename,
            },
          }
        },
      })
    }

    if (manual) {
      changePage(pageNumber)
    } else {
      this.setState({ pageNumber })
    }
  }
  render() {
    const { filterInputPlaceholders, searchableField, searchableFields } = this.props
    if (searchableFields.length) {
      const filterComponents = searchableFields.map((field, index) => ({
        id: index,
        getComponent: () => {
          const name = typeof field === 'string' ? field : field.name
          const type = typeof field === 'string' ? 'string' : field.type

          return (
            <ClearableInputWrapper
              name={name}
              type={type}
              onChange={this.handleOnChange}
              value={this.state[name]}
              onClear={this.clearQuery}
              placeholder={filterInputPlaceholders[index]}
            />
          )
        },
      }))

      const props = { filterComponents }
      return this.props.children(props)
    }

    const filterComponent = (
      <ClearableInputWrapper
        name={searchableField}
        onChange={this.handleOnChange}
        value={this.state[searchableField]}
        onClear={this.clearQuery}
        placeholder={this.props.filterInputPlaceholder}
      />
    )
    const props = { filterComponent }
    return this.props.children(props)
  }
}

Searchable.childContextTypes = {
  pageNumber: PropTypes.number,
  totalPages: PropTypes.number,
  items: PropTypes.array,
  fetchMoreData: PropTypes.func,
  isLoading: PropTypes.bool,
}

export default Searchable
