// https://docs.cypress.io/api/introduction/api.html

describe('Testing Homepage', () => {

  it('Visits the homepage url', () => {
    cy.visit('/#/')
    cy.contains('h3', 'Installed CLI Plugins')
  })

})
