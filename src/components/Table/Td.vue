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
</style>