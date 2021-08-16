import { mount, createLocalVue } from '@vue/test-utils'
import store from '@/store';
import Vuex from 'vuex';
import NoActivado from '@/views/NoActivado.vue'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('NoActivado.vue', () => {

  it('Carga la pantalla de NoActivado.', () => {
    const wrapper = mount(NoActivado, {
      localVue,
      store,
    })

    expect(wrapper.text()).toContain('Has iniciado sesión.')
  })
})
