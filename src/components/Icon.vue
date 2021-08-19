<template>
  <div
    class="svg"
    :style="{
      backgroundColor: colorIcono,
      mask: `url(${linkDelIcono}) no-repeat center / contain`,
    }"
  ></div>
</template>

<script>
const iconosValidos = ["home", "key", "logout", "team"];

export default {
  props: { icono: String, color: String },
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
  },
};
</script>

<style lang="scss" scoped>
.svg {
  height: 24px;
  width: 24px;
}
</style>
