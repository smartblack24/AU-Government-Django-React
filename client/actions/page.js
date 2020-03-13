import { LOADING_STATUS } from 'constants/page'

export const setLoadingStatus = (dataType, isLoading) => (
  {
    type: LOADING_STATUS,
    payload: { dataType, isLoading },
  }
)
