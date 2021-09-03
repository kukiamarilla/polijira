<template>
  <div class="table" :style="{ height }">
    <slot />
  </div>
</template>

<script>
export default {
  props: ["height"],
};
</script>

<style lang="scss" scoped>
.table {
  --space-between-rows: 12px;
  --space-between-columns: 36px;
}
</style>
