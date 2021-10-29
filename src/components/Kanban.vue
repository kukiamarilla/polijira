<template>
  <div class="kanban">
    <ColumnaKanban nombre="To Do" color="var(--info)">
      <UserStoryKanban/>
      <UserStoryKanban/>
      <UserStoryKanban/>
    </ColumnaKanban>
    <ColumnaKanban nombre="Doing" color="var(--warning)">
      <UserStoryKanban/>
    </ColumnaKanban>
    <ColumnaKanban nombre="Done" color="var(--success)">
      <UserStoryKanban/>
      <UserStoryKanban/>
    </ColumnaKanban>
  </div>
</template>

<script>
import UserStoryKanban from "@/components/UserStoryKanban";
import ColumnaKanban from "@/components/ColumnaKanban";
import sprintService from "@/services/sprintService";

export default {
  components: {
    ColumnaKanban,
    UserStoryKanban
  },
  data() {
    return {
      sprintBacklogs: []
    }
  },
  mounted() {
    this.load()
  },
  methods: {
    load() {
      sprintService.sprintBacklogs(sb => {
        this.sprintBacklogs = sb;
      })
    },
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