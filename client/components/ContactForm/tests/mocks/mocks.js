const occupations = [
  'Accountant',
  'Banker',
  'Barrister',
  'Builder',
  'Engineer',
  'Executive',
]

const clients = [
  'Mark Cox',
  'Ulian Node',
  'Barry Mich',
  'In Dus',
  'Eng Ineer',
  'Stu Idiot',
]

let newId = 0

const mocks = {
  Occupation: () => ({
    id: () => ++newId,
    name: () => occupations[newId % occupations.length],
    __typename: () => 'Occupation',
  }),

  ClientsEdge: () => ({
    cursor: 'Cursor line',
  }),

  Contact: () => ({
    id: () => ++newId,
    name: () => clients[newId % clients.length],
  }),

  Client: () => ({
    id: () => ++newId,
    name: () => clients[newId % clients.length],
    __typename: () => 'Client',
  }),
};

export default mocks;
