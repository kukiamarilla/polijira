<template>
  <button :class="tema" v-on:click="handleClick">
    <Icon :icono="icono" hover="#9480ff" />
    <Tooltip :texto="descripcion" direccion="derecha" />
  </button>
</template>

<script>
import Icon from "@/components/Icon";
import Tooltip from "@/components/Tooltip";
export default {
  props: { icono: String, link: String, activo: Boolean, descripcion: String },
  computed: {
    tema() {
      const activo = this.activo ? "activo" : "";

      return `${activo} h4`;
    },
  },
  components: {
    Icon,
    Tooltip,
  },
  methods: {
    handleClick() {
      if (this.link) this.$router.push(this.link);
      this.$emit("click");
    },
  },
};
</script>

<style scoped>
button {
  background-color: transparent;
  border: none;
  cursor: pointer;
  position: relative;
}

.icono {
  color: var(--gray-4);
}

.icono:hover {
  color: var(--primary-light);
}

.icono.activo {
  color: black;
}
</style>
