import { mount, createLocalVue } from "@vue/test-utils";
import Vuex from "vuex";
import Vue from "vue";

import store from "@/store";
import App from "@/App.vue";

const localVue = createLocalVue();
localVue.use(Vuex);

describe("App.vue", () => {
  it("Muestra la alerta cuando cambie el estado de la alerta en el store.", async () => {
    const wrapper = mount(App, {
      localVue,
      store,
    });

    expect(wrapper.html().includes("esto es una prueba")).toBe(false);

    store.commit("alert/showAlert", { message: "esto es una prueba" });

    await Vue.nextTick();

    expect(wrapper.html().includes("esto es una prueba")).toBe(true);
  });
});
