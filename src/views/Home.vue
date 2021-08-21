<template>
  <div>
    <Sidebar />

    <div v-if="proyectos" class="proyectos">
      <ProyectoCard nombre="Proyecto 1" estado="Finalizado" />
    </div>
    <div v-else>
      <h1 class="text-center">Aun no hay ningún proyecto creado. Crea uno.</h1>

      <div class="d-flex justify-content-center">
        <CardAdd class="big-add m-auto" />
      </div>
    </div>

    <Waves class="waves" />
  </div>
</template>

<script>
import Sidebar from "@/components/Sidebar";
import CardAdd from "@/components/CardAdd.vue";
import Waves from "@/components/Waves";
import ProyectoCard from "@/components/ProyectoCard";

export default {
  data() {
    return {
      proyectos: [""],
    };
  },
  components: {
    Sidebar,
    CardAdd,
    Waves,
    ProyectoCard,
  },
  methods: {},
};
</script>

<style scoped>
.proyectos {
  margin: 0 88px 120px 130px;
}

.big-add,
.waves {
  margin-top: 120px;
}
</style>
