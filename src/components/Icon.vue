<template>
  <div
    :style="{
      backgroundColor: colorIcono,
      height: tamaño,
      mask: `url(${linkDelIcono}) no-repeat center / contain`,
      width: tamaño,
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
    tamaño() {
      return this.size ? this.size : "24px";
    },
  },
};
</script>

<style lang="scss" scoped></style>
