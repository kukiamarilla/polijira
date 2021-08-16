import { mount, createLocalVue } from '@vue/test-utils'
import store from '@/store';
import Vuex from 'vuex';
import Boton from '@/components/Boton.vue'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('Boton.vue', () => {

  it('Al dar click se emite el evento.', () => {
    const wrapper = mount(Boton, {
      localVue,
      store,
    })
    let button = wrapper.find('button');
    button.trigger('click');
    expect(wrapper.emitted()['click']).toBeTruthy();
  })

})
