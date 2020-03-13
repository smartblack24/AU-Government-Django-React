const express = require('express')
const next = require('next')

const port = parseInt(process.env.PORT, 10) || 3000
const host = process.env.HOST || 'localhost'
const dev = process.env.NODE_ENV !== 'production'
const app = next({ dev, dir: './client' })
const handle = app.getRequestHandler()

app.prepare().then(() => {
  const server = express()

  server.get('/profile/:id', (req, res) => {
    const actualPage = '/profile'
    const queryParams = { id: req.params.id }
    app.render(req, res, actualPage, queryParams)
  })

  server.get('/my-profile', (req,res) => {
    const actualPage = '/my-profile'
    app.render(req, res, actualPage, {})
  })

  server.get('/reset-password/:uid/:token', (req, res) => {
    const actualPage = '/reset-password'
    const queryParams = { uid: req.params.uid, token: req.params.token }
    app.render(req, res, actualPage, queryParams)
  })

  server.get('/invoices/add/:id', (req, res) => {
    const actualPage = '/addinvoice'
    const queryParams = { id: req.params.id }
    app.render(req, res, actualPage, queryParams)
  })

  server.get('/addinvoice', (req, res) => {
    res.status(404).send('Not found')
  })

  server.get('/addclient', (req, res) => {
    res.status(404).send('Not found')
  })

  server.get('/addtimeentry', (req, res) => {
    res.status(404).send('Not found')
  })

  server.get('/addcontact', (req, res) => {
    res.status(404).send('Not found')
  })

  server.get('/adddisbursement', (req, res) => {
    res.status(404).send('Not found')
  })

  server.get('/addorganisation', (req, res) => {
    res.status(404).send('Not found')
  })

  server.get('/addmatter', (req, res) => {
    res.status(404).send('Not found')
  })

  server.get('/addlead', (req, res) => {
    res.status(404).send('Not found')
  })

  server.get('/contacts/add', (req, res) => {
    app.render(req, res, '/addcontact', {})
  })

  server.get('/time-entries/add', (req, res) => {
    app.render(req, res, '/addtimeentry', {})
  })

  server.get('/clients/add', (req, res) => {
    app.render(req, res, '/addclient', {})
  })

  server.get('/organisations/add', (req, res) => {
    app.render(req, res, '/addorganisation', {})
  })

  server.get('/matters/add', (req, res) => {
    app.render(req, res, '/addmatter', {})
  })

  server.get('/leads/add', (req, res) => {
    app.render(req, res, '/addlead', {})
  })

  server.get('/disbursements/add', (req, res) => {
    app.render(req, res, '/adddisbursement', {})
  })

  server.get('/matter/:id', (req, res) => {
    const actualPage = '/matter'
    const queryParams = { id: req.params.id }
    app.render(req, res, actualPage, queryParams)
  })

  server.get('/lead/:id', (req, res) => {
    const actualPage = '/lead'
    const queryParams = { id: req.params.id }
    app.render(req, res, actualPage, queryParams)
  })

  server.get('/invoice/:id', (req, res) => {
    const actualPage = '/invoice'
    const queryParams = { id: req.params.id }
    app.render(req, res, actualPage, queryParams)
  })

  server.get('/disbursement/:id', (req, res) => {
    const actualPage = '/disbursement'
    const queryParams = { id: req.params.id }
    app.render(req, res, actualPage, queryParams)
  })

  server.get('/client/:id', (req, res) => {
    const actualPage = '/client'
    const queryParams = { id: req.params.id }
    app.render(req, res, actualPage, queryParams)
  })

  server.get('/time-entry/:id', (req, res) => {
    const actualPage = '/time-entry'
    const queryParams = { id: req.params.id }
    app.render(req, res, actualPage, queryParams)
  })

  server.get('/contact/:id', (req, res) => {
    const actualPage = '/contact'
    const queryParams = { id: req.params.id }
    app.render(req, res, actualPage, queryParams)
  })

  server.get('/organisation/:id', (req, res) => {
    const actualPage = '/organisation'
    const queryParams = { id: req.params.id }
    app.render(req, res, actualPage, queryParams)
  })

  server.get('*', (req, res) => {
    return handle(req, res)
  })

  server.listen(port, host, err => {
    if (err) throw err
    console.log(`> Ready on http://${host}:${port}`)
  })
})
