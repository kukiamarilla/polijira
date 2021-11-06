<template>
  <div class="user-story" draggable="true" @dragstart="startDrag" @dragover.prevent @click="verSprintBacklog">
    <div class="d-flex top">
      <div class="title">
        <span class="highlight" >{{userStory.user_story.nombre}}</span>
      </div>
      <div>
        <div class="d-flex">
          <span>{{userStory.horas_estimadas}} hs.</span>&nbsp;&nbsp;
          <Icon icono="clock" size="16px" color="#000" hover="#000"/>
        </div>
      </div>
    </div>
    <div>Asignado a: {{userStory.desarrollador.miembro_proyecto.usuario.nombre}}</div>
    
  </div>
</template>

<script>
import Icon from "@/components/Icon";

export default {
  props: ["userStory"],
  components: {
    Icon,
  },
  methods: {
    startDrag(evt) {
      const el = evt.target;
      setTimeout(() => {
        el.style.display = "none"
      }, 0)
      evt.dataTransfer.setData("userStory", this.userStory.id)
      evt.dataTransfer.effectAllowed = 'move'
      console.log("Drag Start")
    },
    verSprintBacklog() {
      this.verUserStory = this.userStory;
    }
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