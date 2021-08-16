<template>
  <button :class="colorTema" v-on:click="handleClick">{{ texto }}</button>
</template>

<script>
export default {
  props: { texto: String, tema: String },
  computed: {
    colorTema() {
      const tema = this.tema;
      return `${tema} h4`;
    },
  },
  methods: {
    handleClick() {
      this.$emit("click");
    },
  },
};
</script>

<style scoped>
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
</style>
