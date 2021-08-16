import { mount, createLocalVue } from '@vue/test-utils'
import store from '@/store';
import Vuex from 'vuex';
import Login from '@/views/Login.vue'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('Login.vue', () => {

  it('Carga la pantalla de Login.', () => {
    const wrapper = mount(Login, {
      localVue,
      store,
    })

    expect(wrapper.text()).toContain('Gestiona todos tus proyectos.')
  })

  it('Existe el botón de Iniciar Sesión.', () => {
    const wrapper = mount(Login, {
      localVue,
      store,
    })
    let button = wrapper.find("button")
    expect(button.text()).toBe("Iniciar Sesión");
  })

})
