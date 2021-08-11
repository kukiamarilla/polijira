import { mount, createLocalVue } from '@vue/test-utils'
import store from '@/store';
import Vuex from 'vuex';
import VueDemo from '@/components/VueDemo.vue'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('VueDemo.vue', () => {

  it('Renders the component.', () => {
    const wrapper = mount(VueDemo, {
      localVue,
      store
    })

    expect(wrapper.text()).toContain('Installed CLI Plugins')
  })

})
