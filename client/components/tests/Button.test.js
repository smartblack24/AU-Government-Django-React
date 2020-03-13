import React from 'react'
import renderer from 'react-test-renderer'
import Button from '../Button'

/* eslint-disable */
describe('Button', () => {

  it('should render Button with some props', () => {
    const wrapper = renderer.create(
        <Button
          className="btn btn-success"
          onClick={jest.fn()}
          title="Text Button"
          type='button'
          style={{color: 'red'}}
          loading={false}
          disabled
        />
    )
    expect(wrapper).toMatchSnapshot()
  })

  it('should render Button with icon props', () => {
    const wrapper = renderer.create(
        <Button
          className="btn btn-success"
          onClick={jest.fn()}
          title="Text Button"
          type='button'
          icon="fa-plus"
          style={{color: 'red'}}
          loading={false}
          disabled
        />
    )
    expect(wrapper).toMatchSnapshot()
  })

  it('should render Button with icon and loading props', () => {
    const wrapper = renderer.create(
        <Button
          className="btn btn-success"
          onClick={jest.fn()}
          title="Text Button"
          type='button'
          icon="fa-plus"
          style={{color: 'red'}}
          loading={true}
          disabled
        />
    )
    expect(wrapper).toMatchSnapshot()
  })


  it('should render Button with loading props', () => {
    const wrapper = renderer.create(
        <Button
          className="btn btn-success"
          onClick={jest.fn()}
          title="Text Button"
          type='button'
          style={{color: 'red'}}
          loading={true}
          disabled
        />
    )
    expect(wrapper).toMatchSnapshot()
  })
})
