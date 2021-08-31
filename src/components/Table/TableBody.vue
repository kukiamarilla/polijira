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
  max-height: 100%;
  overflow: scroll;
}
</style>