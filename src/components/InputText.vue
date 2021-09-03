<template>
  <div>
    <label class="highlight">{{ title }}</label>
    <input type="text" v-model="text" @input="$emit('input', text)" />
  </div>
</template>

<script>
export default {
  props: ["title", "value"],
  data() {
    return {
      text: this.value,
    };
  },
  watch: {
    value() {
      this.text = this.value;
    },
  },
};
</script>

<style lang="scss" scoped>
input[type="text"] {
  border: 1px solid var(--gray-4);
  border-radius: 5px;
  margin: 16px 0 32px 0;
  padding: 8px 16px;
  width: 100%;
}
</style>