<template>
  <div :style="{ width }">
    <slot />
  </div>
</template>

<script>
export default {
  props: ["width"],
};
</script>

<style scoped>
div {
  font-weight: bold;
}
</style>