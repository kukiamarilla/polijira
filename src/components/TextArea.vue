<template>
  <div>
    <label class="highlight">{{ title }}</label>
    <textarea
      type="text"
      v-model="text"
      @input="$emit('input', text)"
      :disabled="disabled"
    ></textarea>
  </div>
</template>

<script>
export default {
  props: ["title", "value", "disabled"],
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
textarea {
  border: 1px solid var(--gray-4);
  border-radius: 5px;
  margin: 16px 2px 32px 2px;
  padding: 8px 16px;
  width: calc(100% - 4px);
  height: 96px;
}
</style>
