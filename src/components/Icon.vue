<template>
  <div
    :style="{
      '--hovercolor': hoverColor,
      '--color': colorIcono,
      height: tamanho,
      mask: `url(${linkDelIcono}) no-repeat center / contain`,
      width: tamanho,
    }"
  ></div>
</template>

<script>
const iconosValidos = [
  "add",
  "box",
  "card",
  "check",
  "clock",
  "delete",
  "edit",
  "flag",
  "home",
  "key",
  "logout",
  "minus",
  "options",
  "protected",
  "success",
  "team",
  "warning",
  "watch",
];

export default {
  props: { icono: String, color: String, size: String, hover: String },
  data() {
    return {
      iconos: iconosValidos,
    };
  },
  computed: {
    linkDelIcono() {
      const iconoValido = this.iconos.includes(this.icono);
      const linkIcono = iconoValido
        ? require(`@/assets/icons/${this.icono}.svg`)
        : "";

      return linkIcono;
    },
    colorIcono() {
      return this.color ? this.color : "currentColor";
    },
    hoverColor() {
      return this.hover ? this.hover : this.color;
    },
    tamanho() {
      return this.size ? this.size : "24px";
    },
  },
};
</script>

<style lang="scss" scoped>
div {
  background-color: var(--color);
  &:hover {
    background-color: var(--hovercolor);
  }
}
</style>
