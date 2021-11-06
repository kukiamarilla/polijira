<template>
  <div>
    <div class="d-flex tab-header">
        <h4 v-for="tab in tabs" :key="tab.name" :class="{selector: true, active: tabSelected == tab.name}" @click="tabSelected = tab.name">{{tab.title}}</h4>
    </div>
    <hr>
    <div class="tab-content">
        <template v-for="tab in tabs">
          <div :key="tab.name" class="tab-body" v-if="tabSelected == tab.name">
              <slot :name="tab.name"></slot>
          </div>
        </template>
    </div>
  </div>
</template>

<script>
export default {
  props: ["tabs", "default"],
  data() {
    return {
      tabSelected: this.default
    }
  }
}
</script>

<style lang="scss" scoped>

.tab-header h4{
    margin-right: 16px;
    color: var(--gray-4);
    cursor: pointer;
    &.active {
        color: #000;
    }
}
hr{
    margin-top: 20px;
    color: var(--gray-4);
    border-top: 0;
}
.tab-body {
    padding: 16px 0;
}
</style>