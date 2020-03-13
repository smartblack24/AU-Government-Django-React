import {
  makeExecutableSchema,
  addMockFunctionsToSchema,
} from 'graphql-tools';
import mocks from './mocks';


const typeDefs = `
  type Contact {
    id: ID
    clients: ClientsConnection
    secondClients: ClientsConnection
  }

  type Client {
    id: ID
    name: String
  }

  type ClientsConnection {
    edges: [ClientsEdge]
    totalCount: Int
  }

  type ClientsEdge {
    cursor: String!
    node: Client
  }

  type Occupation {
    id: ID
    name: String
  }

  type Occupations {
    occupations: [Occupation]
  }

  type Query {
    client: Client
    occupation: Occupation
    occupations: [Occupation]
    clients: [Client]
    contact(id:ID!): Contact
    clientsConnection: ClientsConnection
  }

  schema {
    query: Query
  }
`

const schema = makeExecutableSchema({
  typeDefs,
})

addMockFunctionsToSchema({
  schema,
  mocks,
  preserveResolvers: true,
})

export default schema;
