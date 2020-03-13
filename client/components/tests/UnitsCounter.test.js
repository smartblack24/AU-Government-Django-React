import React from 'react'
import renderer from 'react-test-renderer'
import UnitsCounter from '../UnitsCounter'

/* eslint-disable */
describe('UnitsCounter', () => {

  it('should render UnitsCounter with props', () => {
    const props = {
      unitsToday: 10,
      unitsWeek: 11,
      unitsMonth: 12,
    }
    const wrapper = renderer.create(
        <UnitsCounter
          user={props}
        />
    )
    expect(wrapper).toMatchSnapshot()
  })
})
