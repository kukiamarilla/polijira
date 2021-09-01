<template>
  <div class="body">
    <slot />
  </div>
</template>

<script>
export default {};
</script>

<style scoped>
.body {
  padding-top: var(--space-between-rows);
  max-height: calc(100% - 50px);
  overflow: scroll;
}
</style>