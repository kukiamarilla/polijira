<template>
  <div>
    <Sidebar />
    <div class="container shadow">
      <h2>Usuarios</h2>

      <Table />
    </div>

    <Waves />
  </div>
</template>

<script>
import Sidebar from "@/components/Sidebar";
import Waves from "@/components/Waves";
import Table from "@/components/Table";

export default {
  components: {
    Sidebar,
    Waves,
    Table,
  },
};
</script>

<style lang="scss" scoped>
.container {
  background-color: white;
  border-radius: 20px;
  left: 110px;
  height: var(--absolute-remaining-height);
  min-height: 300px;
  padding: 40px;
  position: absolute;
  right: 88px;
}

h2 {
  margin-bottom: 58px;
}
</style>
