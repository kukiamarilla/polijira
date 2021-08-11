// https://docs.cypress.io/api/introduction/api.html

describe('Testing messages', () => {
  before(() => {
    cy.setupDB("create_message");
  })

  it('Visits the messages url', () => {
    cy.visit('/#/messages')
    cy.contains('p', 'The data below is added/removed from the SQLite Database using Django\'s ORM and Rest Framework.')
  })

  it('Gets data from database', () => {
    cy.visit('/#/messages')
    cy.contains('body', 'Test Message')
    cy.contains('body', 'This is a test message')
  })

  it('Deletes the message', () => {
    cy.visit('/#/messages')
    cy.intercept('DELETE', '/api/messages/1').as('getMessages')
    cy.get('input[value=Delete]').click()
    cy.wait('@getMessages')
    cy.contains('This is a test message').should('not.exist')
  })

  it('Creates new message', () => {
    cy.visit('/#/messages')
    cy.get('input[name=subject]').type('New Message')
    cy.get('input[name=body]').type('This is a new message')
    cy.get('input[value=Add]').click()
    cy.contains('body', 'New Message')
    cy.contains('body', 'This is a new message')
  })
})
