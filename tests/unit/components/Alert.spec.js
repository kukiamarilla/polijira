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

  it("Muestra la alerta con el tema proveido.", () => {
    const propsIniciales = {};

    let titulo = Alert.computed.title.call(propsIniciales);
    let icono = Alert.computed.icon.call(propsIniciales);
    let colorIcono = Alert.computed.iconColor.call(propsIniciales);

    // el tema (type) por defecto es error
    expect(titulo).toBe("Error");
    expect(icono).toBe("warning");
    expect(colorIcono).toBe("var(--danger)");

    let propsData = { type: "success" };

    titulo = Alert.computed.title.call(propsData);
    icono = Alert.computed.icon.call(propsData);
    colorIcono = Alert.computed.iconColor.call(propsData);

    expect(titulo).toBe("Éxito");
    expect(icono).toBe("success");
    expect(colorIcono).toBe("var(--success)");

    propsData = { type: "error" };

    titulo = Alert.computed.title.call(propsData);
    icono = Alert.computed.icon.call(propsData);
    colorIcono = Alert.computed.iconColor.call(propsData);

    expect(titulo).toBe("Error");
    expect(icono).toBe("warning");
    expect(colorIcono).toBe("var(--danger)");
  });
});
