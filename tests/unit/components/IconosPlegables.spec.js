import { mount } from "@vue/test-utils";
import IconosPlegables from "@/components/IconosPlegables";

describe("IconosPlegables", () => {
  let wrapper;

  beforeEach(() => {
    wrapper = mount(IconosPlegables);
  });

  it("Inicialmente, solo muestra icono de opciones", () => {
    expect(wrapper.vm.altura).toBe("48px");
  });

  it("Click inicial muestra opciones", () => {
    const btnOpciones = wrapper.find(".btn-icon:first-child");
    btnOpciones.trigger("click");

    expect(wrapper.vm.altura).toBe("128px");
  });

  it("Ocultar clickendo de nuevo a icono de opciones", () => {
    const btnOpciones = wrapper.find(".btn-icon:first-child");
    btnOpciones.trigger("click");
    btnOpciones.trigger("click");

    expect(wrapper.vm.altura).toBe("48px");
  });

  it("Click en el boton 'ver' emite evento 'clickWatch'", async () => {
    const botonVer = wrapper.find(".btn-icon:nth-child(2)");

    await botonVer.trigger("click");

    expect(wrapper.emitted().clickWatch).toBeTruthy();
  });

  it("Oculta boton 'ver' via estado", async () => {
    await wrapper.setProps({ hideWatch: true });

    const botonVer = wrapper.find(".btn-icon:nth-child(2) > div");

    expect(botonVer.exists()).toBe(false);
  });

  it("Click en el boton 'eliminar' emite evento 'clickDelete'", async () => {
    const botonVer = wrapper.find(".btn-icon:nth-child(3)");

    await botonVer.trigger("click");

    expect(wrapper.emitted().clickDelete).toBeTruthy();
  });

  it("Oculta boton 'eliminar' via estado", async () => {
    await wrapper.setProps({ hideDelete: true });

    const botonEliminar = wrapper.find(".btn-icon:nth-child(3) > div");

    expect(botonEliminar.exists()).toBe(false);
  });
});
