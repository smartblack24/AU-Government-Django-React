import React from 'react'
import renderer from 'react-test-renderer'
import Pre from '../Pre'

/* eslint-disable */
describe('Pre', () => {

  it('should render Pre without props', () => {
    const wrapper = renderer.create(
      <Pre />
    )
    expect(wrapper).toMatchSnapshot()
  })

  it('should render Pre with props', () => {
    const wrapper = renderer.create(
      <Pre children={"Test children"} />
    )
    expect(wrapper).toMatchSnapshot()
  })
})
