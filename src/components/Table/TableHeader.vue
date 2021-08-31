<template>
  <div class="header">
    <div class="row">
      <slot />
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style scoped>
.header {
  border-bottom: 1px solid var(--gray-4);
  border-top: 1px solid var(--gray-4);
  overflow-y: scroll;
  padding: 16px 0;
}
.row {
  display: flex;
  flex-direction: row;
  justify-self: space-between;
}
</style>