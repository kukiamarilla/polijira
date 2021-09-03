// https://docs.cypress.io/api/introduction/api.html

describe('Testing Flujo de Login', () => {

  it('Visita la pagina de login sin estar logueado', () => {
    cy.visit('/#/login')
    cy.contains('h2', 'Gestiona todos tus proyectos')
  })
  it('Redirecciona a login si no está logueado', () => {
    cy.visit('/#/no-activado')
    cy.contains('h2', 'Gestiona todos tus proyectos')
  })
  // it('Redirecciona a no activado si está logueado', () => {
  //   localStorage.setItem("session", "true")
  //   cy.visit('/#/login')
  //   cy.contains('h1', 'Has iniciado sesión.')
  // })
  // it('Visita la pagina de login estando logueado', () => {
  //   localStorage.setItem("session", "true")
  //   cy.visit('/#/no-activado')
  //   cy.contains('h1', 'Has iniciado sesión.')
  // })
})
