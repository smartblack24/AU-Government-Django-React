/* eslint-disable */
import { ApolloClient, createNetworkInterface, IntrospectionFragmentMatcher } from 'react-apollo'
import fetch from 'isomorphic-fetch'
import Cookies from 'js-cookie'
import { cookies as getCookies } from 'utils'
import { BACKEND_URL } from 'constants/page'
import introspectionQueryResultData from '../fragmentTypes.json'

let apolloClient = null

// Polyfill fetch() on the server (used by apollo-client)
if (!process.browser) {
  global.fetch = fetch
}

function create(headers) {
  const networkInterface = createNetworkInterface({
    uri: `${BACKEND_URL}/graphql/`, // Server URL (must be absolute)
  })

  networkInterface
    .use([
      {
        applyMiddleware(req, next) {
          if (!req.options.headers) {
            req.options.headers = {} // Create the header object if needed.
          }
          // get the authentication token from cookies if it exists
          let token = null
          if (headers) {
            token = getCookies(headers).token
          } else {
            token = Cookies.get('token')
          }
          req.options.headers.authorization = token ? `Bearer ${token}` : null
          next()
        },
      },
    ])
    .useAfter([
      {
        applyAfterware({ response }, next) {
          if (response.status === 401) {
            console.log('401 error')
          }
          next()
        },
      },
    ])

  let connectionsCount = 0

  const client = new ApolloClient({
    ssrMode: !process.browser, // Disables forceFetch on the server (so queries are only run once)
    networkInterface,
    dataIdFromObject: o => {
      if (o.id) {
        return `${o.__typename}-${o.id}`
      } else if (o.node) {
        return `${o.__typename}-${o.node.id}`
      } else if (o.cursor) {
        return `${o.__typename}-${o.cursor}`
      } else {
        connectionsCount++
        return `${o.__typename}-${connectionsCount}`
      }

      return o.__typename
    },
    fragmentMatcher: new IntrospectionFragmentMatcher({ introspectionQueryResultData }),
  })

  return client
}

export default function initApollo(headers = null) {
  // Make sure to create a new client for every server-side request so that data
  // isn't shared between connections (which would be bad)
  if (!process.browser) {
    return create(headers)
  }

  // Reuse client on the client-side
  if (!apolloClient) {
    apolloClient = create(headers)
  }

  return apolloClient
}
/* eslint-enable */
