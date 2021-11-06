<template>
  <div class="column">
    <div class="header" ref="header">
      <h4>{{nombre}}</h4>
    </div>
    <div 
      :class="{'user-stories-container': true, enter}" 
      @drop.prevent="finishDrag" 
      @dragover.prevent 
      @dragenter.prevent="enter = true" 
      @dragleave.prevent="enter = false"
    >
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  props: ["color", "nombre"],
  data() {
    return {
      enter: false
    }
  },
  mounted() {
    this.loadColor()
  },
  methods: {
    loadColor() {
      this.$refs.header.style.setProperty("--header-color", this.color)
    },
    finishDrag(evt) {
      this.enter = false
      const el = evt.dataTransfer.getData("element")
      el.style.display = "block"
      evt.target.appendChild(el)
      console.log("Drag End")
    },
  }
}
</script>

<style lang="scss" scoped>
.header {
  --header-color: #000
}
.column{
  display: flex;
  flex-direction: column;
  width: calc(100% / 3 - 32px / 3);
  .header {
    background-color: #fff;
    box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.25);
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    padding: 12px 40px;
    position: relative;
    overflow: hidden;
    h4 {
      color: var(--header-color)
    }
    &::before {
      content: "";
      position: absolute;
      left: 0;
      top: 0;
      height: 100%;
      width: 16px;
      background-color: var(--header-color);
    }
  }
}
.user-stories-container {
  min-height: 108px;
  display: flex;
  flex-direction: column;
  padding: 8px;
  &.enter{
    background-color: var(--gray-6);
  }
}
</style>