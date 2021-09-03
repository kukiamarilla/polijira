<template>
  <div class="row">
    <slot />
  </div>
</template>

<script>
export default {};
</script>

<style scoped>
.row {
  display: flex;
  padding-bottom: var(--space-between-rows);
  padding-top: var(--space-between-rows);
}
</style>