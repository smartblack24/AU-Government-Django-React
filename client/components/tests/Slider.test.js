import React from 'react'
import renderer from 'react-test-renderer'
import Slider from '../Slider'

/* eslint-disable */
describe('Slider', () => {

  it('should render Slider without data', () => {
    const wrapper = renderer.create(
        <Slider />
    )
    expect(wrapper).toMatchSnapshot()
  })

  it('should render Slider with data initialState(close)', () => {
    const wrapper = renderer.create(
        <Slider
          id="first"
          children={<h1>TEST</h1>}
          title="Test title"
        />
    )
    expect(wrapper).toMatchSnapshot()
  })

  it('should render Slider with data initialState(hidden)', () => {
    const wrapper = renderer.create(
        <Slider
          id="first"
          children={<h1>TEST</h1>}
          title="Test title"
          initialState="hidden-xs-up"
        />
    )
    expect(wrapper).toMatchSnapshot()
  })
})
