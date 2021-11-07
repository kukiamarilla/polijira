<template>
  <div :class="`modal ${modalState}`">
    <div class="modal-bg" v-on:click.self="$emit('input', false)">
      <div class="modal-box shadow" :style="getStyle">
        <div class="overflow-y-scroll h-100">
          <slot />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: { value: Boolean, height: String, width: String },
  computed: {
    modalState() {
      return this.value ? "show" : "";
    },
    getStyle() {
      const styles = {};

      styles.height = this.height ? this.height : "auto";
      styles.width = this.width ? this.width : "735px";

      return styles;
    },
  },
};
</script>

<style lang="scss" scoped>
.modal {
  display: none;
  &.show {
    display: block;
  }

  .modal-bg {
    align-items: flex-start;
    display: flex;
    background-color: rgba(0, 0, 0, 0.25);
    height: 100vh;
    justify-content: center;
    left: 0;
    padding: 50px;
    position: fixed;
    top: 0;
    width: 100vw;
    z-index: 3;
  }

  .modal-box {
    background-color: white;
    border-radius: 20px;
    padding: 40px;
    z-index: 2;
  }
}
</style>
