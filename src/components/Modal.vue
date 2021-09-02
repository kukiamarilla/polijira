<template>
  <div :class="`modal ${modalState}`">
    <div class="modal-bg" v-on:click.self="$emit('close')">
      <div
        class="modal-box shadow"
        :style="{ height: getHeight, width: getWidth }"
      >
        <slot />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: { show: Boolean, height: String, width: String },
  computed: {
    modalState() {
      return this.show ? "show" : "";
    },
    getHeight() {
      return this.height ? this.height : "auto";
    },
    getWidth() {
      return this.width ? this.width : "735px";
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
