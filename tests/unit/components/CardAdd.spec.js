import { mount } from "@vue/test-utils";
import CardAdd from "@/components/CardAdd";

describe("CardAdd", () => {
  it("Emite evento 'click'", () => {
    const wrapper = mount(CardAdd);

    const card = wrapper.find(".card-add");
    card.trigger("click");

    expect(wrapper.emitted().click).toBeTruthy();
  });
});
