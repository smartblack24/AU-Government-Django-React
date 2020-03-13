import Immutable from 'immutable'
import { LOGIN_SUCCESS, LOGOUT_SUCCESS } from 'constants/user'

const initialState = Immutable.Map({
  isAuthenticated: false,
})

export default (state = initialState, action) => {
  switch (action.type) {
    case LOGIN_SUCCESS:
      return state.set('isAuthenticated', true).merge(Immutable.fromJS(action.payload))
    case LOGOUT_SUCCESS:
      return state.set('isAuthenticated', false)
    default:
      return state
  }
}
