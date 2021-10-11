<template>
  <div>
    <label class="highlight">{{ title }}</label>
    <input
      type="number"
      v-model="text"
      @input="$emit('input', parseInt(text))"
      :disabled="disabled"
      :min="min"
      :max="max"
    />
  </div>
</template>

<script>
export default {
  props: ["title", "value", "disabled", "min", "max"],
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
input {
  border: 1px solid var(--gray-4);
  border-radius: 5px;
  margin: 16px 2px 32px 2px;
  padding: 8px 16px;
  width: calc(100% - 4px);
}
</style>
