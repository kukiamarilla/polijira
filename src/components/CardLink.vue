<template>
  <div
    :class="{ card: true, shadow: true, resaltado: resaltado }"
    @mouseover="hover"
    @mouseout="blur"
    @click="redirigir"
  >
    <Icon :icono="icono" :color="colorIcono" size="78px" />
    <h2>{{ titulo }}</h2>
  </div>
</template>

<script>
import Icon from "@/components/Icon";

export default {
  components: { Icon },
  props: {
    titulo: String,
    link: String,
    icono: String,
    resaltado: Boolean,
  },
  data() {
    return {
      colorIcono: "",
    };
  },
  mounted() {
    this.colorIcono = this.resaltado ? "white" : "black";
  },
  methods: {
    hover() {
      this.colorIcono = "white";
    },
    blur() {
      this.colorIcono = this.resaltado ? "white" : "black";
    },
    redirigir() {
      if (this.link) this.$router.push(this.link);
    },
  },
};
</script>

<style lang="scss" scoped>
.card {
  align-items: center;
  border-radius: 20px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  height: 226px;
  padding: 32px 16px;
  position: relative;
  width: 276px;

  &.resaltado {
    background-color: var(--success);
    color: white;
  }

  &:hover,
  &.resaltado:hover {
    background-color: var(--primary);
    color: white;
  }
}

h2 {
  padding-top: 32px;
  text-align: center;
}
</style>
