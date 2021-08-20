<template>
  <div>
    <Sidebar />

    <h1 class="text-center">Aun no hay ningún proyecto creado. Crea uno.</h1>

    <div class="d-flex justify-content-center">
      <CardAdd class="big-add m-auto" />
    </div>

    <Waves class="waves" />
  </div>
</template>

<script>
import Sidebar from "@/components/Sidebar";
import CardAdd from "@/components/CardAdd.vue";
import Waves from "@/components/Waves";

export default {
  data() {
    return {};
  },
  components: {
    Sidebar,
    CardAdd,
    Waves,
  },
  methods: {},
};
</script>

<style scoped>
.big-add,
.waves {
  margin-top: 120px;
}
</style>
