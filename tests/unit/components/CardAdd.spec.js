import { mount, createLocalVue } from "@vue/test-utils";
import store from "@/store";
import Vuex from "vuex";
import CardAdd from "@/components/CardAdd.vue";

const localVue = createLocalVue();
localVue.use(Vuex);

describe("CardAdd.vue", () => {
  it("Al dar click se emite el evento.", () => {
    const wrapper = mount(CardAdd, {
      localVue,
      store,
    });

    const card = wrapper.find(".card");
    card.trigger("click");

    expect(wrapper.emitted().click).toBeTruthy();
  });
});
