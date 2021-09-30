import { mount, createLocalVue } from "@vue/test-utils";
import Vuex from "vuex";

import store from "@/store";
import Alert from "@/components/Alert.vue";

const localVue = createLocalVue();
localVue.use(Vuex);

describe("Alert.vue", () => {
  it("Boton aceptar cambia el estado de la alerta en el store.", async () => {
    const wrapper = mount(Alert, {
      localVue,
      store,
    });

    wrapper.vm.$store.commit("alert/showAlert");

    expect(wrapper.vm.$store.state.alert.alert.show).toBe(true);

    const boton = wrapper.find("button");
    await boton.trigger("click");

    expect(wrapper.vm.$store.state.alert.alert.show).toBe(false);
  });
});
