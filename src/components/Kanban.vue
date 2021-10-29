<template>
  <div class="kanban">
      <div class="column todo">
        <div class="header">
          <h4>To Do</h4>
        </div>
        <div class="user-stories-container" @drop.prevent="finishDrag" @dragover.prevent>
          <div class="user-story" draggable="true" @dragstart="startDrag" @dragover.stop>
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
        </div>
      </div>
      <div class="column doing">
        <div class="header">
          <h4>Doing</h4>
        </div>
        <div class="user-stories-container"  @drop.prevent="finishDrag" @dragover.prevent></div>
      </div>
      <div class="column done">
        <div class="header">
          <h4>Done</h4>
        </div>
        <div class="user-stories-container"  @drop.prevent="finishDrag" @dragover.prevent></div>
      </div>
  </div>
</template>

<script>
import Icon from "@/components/Icon";

export default {
  data() {
    return{
      dragState: {
        columns: {
          todo: "inactive",
          doing: "inactive",
          done: "inactive",
        }
      }
    }
  },
  components: {
    Icon
  },
  methods: {
    startDrag(evt) {
      evt.dataTransfer.setData("US", "hola")
      evt.dataTransfer.effectAllowed = 'move'
      console.log("Drag Start")
    },
    finishDrag(evt) {
      const el = evt.dataTransfer.getData("US")
      console.log(el)
      console.log("Drag End")
    },
    dragEnter(column, evt) {
      if (evt.dataTransfer.types.includes['US']) {
        // Only handle cards.
        evt.preventDefault();
      }
      this.dragState = {...this.dragState, columns: {...this.dragState.columns, doing: "active"}};
    }
  }
}
</script>

<style lang="scss" scoped>
.kanban {
  display: flex;
  justify-content: space-between;
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
    &::before {
      content: "";
      position: absolute;
      left: 0;
      top: 0;
      height: 100%;
      width: 16px;
    }
  }
  &.todo .header{
    color: var(--info);
    &::before {
      background-color: var(--info);
    }
  }
  &.doing .header{
    color: var(--warning);
    &::before {
      background-color: var(--warning);
    }
  }
  &.done .header{
    color: var(--success);
    &::before {
      background-color: var(--success);
    }
  }
}
.user-story {
  height: 96px;
  padding: 16px;
  box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.25);
  margin-top: 8px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  .top{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    .title {
      max-width: calc(100% - 50px);
    }
  }
}

.user-stories-container {
  min-height: 108px;
  display: flex;
  flex-direction: column;
}

</style>