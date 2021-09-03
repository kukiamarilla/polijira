import { mount, createLocalVue } from '@vue/test-utils'
import store from '@/store';
import Vuex from 'vuex';
import Navbar from '@/components/Navbar.vue'
import Vue from 'vue';

const localVue = createLocalVue()
localVue.use(Vuex)

describe('Navbar.vue', () => {

  it('No se muestra el botón Cerrar Sesión si mostrarLogout no es true.', () => {
    const wrapper = mount(Navbar, {
      localVue,
      store,
    })
    let button = wrapper.find('button');
    expect(button.exists()).toBe(false);
  })

  it('Se muestra el botón Cerrar Sesión si mostrarLogout es true.', async () => {
    const wrapper = mount(Navbar, {
      localVue,
      store,
      propsData: {
        mostrarLogout: true
      }
    })
    store.commit("auth/login")
    await Vue.nextTick();
    let button = wrapper.find('button');
    expect(button.exists()).toBe(true);
  })

})
