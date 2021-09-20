import { mount } from "@vue/test-utils";
import Checkbox from "@/components/Checkbox";

describe("Checkbox", () => {
  let wrapper;

  beforeEach(() => {
    wrapper = mount({
      data() {
        return { value: false, disabled: false };
      },
      template:
        "<div> <checkbox v-model='value' :disabled='disabled'></checkbox> </div>",
      components: { checkbox: Checkbox },
    });
  });

  it("Inicializacion correcta", () => {
    expect(wrapper.vm.value).toBe(false);
    expect(wrapper.vm.disabled).toBe(false);
  });

  it("Intercambia su valor con clicks", async () => {
    const input = wrapper.find(".switch");

    await input.trigger("click");
    expect(wrapper.vm.value).toBe(true);

    await input.trigger("click");
    expect(wrapper.vm.value).toBe(false);
  });

  it("Evita cambios si esta deshabilitado", async () => {
    await wrapper.setData({ value: false, disabled: true });

    const input = wrapper.find(".switch");

    console.log(input.vm.value, input.vm.disabled);

    await input.trigger("click");
    expect(wrapper.vm.value).toBe(false);
  });
});
