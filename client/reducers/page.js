import Immutable from 'immutable'
import {
  LOADING_STATUS,
  CLIENTS_LOADING_STATUS,
  MATTERS_LOADING_STATUS,
  TIME_ENTRIES_LOADING_STATUS,
  DISBURSEMENTS_LOADING_STATUS,
  FIXED_PRICE_ITEM_LOADING_STATUS,
} from 'constants/page'

const initialState = Immutable.Map({
  clientLoading: false,
})

export default (state = initialState, action) => {
  switch (action.type) {
    case LOADING_STATUS:
      return state.set(action.payload.dataType, action.payload.isLoading)

    case 'APOLLO_QUERY_RESULT': {
      switch (action.operationName) {
        case 'clients':
          return state.set(CLIENTS_LOADING_STATUS, false)
        case 'matters':
          return state.set(MATTERS_LOADING_STATUS, false)
        case 'matter':
          return state.set(MATTERS_LOADING_STATUS, false)
        case 'timeEntries':
          return state.set(TIME_ENTRIES_LOADING_STATUS, false)
        case 'disbursements':
          return state.set(DISBURSEMENTS_LOADING_STATUS, false)
        default:
          return state
      }
    }
    case 'APOLLO_MUTATION_RESULT': {
      switch (action.operationName) {
        case 'updateFixedPriceItem':
          return state.set(FIXED_PRICE_ITEM_LOADING_STATUS, false)
        case 'createFixedPriceItem':
          return state.set(FIXED_PRICE_ITEM_LOADING_STATUS, false)
        default:
          return state
      }
    }

    default:
      return state
  }
}
