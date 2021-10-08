import { mount, createLocalVue } from "@vue/test-utils";
import store from "@/store";
import Vuex from "vuex";
import Counter from "@/components/Counter.vue";

const localVue = createLocalVue();
localVue.use(Vuex);

describe("Counter.vue", () => {
  it("Carga correctamente valor inicial.", async () => {
    const wrapper = mount(Counter, {
      localVue,
      store,
      propsData: { label: "prueba", value: 1, min: 0, max: 2 },
    });

    const contenedorValor = wrapper.find(".indicator .highlight");

    expect(contenedorValor.text()).toBe("1");
  });

  it("Pulsar '+' aumenta en una unidad el valor", async () => {
    const wrapper = mount(Counter, {
      localVue,
      store,
      propsData: { label: "prueba", value: 1, min: 0, max: 2 },
    });

    const btnAumentar = wrapper.find(".icon-container:nth-child(2)");

    console.log(btnAumentar.html());
  });
});
