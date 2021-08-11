import { mount, createLocalVue } from '@vue/test-utils'
import store from '@/store';
import Vuex from 'vuex';
import Messages from '@/components/Messages.vue'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('Messages.vue', () => {

  it('Renders the component.', () => {
    const wrapper = mount(Messages, {
      localVue,
      store
    })

    expect(wrapper.text()).toContain('The data below')
  })

  it('Initial data values are empty.', () => {
    const wrapper = mount(Messages, {
      localVue,
      store
    })

    expect(wrapper.vm.subject).toContain('')
    expect(wrapper.vm.msgBody).toContain('')
  })

  it('Data changes when inputs are filled.', () => {
    const wrapper = mount(Messages, {
      localVue,
      store
    })

    wrapper.find('input[name=subject]').setValue('new message')
    wrapper.find('input[name=body]').setValue('message body')

    expect(wrapper.vm.subject).toBe('new message')
    expect(wrapper.vm.msgBody).toContain('message body')
  })

})
