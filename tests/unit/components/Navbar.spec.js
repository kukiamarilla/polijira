import { mount, createLocalVue } from '@vue/test-utils'
import store from '@/store';
import Vuex from 'vuex';
import Navbar from '@/components/Navbar.vue'
import Vue from 'vue';

const localVue = createLocalVue()
localVue.use(Vuex)

describe('Navbar.vue', () => {

  it('No se muestra el botón Cerrar Sesión si no está logueado.', () => {
    const wrapper = mount(Navbar, {
      localVue,
      store,
    })
    let button = wrapper.find('button');
    expect(button.exists()).toBe(false);
  })

  it('So se muestra el botón Cerrar Sesión si está logueado.', async () => {
    const wrapper = mount(Navbar, {
      localVue,
      store,
    })
    store.commit("auth/login")
    await Vue.nextTick();
    let button = wrapper.find('button');
    expect(button.exists()).toBe(true);
  })

})
