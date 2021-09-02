<template>
  <div
    :class="{ switch: true, active: value, disabled: disabled }"
    @click="toggle"
  >
    <div class="switch-background"></div>
    <div class="switch-control"></div>
  </div>
</template>

<script>
export default {
  props: ["value", "disabled"],
  methods: {
    toggle() {
      if (!this.disabled) this.$emit("input", !this.value);
    },
  },
};
</script>

<style scoped lang="scss">
.switch {
  position: relative;
  height: 20px;
  width: 60px;
  .switch-background {
    background-color: var(--danger);
    height: 16px;
    width: 50px;
    top: 2px;
    left: 5px;
    border-radius: 8px;
    position: absolute;
    transition: background-color 0.2s ease-in-out;
  }
  .switch-control {
    background-color: var(--gray-6);
    height: 20px;
    width: 20px;
    border-radius: 10px;
    box-shadow: 1px 0 4px rgba(0, 0, 0, 0.25);
    position: absolute;
    top: 0;
    left: 0px;
    transition: left 0.2s ease-in-out;
  }
  &.active {
    .switch-background {
      background-color: var(--success);
    }
    .switch-control {
      left: 40px;
    }
  }
  &:not(.disabled) {
    cursor: pointer;
  }
}
</style>