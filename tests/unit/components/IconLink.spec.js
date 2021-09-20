import { mount } from "@vue/test-utils";
import IconLink from "@/components/IconLink";

describe("IconLink", () => {
  it("Permite evento 'click'", () => {
    const wrapper = mount(IconLink);

    const button = wrapper.find("button");
    button.trigger("click");

    expect(wrapper.emitted().click).toBeTruthy();
  });
});
