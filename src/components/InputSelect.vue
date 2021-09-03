<template>
  <div class="input-container">
    <slot />
  </div>
</template>

<script>
export default {};
</script>

<style scoped>
.input-container {
  border: 1px solid var(--gray-4);
  border-radius: 5px;
  margin: 16px 0 32px 0;
  padding: 8px 16px;
}
</style>
