<template>
  <div class="user-story" v-show="!hide" draggable="true" @dragstart="startDrag" @dragover.prevent @dragend="dropped">
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
    <div class="d-flex justify-content-space-between">
      <span v-if="userStory.desarrollador">Asignado a: {{userStory.desarrollador.miembro_proyecto.usuario.nombre}}</span>
      <span v-else>Asignado a:<span class="text-danger" > Nadie</span></span>
      <span class="text-danger" v-if="userStory.user_story.estado == 'C'">Cancelado</span>
      <span class="text-success" v-if="userStory.user_story.estado == 'R'">Lanzado</span>
    </div>
    
  </div>
</template>

<script>
import Icon from "@/components/Icon";

export default {
  props: ["userStory"],
  data() {
    return {
      hide: false
    };
  },
  components: {
    Icon,
  },
  methods: {
    startDrag(evt) {
      setTimeout(() => {
        this.hide = true;
      }, 0)
      evt.dataTransfer.setData("userStory", this.userStory.id)
      evt.dataTransfer.effectAllowed = 'move'
    },
    dropped() {
      this.$emit("dropped")
      setTimeout(() => {
        this.hide = false;
      }, 500)
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