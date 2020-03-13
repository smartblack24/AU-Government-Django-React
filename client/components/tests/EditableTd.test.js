import React from 'react'
import renderer from 'react-test-renderer'
import EditableTd from '../../utils/EditableTd'

/* eslint-disable */
describe('EditableTd', () => {

  it('should render EditableTd with props', () => {
    const props = {
      fieldName: 'Test text',
      onChange: jest.fn(),
      children: 1,
    }
    const wrapper = renderer.create(
        <EditableTd
          fieldName={props.fieldName}
          onChange={props.onChange}
          children={props.children}
        />
    )
    expect(wrapper).toMatchSnapshot()
  })
})
