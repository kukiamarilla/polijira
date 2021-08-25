<template>
  <button :class="tema" v-on:click="handleClick">
    <Icon :icono="icono" />
    <span class="descripcion">{{ descripcion }}</span>
  </button>
</template>

<script>
import Icon from "@/components/Icon";

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
  },
  methods: {
    handleClick() {
      // go to {{ link }}
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

button > .descripcion {
  display: none;
}

button:hover > .descripcion {
  background-color: black;
  border-radius: 10px;
  color: white;
  cursor: auto;
  display: block;
  font-family: "Roboto";
  font-size: 12px;
  left: calc(100% + 8px);
  padding: 5px 0;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 109px;
}

.descripcion::before {
  background-color: black;
  content: "";
  height: 8px;
  left: 0;
  position: absolute;
  top: 50%;
  transform: translate(-45%, -50%) rotate(45deg);
  width: 8px;
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
