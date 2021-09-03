<template>
  <button :class="colorTema" v-on:click="handleClick" :style="{ width: ancho }">
    {{ texto }}
  </button>
</template>

<script>
export default {
  props: { texto: String, tema: String, width: String },
  computed: {
    colorTema() {
      const tema = this.tema;
      return `${tema} h4`;
    },
    ancho() {
      return this.width ? this.width : "auto";
    },
  },
  methods: {
    handleClick() {
      this.$emit("click");
    },
  },
};
</script>

<style lang="scss" scoped>
$primary: var(--primary);
$success: var(--success);
button {
  border: none;
  border-radius: 2rem;
  cursor: pointer;
  padding: 0.4375rem 2.65625rem;
}

.primary {
  color: white;
  background-color: var(--primary-light);
}

.primary:hover {
  background-color: var(--primary);
}

.primary:active {
  background-color: var(--primary-dark);
}

.secondary {
  color: black;
  background-color: white;
}

.secondary:hover {
  background-color: #eee;
}

.secondary:active {
  background-color: #ddd;
}
.success {
  color: white;
  background-color: var(--success);
}

.success:hover {
  background-color: darken(#6be78d, 20%);
}

.success:active {
  background-color: darken(#6be78d, 20%);
}
</style>
