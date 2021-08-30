<template>
  <div
    :style="{
      backgroundColor: colorIcono,
      height: tamanho,
      mask: `url(${linkDelIcono}) no-repeat center / contain`,
      width: tamanho,
    }"
  ></div>
</template>

<script>
const iconosValidos = [
  "home",
  "key",
  "logout",
  "team",
  "add",
  "options",
  "watch",
  "delete",
  "check",
];

export default {
  props: { icono: String, color: String, size: String },
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
    tamanho() {
      return this.size ? this.size : "24px";
    },
  },
};
</script>

<style lang="scss" scoped></style>
