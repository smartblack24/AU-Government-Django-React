import { getMatters, getClient } from 'queries'

const storageKey = 'redux-tab-sync'
const sourceId = Math.floor(Math.random() * 10000)

function wrapAction(action) {
  return {
    action,
    sourceId,
    time: Date.now(),
  }
}

export function storageMiddleware() {
  return () => next => (action) => {
    const wrappedAction = wrapAction(action)

    if (process.browser) {
      // eslint-disable-next-line
      localStorage.setItem(storageKey, JSON.stringify(wrappedAction))
    }

    next(action)
  }
}

export function createOnStorage(store, client) {
  return () => {
    // eslint-disable-next-line
    const wrappedAction = JSON.parse(localStorage.getItem(storageKey))

    if (
      wrappedAction.action.type.indexOf('RESULT') > -1 &&
      wrappedAction.action.operationName === 'matters'
    ) {
      try {
        const data = client.readQuery({ query: getMatters })

        data.matters = wrappedAction.action.result.data.matters

        client.writeQuery({ query: getMatters, data })
      } catch (e) {} // eslint-disable-line
    }
    if (
      wrappedAction.action.type.indexOf('RESULT') > -1 &&
      wrappedAction.action.operationName === 'removeMatter'
    ) {
      try {
        if (wrappedAction.action.result.data.removeInstance.errors.length === 0) {
          const data = client.readQuery({ query: getMatters })

          const index = data.matters.findIndex(
            m => m.id === wrappedAction.action.variables.instanceId,
          )

          if (index > -1) {
            data.matters = data.matters
              .slice(0, index)
              .concat(data.matters.slice(index + 1, data.matters.length))
          }

          client.writeQuery({ query: getMatters, data })
        }
      } catch (e) {} // eslint-disable-line
    }
    if (
      wrappedAction.action.type.indexOf('RESULT') > -1 &&
      wrappedAction.action.operationName === 'createMatter'
    ) {
      try {
        const data = client.readQuery({
          query: getClient,
          variables: { id: wrappedAction.action.variables.clientId },
        })

        data.client.matters.push(wrappedAction.action.result.data.createMatter.matter)

        client.writeQuery({
          query: getClient,
          variables: { id: wrappedAction.action.variables.clientId },
          data,
        })
      } catch (e) {} // eslint-disable-line
    }
  }
}
