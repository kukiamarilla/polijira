import { mount } from "@vue/test-utils";
import Alert from "@/components/Alert.vue";

describe("Alert.vue", () => {
  it("Activar la alerta", () => {
    const wrapper = mount(Alert, {
      propsData: {
        show: true,
        message: "",
        type: "",
      },
    });

    const container = wrapper.find(".modal");

    expect(container.isVisible()).toBe(true);
  });

  it("Ocultar al desactivar", () => {
    const wrapper = mount(Alert, {
      propsData: {
        show: false,
        message: "",
        type: "",
      },
    });

    const container = wrapper.find(".modal");

    expect(container.isVisible()).toBe(false);
  });

  it("Muestra el mensaje usado", () => {
    const wrapper = mount(Alert, {
      propsData: {
        show: true,
        message: "un mensaje",
        type: "",
      },
    });

    expect(wrapper.html().includes("un mensaje")).toBe(true);
  });
});
