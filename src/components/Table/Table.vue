<template>
  <div class="table">
    <slot />
  </div>
</template>

<script>
export default {};
</script>

<style lang="scss" scoped>
.table {
  --space-between-rows: 12px;
  --space-between-columns: 36px;
  height: 300px;
}
</style>
