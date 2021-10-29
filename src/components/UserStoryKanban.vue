<template>
  <div class="user-story" draggable="true" @dragstart="startDrag" @dragover.prevent>
    <div class="d-flex top">
      <div class="title">
        <span class="highlight">Pantalla de Login</span>
      </div>
      <div>
        <div class="d-flex">
          <span>8 hs.</span>&nbsp;&nbsp;
          <Icon icono="clock" size="16px"/>
        </div>
      </div>
    </div>
    <div>Asignado a: Panchito Lopez</div>
  </div>
</template>

<script>
import Icon from "@/components/Icon";

export default {
  components: {
    Icon
  },
  methods: {
    startDrag(evt) {
      const el = evt.target;
      setTimeout(() => {
        el.style.display = "none"
      }, 0)
      evt.dataTransfer.setData("element", el)
      evt.dataTransfer.effectAllowed = 'move'
      console.log("Drag Start")
    },
  }
}
</script>

<style lang="scss" scoped>
.user-story {
  height: 96px;
  padding: 16px;
  box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.25);
  margin-top: 8px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background-color: #fff;
  .top{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    .title {
      max-width: calc(100% - 50px);
    }
  }
}
</style>