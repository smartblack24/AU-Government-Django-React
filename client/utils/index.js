import React, { Fragment } from 'react'
import ReactAutocomplete from 'react-autocomplete'
import $ from 'jquery'
import { filter, sortBy } from 'lodash'
import moment from 'moment'
import swal from 'sweetalert'

export const cookies = (headers) => {
  const result = {}
  if (headers.cookie) {
    const cookieStrings = headers.cookie.split('; ')
    for (let i = 0; i < cookieStrings.length; i += 1) {
      const cookieKeyValue = cookieStrings[i].split('=')
      result[cookieKeyValue[0]] = cookieKeyValue[1]
    }
  }
  return result
}

export const formatDate = (value) => {
  if (!value) {
    return ''
  }

  let result = value.replace(/[^\d]/g, '')

  if (result.length >= 3) {
    result = result.replace(/([\d]{2})/, '$1/')
  }
  if (result.length >= 6) {
    result = result.replace(/([\d]{2})\/([\d]{2})/, '$1/$2/')
  }
  if (result.length >= 10) {
    result = result.replace(/([\d]{2})\/([\d]{2})\/([\d]{4}).*/, '$1/$2/$3')
  }

  return result
}

export const normalizeCurrency = (value) => {
  const stringCurrency = value.toString()

  return Number(stringCurrency.replace(/[^0-9.-]+/g, ''))
}

export const onlyNumbers = (value) => {
  if (!value) {
    return value
  }

  return value.toString().replace(/[^\d]/g, '')
}

export const removeAlert = (instanceId, instanceType, update, successText, mutate) =>
  swal({
    title: 'Confirmation',
    text: 'Are you sure?',
    icon: 'warning',
    buttons: {
      cancel: true,
      confirm: {
        closeModal: false,
      },
    },
  }).then((willDelete) => {
    if (willDelete) {
      mutate({
        variables: {
          instanceId,
          instanceType,
        },
        update,
      }).then((response) => {
        if (response.data.removeInstance.errors.length > 0) {
          const msg = response.data.removeInstance.errors.join('\n')
          swal({ text: msg, icon: 'error' })
        } else {
          swal({
            icon: 'success',
            text: successText,
          })
        }
      })
    }
  })

export const normalizePhone = (value, previousValue) => {
  if (!value) {
    return value
  }
  const onlyNums = value.replace(/[^\d]/g, '')
  if (!previousValue || value.length > previousValue.length) {
    // typing forward
    if (onlyNums.length === 4) {
      return `${onlyNums}-`
    }
    if (onlyNums.length === 7) {
      return `${onlyNums.slice(0, 4)}-${onlyNums.slice(4)}-`
    }
  }
  if (onlyNums.length <= 4) {
    return onlyNums
  }
  if (onlyNums.length <= 7) {
    return `${onlyNums.slice(0, 4)}-${onlyNums.slice(4)}`
  }
  return `${onlyNums.slice(0, 4)}-${onlyNums.slice(4, 7)}-${onlyNums.slice(7, 10)}`
}

export const capitalize = str => str.charAt(0).toUpperCase() + str.slice(1)

export class Autocomplete extends React.PureComponent {
  static defaultProps = {
    menuStyle: {},
    loading: false,
    className: 'form-control',
    clearButton: true,
    clearButtonStyle: {},
    loadingSpinnerStyle: {},
  }
  constructor(props) {
    super(props)

    this.state = {
      value: props.initialValue || '',
    }

    this.getItemValue = this.props.getItemValue || this.getItemValue
  }
  componentWillReceiveProps(nextProps) {
    if (nextProps.initialValue !== this.props.initialValue) {
      this.setState({ value: nextProps.initialValue })
    }
  }
  getItemValue = item => item[this.props.itemAccessor]
  shouldItemRender = (item, query) => {
    const str = this.getItemValue(item)
    const searchResult = query.split(' ').map((q) => {
      if (str.toLowerCase().includes(q.toLowerCase())) {
        return true
      }

      return false
    })

    for (let i = 0; i < searchResult.length; i += 1) {
      if (searchResult[i] !== true) {
        return false
      }
    }

    return true
  }
  handleChange = (event) => {
    if (this.props.onChange) {
      this.props.onChange(event.target.value)
    }
    this.setState({ value: event.target.value })
  }
  handleSelect = (value) => {
    const result = this.props.onSelect(value)
    if (result) {
      this.setState({ value: result })
    }
  }
  clearQuery = () => {
    const value = ''
    this.setState({ value })
    this.props.onChange(value)
  }
  renderItem = (item, isHighlighted) => (
    <div
      key={item.id}
      style={{ background: isHighlighted ? 'lightgray' : 'white', cursor: 'pointer', padding: 10 }}
    >
      {this.getItemValue(item)}
    </div>
  )
  render() {
    return (
      <div style={{ position: 'relative' }}>
        <ReactAutocomplete
          getItemValue={this.getItemValue}
          items={this.props.loading ? [] : this.props.items}
          renderItem={this.renderItem}
          inputProps={{
            className: this.props.className,
            placeholder: this.props.placeholder,
            style: { paddingRight: 30 },
            ...this.props.inputProps,
          }}
          shouldItemRender={this.shouldItemRender}
          value={this.state.value}
          onChange={this.handleChange}
          onSelect={this.handleSelect}
          wrapperStyle={{ width: '100%' }}
          menuStyle={{
            borderTop: '1px solid #80bdff',
            borderLeft: '1px solid #80bdff',
            borderRight: '1px solid #80bdff',
            borderBottom: '1px solid #80bdff',
            position: this.props.menuStyle.position || 'absolute',
            left: 0,
            top: 36,
            zIndex: 100,
            maxHeight: 220,
            overflow: 'scroll',
            ...this.props.menuStyle,
          }}
        />
        {this.props.clearButton &&
          this.state.value && (
            <i
              onClick={this.clearQuery}
              tabIndex="-1"
              role="button"
              className="fa fa-times clear"
            />
          )}
        {this.props.loading && <div className="spinner" />}
        <style jsx>{`
          .clear {
            position: absolute;
            top: ${this.props.clearButtonStyle.top || '10px'};
            right: ${this.props.clearButtonStyle.right || '15px'};
            cursor: pointer;
          }
          .clear:hover {
            color: red;
          }
          .disabled {
            pointer-events: none;
          }
          .spinner {
            position: absolute;
            top: ${this.props.loadingSpinnerStyle.top || '10px'};
            right: ${this.props.loadingSpinnerStyle.right || '15px'};
            -webkit-animation: Select-animation-spin 400ms infinite linear;
            -o-animation: Select-animation-spin 400ms infinite linear;
            animation: Select-animation-spin 400ms infinite linear;
            width: 16px;
            height: 16px;
            box-sizing: border-box;
            border-radius: 50%;
            border: 2px solid #ccc;
            border-right-color: #333;
            display: inline-block;
            vertical-align: middle;
          }
          @keyframes Select-animation-spin {
            to {
              transform: rotate(1turn);
            }
          }
          @-webkit-keyframes Select-animation-spin {
            to {
              -webkit-transform: rotate(1turn);
            }
          }
        `}</style>
      </div>
    )
  }
}

export const Tab = ({ number, currentNumber, onClick, children, disabled }) => {
  const _onClick = () => {
    onClick(number)
  }
  const stub = () => ({})
  return (
    <li className="nav-item">
      <a
        tabIndex={0}
        className={`nav-link ${currentNumber === number && 'active'} ${disabled && 'disabled'}`}
        role="tab"
        onClick={disabled ? stub : _onClick}
      >
        {children}
      </a>
      <style jsx>{`
        a {
          cursor: pointer;
        }
        a.disabled {
          cursor: not-allowed;
        }
        .disabled:hover {
          color: #868e96 !important;
        }
      `}</style>
    </li>
  )
}

export const flattenObject = (ob) => {
  const toReturn = {}

  Object.keys(ob).map((i) => {
    if (Object.prototype.hasOwnProperty.call(ob, i)) {
      if (typeof ob[i] === 'object') {
        const flatObject = flattenObject(ob[i])
        toReturn[`${i}`] = flatObject
        Object.keys(flatObject).map((x) => {
          if (Object.prototype.hasOwnProperty.call(flatObject, x)) {
            toReturn[`${i}.${x}`] = flatObject[x]
          }

          return toReturn
        })
      } else {
        toReturn[i] = ob[i]
      }
    }
    return toReturn
  })
  return toReturn
}

export const setHeight = () => {
  const width = window.innerWidth > 0 ? window.innerWidth : this.screen.width
  const topOffset = 70
  if (width < 1170) {
    $('body').addClass('mini-sidebar')
    $('.navbar-brand span').hide()
    $('.scroll-sidebar, .slimScrollDiv')
      .css('overflow-x', 'visible')
      .parent()
      .css('overflow', 'visible')
    $('.sidebartoggler i').addClass('ti-menu')
  } else {
    $('body').removeClass('mini-sidebar')
    $('.navbar-brand span').show()
    // $(".sidebartoggler i").removeClass("ti-menu");
  }

  let height = (window.innerHeight > 0 ? window.innerHeight : this.screen.height) - 1
  height -= topOffset
  if (height < 1) height = 1
  if (height > topOffset) {
    $('.page-wrapper').css('min-height', `${height}px`)
  }
}

export const renderInput = ({
  input,
  placeholder,
  type,
  meta,
  id,
  formGroup,
  className,
  disabled,
}) => (
  <div
    className={`${formGroup ? 'form-group' : ''} ${
      meta.touched && meta.error ? 'has-danger' : meta.touched && 'has-success'
    }`}
  >
    <input
      {...input}
      placeholder={placeholder}
      type={type}
      id={id}
      disabled={disabled}
      className={`${className || 'form-control'} ${
        meta.touched && meta.error ? 'form-control-danger' : ''
      } ${meta.warning ? 'form-control-warning' : 'form-control-success'}`}
    />
    <span className="help-block text-danger">
      <small style={{ color: '#D5B000' }}>{meta.warning && meta.warning}</small>
      <small>{meta.touched && meta.error && meta.error}</small>
    </span>
  </div>
)

renderInput.defaultProps = {
  formGroup: true,
  disabled: false,
  onClick: () => {},
}

export const renderSelect = props => (
  <div
    className={`${
      props.meta.touched && props.meta.error ? 'has-danger' : props.meta.touched && 'has-success'
    }`}
  >
    <select {...props.input} {...props} />
    <span className="help-block text-danger">
      <small>{props.meta.touched && props.meta.error && props.meta.error}</small>
    </span>
  </div>
)

export const renderTextarea = ({ input, style, placeholder, type, meta, id }) => (
  <div
    className={`form-group ${
      meta.touched && meta.error ? 'has-danger' : meta.touched && 'has-success'
    }`}
  >
    <textarea
      {...input}
      style={style}
      placeholder={placeholder}
      type={type}
      id={id}
      className="form-control"
    />
    <span className="help-block text-danger">
      <small>{meta.touched && meta.error && meta.error}</small>
    </span>
  </div>
)

export const renderAutocomplete = ({
  input,
  placeholder,
  meta,
  initialValue,
  items,
  disabled,
  getItemValue,
  menuStyle,
  onSelect,
  containerClassName,
  className,
  handleOnChange,
  loading,
  itemAccessor,
}) => (
  <div
    style={{ position: 'relative', overflow: 'visible' }}
    className={`${containerClassName || 'form-group'} ${
      meta.touched && meta.error ? 'has-danger' : meta.touched && 'has-success'
    }`}
  >
    <Autocomplete
      getItemValue={getItemValue}
      items={items}
      loading={loading}
      onSelect={onSelect}
      itemAccessor={itemAccessor}
      onChange={handleOnChange}
      clearButton={false}
      inputProps={{ ...input, disabled }}
      placeholder={placeholder}
      className={`${className || 'form-control'} ${
        meta.touched && meta.error ? 'form-control-danger' : 'form-control-success'
      }`}
      initialValue={initialValue}
      menuStyle={menuStyle}
    />
    <span className="help-block text-danger">
      <small>{meta.touched && meta.error && meta.error}</small>
    </span>
  </div>
)

renderAutocomplete.defaultProps = {
  disabled: false,
}

export const Input = (props) => {
  const handleOnChange = (event) => {
    let value = event.target.value

    if (props.normalize) {
      value = props.normalize(value)
    }
    if (props.format) {
      value = props.format(value)
    }

    props.onChange(value, props.name)
  }
  const { normalize, format, ...input } = props
  return <input {...input} onChange={handleOnChange} />
}

export const Textarea = (props) => {
  const handleOnChange = event => props.onChange(event.target.value, props.name)
  return <textarea {...props} onChange={handleOnChange} />
}

export const Select = (props) => {
  const handleOnChange = event => props.onChange(event.target.value, props.name)
  return (
    <select {...props} onChange={handleOnChange}>
      {props.children}
    </select>
  )
}

export const getGstStatusDisplay = (gstStatus) => {
  let gstStatusDisplay
  switch (parseInt(gstStatus, 10)) {
    case 1:
      gstStatusDisplay = 'GST (10%)'
      break

    case 2:
      gstStatusDisplay = 'GST Export (0%)'
      break

    case 3:
      gstStatusDisplay = 'BAS Excluded (0%)'
      break

    default:
      gstStatusDisplay = 'GST (10%)'
  }

  return gstStatusDisplay
}

export const getBillableStatusDisplay = (status) => {
  let billableStatusDisplay
  switch (parseInt(status, 10)) {
    case 1:
      billableStatusDisplay = 'Billable'
      break

    case 2:
      billableStatusDisplay = 'Non billable'
      break

    default:
      billableStatusDisplay = 'GST (10%)'
  }

  return billableStatusDisplay
}

export const getNominatedTypeDisplay = (type) => {
  let nominatedTypeDisplay
  switch (parseInt(type, 10)) {
    case 1:
      nominatedTypeDisplay = 'Executor'
      break

    case 2:
      nominatedTypeDisplay = 'Attorney'
      break
    case 3:
      nominatedTypeDisplay = 'Guardian'
      break
    case 4:
      nominatedTypeDisplay = 'Donee'
      break
    case 5:
      nominatedTypeDisplay = 'Substitute Decision Maker'
      break
    case 6:
      nominatedTypeDisplay = 'Beneficiary'
      break
    case 7:
      nominatedTypeDisplay = 'Other'
      break

    default:
      nominatedTypeDisplay = 'No Selection'
  }

  return nominatedTypeDisplay
}

export const closeModalWindow = () => $('#modalCloseButton').click()

export const toggleSideBar = () => {
  if ($('body').hasClass('mini-sidebar')) {
    $('body').trigger('resize')
    $('.scroll-sidebar, .slimScrollDiv')
      .css('overflow', 'hidden')
      .parent()
      .css('overflow', 'visible')
    $('body').removeClass('mini-sidebar')
    $('.navbar-brand span').show()
  } else {
    $('body').trigger('resize')
    $('.scroll-sidebar, .slimScrollDiv')
      .css('overflow-x', 'visible')
      .parent()
      .css('overflow', 'visible')
    $('body').addClass('mini-sidebar')
    $('.navbar-brand span').hide()
  }
}

export const formatCurrency = (number) => {
  const numberFormat = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' })

  return numberFormat.format(number)
}

export const randomColorHex = () => {
  const letters = '0123456789ABCDEF'
  let color = '#'
  for (let i = 0; i < 6; i += 1) {
    color += letters[Math.floor(Math.random() * 16)]
  }
  return color
}

export const confirmAlert = () =>
  swal({
    title: 'Confirmation',
    text: 'Are you sure?',
    icon: 'warning',
    buttons: {
      cancel: true,
      confirm: {
        closeModal: false,
      },
    },
  })

export const getEntryType = (entryType) => {
  if (entryType === 1) {
    return 'TimeEntry'
  }

  if (entryType === 2) {
    return 'Disbursement'
  }

  return 'FixedPriceItem'
}

export const parseCurrency = (currency) => {
  const stringCurrency = currency.toString()

  return Number(stringCurrency.replace(/[^0-9.-]+/g, ''))
}

export const swalCreator = ({ success, errors, successMsg, errorMsg }) => {
  const icon = success ? 'success' : 'error'
  let text

  if (success) {
    text = successMsg || 'Success'
  } else {
    text = errorMsg || errors.join('\n')
  }

  return swal({ icon, text })
}

export const deserializeParams = (queryString) => {
  let query = {} // eslint-disable-line

  if (!queryString || queryString === '') {
    return query
  }

  const questionIndex = queryString.indexOf('?')

  const pairs = (questionIndex === -1 ? queryString : queryString.substr(questionIndex + 1)).split('&')

  pairs.forEach(pair => { // eslint-disable-line
    const splits = pair.split('=')
    query[decodeURIComponent(splits[0])] = decodeURIComponent(splits[1] || '')
  })

  return query
}

export const getEmailContact = (name, address) => name || address

export const getEmailDate = date => moment(date).format('h:mm A MMM D, YYYY')

export const emailHeader = (name, orderBy, onClick) => {
  const desc = orderBy[0] === '-'
  const id = desc ? orderBy.substr(1) : orderBy

  return (
    <div
      className="d-flex justify-content-between"
      onClick={
        () => {
          if (onClick) {
            let newOrderBy
            if (id === name) {
              newOrderBy = `${desc ? '' : '-'}${name}`
            } else {
              newOrderBy = `-${name}`
            }
            onClick(newOrderBy)
          }
        }
      }
      role="presentation"
      style={{ cursor: 'pointer' }}
    >
      {capitalize(name)}
      {id === name && <i className={`mdi mdi-arrow-${desc ? 'down' : 'up'}-bold`} aria-hidden="true" /> }
    </div>
  )
}

export const MatterOptions = ({ matters }) => {
  const openMatters = sortBy(filter(matters, matter => matter.billableStatusDisplay === 'Open'), ['name'])
  const closedMatters = sortBy(filter(matters, matter => matter.billableStatusDisplay === 'Closed'), ['name'])
  const suspendedMatters = sortBy(filter(matters, matter => matter.billableStatusDisplay === 'Suspended'), ['name'])

  return (<Fragment>
    <option key={0} value={'no_matter'}>No matter</option>
    {openMatters.length > 0 &&
      <optgroup label="------------- Opened -----------">
        {openMatters.map(({ id, name }) => <option key={id} value={id}>{name}</option>)}
      </optgroup>
    }
    {closedMatters.length > 0 &&
      <optgroup label="------------- Closed -----------">
        {closedMatters.map(({ id, name }) => <option key={id} value={id}>{name}</option>)}
      </optgroup>
    }
    {suspendedMatters.length > 0 &&
      <optgroup label="------------- Suspended -----------">
        {suspendedMatters.map(({ id, name }) => <option key={id} value={id}>{name}</option>)}
      </optgroup>
    }
  </Fragment>)
}
