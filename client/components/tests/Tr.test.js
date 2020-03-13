import React from 'react'
import renderer from 'react-test-renderer'
import Tr from '../../utils/Tr'

/* eslint-disable */
describe('Tr', () => {

  it('should render Tr with props', () => {
    const props = {
      onClick: jest.fn(),
      children: (<th>test</th>)
    }
    const wrapper = renderer.create(
        <Tr
          props={props}
          onClick={jest.fn()}
        />
    )
    expect(wrapper).toMatchSnapshot()
  })

  it('should render Tr without props children', () => {
    const props = {
      onClick: jest.fn(),
      children: (<th>test</th>)
    }
    const wrapper = renderer.create(
        <Tr
          onClick={jest.fn()}
        />
    )
    expect(wrapper).toMatchSnapshot()
  })
})
