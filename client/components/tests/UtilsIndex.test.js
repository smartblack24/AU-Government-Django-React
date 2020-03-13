import React from 'react'
import renderer from 'react-test-renderer'
import {
  formatDate,
  normalizeCurrency,
  onlyNumbers,
  normalizePhone,
  capitalize,
  Tab,
  getGstStatusDisplay,
  getBillableStatusDisplay,
  getNominatedTypeDisplay,
  formatCurrency,
  getEntryType,
  parseCurrency,
  Select,
  Textarea
} from '../../utils/index.js'

/* eslint-disable */
describe('utils', () => {

  it('should render result of formatDate with empty data', () => {
    const date = ''
    const result = renderer.create(
      <div>{formatDate(date)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of formatDate with alphabet data', () => {
    const date = 'qwe'
    const result = renderer.create(
      <div>{formatDate(date)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of formatDate with 4 digits data', () => {
    const date = '1208'
    const result = renderer.create(
      <div>{formatDate(date)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of formatDate with 8 digits data', () => {
    const date = '12082018'
    const result = renderer.create(
      <div>{formatDate(date)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of formatDate with 12 digits data', () => {
    const date = '120820181122'
    const result = renderer.create(
      <div>{formatDate(date)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of formatDate with digits and alphabet data', () => {
    const date = '1208qwe2018'
    const result = renderer.create(
      <div>{formatDate(date)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of normalizeCurrency with empty data', () => {
    const value = ''
    const result = renderer.create(
      <div>{normalizeCurrency(value)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of normalizeCurrency with 1 digit data', () => {
    const value = '1'
    const result = renderer.create(
      <div>{normalizeCurrency(value)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of normalizeCurrency with 3 digit data', () => {
    const value = '123'
    const result = renderer.create(
      <div>{normalizeCurrency(value)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of normalizeCurrency with 3 digit and alphabet data', () => {
    const value = '1qwe23'
    const result = renderer.create(
      <div>{normalizeCurrency(value)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of onlyNumbers with 3 digit and alphabet data', () => {
    const value = '1qwe23'
    const result = renderer.create(
      <div>{onlyNumbers(value)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of onlyNumbers with empty data', () => {
    const value = ''
    const result = renderer.create(
      <div>{onlyNumbers(value)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of normalizePhone with empty data', () => {
    const value = ''
    const previousValue = ''
    const result = renderer.create(
      <div>{normalizePhone(value, previousValue)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of normalizePhone with 4 and 5 length value data', () => {
    const value = '12345'
    const previousValue = '1234'
    const result = renderer.create(
      <div>{normalizePhone(value, previousValue)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of normalizePhone with 8 and 9 length value data', () => {
    const value = '12345678'
    const previousValue = '1234567'
    const result = renderer.create(
      <div>{normalizePhone(value, previousValue)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of normalizePhone with 9 and 10 length value data', () => {
    const value = '123456789'
    const previousValue = '12345678'
    const result = renderer.create(
      <div>{normalizePhone(value, previousValue)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of normalizePhone with 11 and 12 length value data', () => {
    const value = '1234567890'
    const previousValue = '123456789'
    const result = renderer.create(
      <div>{normalizePhone(value, previousValue)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of normalizePhone with 12 and 13 length value data', () => {
    const value = '12345678901'
    const previousValue = '1234567890'
    const result = renderer.create(
      <div>{normalizePhone(value, previousValue)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of capitalize empty data', () => {
    const value = ''
    const result = renderer.create(
      <div>{capitalize(value)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of capitalize string data', () => {
    const value = 'qwe'
    const result = renderer.create(
      <div>{capitalize(value)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of capitalize with few words data', () => {
    const value = 'qwe qwe'
    const result = renderer.create(
      <div>{capitalize(value)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of Tab with empty data', () => {
    const result = renderer.create(
      <Tab />
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of Tab with data', () => {
    const onClick = jest.fn()
    const result = renderer.create(
      <Tab
        number={1}
        currentNumber={2}
        onClick={onClick}
        children={"Children"}
      />
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of Tab with data', () => {
    const onClick = jest.fn()
    const result = renderer.create(
      <Tab
        number={1}
        currentNumber={1}
        onClick={onClick}
        disabled={true}
        children={"Children"}
      />
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of getGstStatusDisplay with status 1 data', () => {
    const status = 1
    const result = renderer.create(
      <div>{getGstStatusDisplay(status)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of getGstStatusDisplay with status 2 data', () => {
    const status = 2
    const result = renderer.create(
      <div>{getGstStatusDisplay(status)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of getGstStatusDisplay with status 3 data', () => {
    const status = 3
    const result = renderer.create(
      <div>{getGstStatusDisplay(status)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of getGstStatusDisplay with status invalid data', () => {
    const status = 5
    const result = renderer.create(
      <div>{getGstStatusDisplay(status)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of getBillableStatusDisplay with status 1 data', () => {
    const status = 1
    const result = renderer.create(
      <div>{getBillableStatusDisplay(status)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of getBillableStatusDisplay with status 2 data', () => {
    const status = 2
    const result = renderer.create(
      <div>{getBillableStatusDisplay(status)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of getBillableStatusDisplay with status invalid data', () => {
    const status = 5
    const result = renderer.create(
      <div>{getBillableStatusDisplay(status)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of getNominatedTypeDisplay with status 1 data', () => {
    const status = 1
    const result = renderer.create(
      <div>{getNominatedTypeDisplay(status)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of getNominatedTypeDisplay with status 2 data', () => {
    const status = 2
    const result = renderer.create(
      <div>{getNominatedTypeDisplay(status)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of getNominatedTypeDisplay with status 3 data', () => {
    const status = 3
    const result = renderer.create(
      <div>{getNominatedTypeDisplay(status)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of getNominatedTypeDisplay with status 4 data', () => {
    const status = 4
    const result = renderer.create(
      <div>{getNominatedTypeDisplay(status)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of getNominatedTypeDisplay with status 5 data', () => {
    const status = 5
    const result = renderer.create(
      <div>{getNominatedTypeDisplay(status)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of getNominatedTypeDisplay with status 6 data', () => {
    const status = 6
    const result = renderer.create(
      <div>{getNominatedTypeDisplay(status)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of getNominatedTypeDisplay with status 7 data', () => {
    const status = 7
    const result = renderer.create(
      <div>{getNominatedTypeDisplay(status)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of getNominatedTypeDisplay with status invalid data', () => {
    const status = 0
    const result = renderer.create(
      <div>{getNominatedTypeDisplay(status)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of formatCurrency with empty data', () => {
    const value = ''
    const result = renderer.create(
      <div>{formatCurrency(value)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of formatCurrency with 1 digit data', () => {
    const value = '1'
    const result = renderer.create(
      <div>{formatCurrency(value)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of formatCurrency with 2 digit data', () => {
    const value = '12'
    const result = renderer.create(
      <div>{formatCurrency(value)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of formatCurrency with 3 digit data', () => {
    const value = '123'
    const result = renderer.create(
      <div>{formatCurrency(value)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of formatCurrency with 6 digit data', () => {
    const value = '123456'
    const result = renderer.create(
      <div>{formatCurrency(value)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of getEntryType with type empty data', () => {
    const value = ''
    const result = renderer.create(
      <div>{getEntryType(value)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of getEntryType with type 1 data', () => {
    const value = 1
    const result = renderer.create(
      <div>{getEntryType(value)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of getEntryType with type 2 data', () => {
    const value = 2
    const result = renderer.create(
      <div>{getEntryType(value)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of getEntryType with type invalid data', () => {
    const value = 12
    const result = renderer.create(
      <div>{getEntryType(value)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of parseCurrency with type empty data', () => {
    const value = ''
    const result = renderer.create(
      <div>{parseCurrency(value)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of parseCurrency with type some data', () => {
    const value = 123
    const result = renderer.create(
      <div>{parseCurrency(value)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of parseCurrency with type invalid data', () => {
    const value = '12qw12'
    const result = renderer.create(
      <div>{parseCurrency(value)}</div>
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of Select with empty data', () => {
    const result = renderer.create(
      <Select />
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of Select with props data', () => {
    const props = {
      onChange: jest.fn(),
      children: <option>Test option</option>
    }
    const result = renderer.create(
      <Select props={props} />
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of Textarea without data', () => {
    const result = renderer.create(
      <Textarea />
    )
    expect(result).toMatchSnapshot()
  })

  it('should render result of Textarea with props data', () => {
    const props = {
      className: "form-control",
      name: 'name',
      onChange: jest.fn(),
    }
    const result = renderer.create(
      <Textarea
        props={props}
      />
    )
    expect(result).toMatchSnapshot()
  })

})
