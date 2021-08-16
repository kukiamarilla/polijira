import { mount, createLocalVue } from '@vue/test-utils'
import store from '@/store';
import Vuex from 'vuex';
import MenuSemiCirculoDerecho from '@/components/MenuSemiCirculoDerecho.vue'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('MenuSemiCirculoDerecho.vue', () => {

  it('Al dar click se emite el evento.', () => {
    const wrapper = mount(MenuSemiCirculoDerecho, {
      localVue,
      store,
    })
    let button = wrapper.find('button');
    button.trigger('click');
    expect(wrapper.emitted()['login']).toBeTruthy();
  })

})
