<template>
  <div class="kanban">
    <ColumnaKanban nombre="To Do" color="var(--info)" @receive="moverUserStory($event, 'T')">
      <UserStoryKanban v-for="us in sprintBacklog.filter(sb => sb.estado_kanban == 'T' )" :key="us.id" :userStory="us" @click.native="ver(us)"/>
    </ColumnaKanban>
    <ColumnaKanban nombre="Doing" color="var(--warning)" @receive="moverUserStory($event, 'D')">
      <UserStoryKanban v-for="us in sprintBacklog.filter(sb => sb.estado_kanban == 'D' )" :key="us.id" :userStory="us" @click.native="ver(us)"/>
    </ColumnaKanban>
    <ColumnaKanban nombre="Done" color="var(--success)" @receive="moverUserStory($event, 'N')">
      <UserStoryKanban v-for="us in sprintBacklog.filter(sb => sb.estado_kanban == 'N' )" :key="us.id" :userStory="us" @click.native="ver(us)"/>
    </ColumnaKanban>
    <VerSprintBacklog v-model="verUserStory" :userStory="userStorySelected"/>
  </div>
</template>

<script>
import UserStoryKanban from "@/components/UserStoryKanban";
import ColumnaKanban from "@/components/ColumnaKanban";
import VerSprintBacklog from "@/components/VerSprintBacklog";

import sprintService from "@/services/sprintService";
import userStoryService from "@/services/userStoryService";

export default {
  components: {
    ColumnaKanban,
    UserStoryKanban,
    VerSprintBacklog
  },
  data() {
    return{
      verUserStory: null,
      userStorySelected: null,
      sprintBacklog: []
    }
  },
  mounted() {
    this.load()
  },
  methods: {
    load() {
      sprintService.sprintBacklog(this.$route.params["idSprint"]).then(sb => {
        this.sprintBacklog = sb
      })
    },
    ver(us) {
      this.verUserStory = true;
      this.userStorySelected = us;
    },
    moverUserStory(id, estado) {
      console.log(id, estado)
      userStoryService.mover(id, estado).then(() => {
        this.load()
      })
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

</style>