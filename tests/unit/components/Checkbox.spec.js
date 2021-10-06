import { mount, createLocalVue } from "@vue/test-utils";
import store from "@/store";
import Vuex from "vuex";
import Checkbox from "@/components/Checkbox.vue";

const localVue = createLocalVue();
localVue.use(Vuex);

describe("Checkbox.vue", () => {
  it("Carga inicial de estado correctamente.", async () => {
    const wrapper = mount(Checkbox, {
      localVue,
      store,
      propsData: { value: true, disabled: false },
    });

    let checkbox = wrapper.find(".switch.active:not(disabled)");

    expect(checkbox.exists()).toBeTruthy();

    await wrapper.setProps({ value: false, disabled: true });

    checkbox = wrapper.find(".switch.disabled:not(active)");

    expect(checkbox.exists()).toBeTruthy();
  });

  it("Cambiar estado con un click.", async () => {
    const wrapper = mount(Checkbox, {
      localVue,
      store,
      propsData: { value: true, disabled: false },
    });

    const checkbox = wrapper.find(".switch");

    await checkbox.trigger("click");

    expect(wrapper.emitted().input[0][0]).toBe(false);
  });
});
