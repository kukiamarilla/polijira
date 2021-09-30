<template>
  <div class="counter">
    <span>{{ label }}</span>
    <div
      class="icon-container"
      @click="$emit('input', typeof max && value + 1 > max ? value : value + 1)"
    >
      <Icon icono="add" color="var(--gray-2)" hover="#000" size="12px" />
    </div>
    <div class="indicator">
      <span class="highlight">{{ value }}</span>
    </div>
    <div
      class="icon-container"
      @click="$emit('input', typeof min && value - 1 < min ? value : value - 1)"
    >
      <Icon icono="minus" color="var(--gray-2)" hover="#000" size="12px" />
    </div>
  </div>
</template>

<script>
import Icon from "@/components/Icon";
export default {
  components: { Icon },
  props: ["label", "value", "min", "max"],
};
</script>

<style lang="scss" scoped>
.counter > * {
  display: block;
  margin: auto;
  margin-top: 16px;
}
span {
  text-align: center;
}
.icon-container {
  display: flex;
  justify-content: center;
  cursor: pointer;
}
.indicator {
  width: 32px;
  height: 32px;
  border-radius: 100%;
  background-color: var(--primary);
  display: flex;
  flex-direction: column;
  justify-content: center;
  span {
    color: #fff;
  }
}
</style>