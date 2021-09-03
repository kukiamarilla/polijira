<template>
  <div>
    <Navbar />
    <Sidebar />

    <div class="container">
      <div v-if="proyectos.length > 0" class="proyectos">
        <ProyectoCard class="card" nombre="Proyecto 1" estado="Finalizado" />
        <ProyectoCard class="card" nombre="Proyecto 2" estado="Pendiente" />
        <ProyectoCard class="card" nombre="Proyecto 3" estado="Cancelado" />
        <CardAdd />
      </div>
      <div v-else class="sin-proyectos">
        <h1 class="text-center">
          Aun no hay ningún proyecto creado. Crea uno.
        </h1>

        <CardAdd class="add-card m-auto" />
      </div>
    </div>

    <Waves class="waves" />
  </div>
</template>

<script>
import Navbar from "@/components/Navbar.vue";
import Sidebar from "@/components/Sidebar";
import CardAdd from "@/components/CardAdd.vue";
import Waves from "@/components/Waves";
import ProyectoCard from "@/components/ProyectoCard";

export default {
  data() {
    return {
      proyectos: [1],
    };
  },
  components: {
    Navbar,
    Sidebar,
    CardAdd,
    Waves,
    ProyectoCard,
  },
  methods: {},
};
</script>

<style lang="scss" scoped>
.container {
  margin-left: 110px;
  margin-right: 32px;
}

.proyectos {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 40px;
  place-items: center;

  & > .card {
    max-width: 100%;
    min-width: 300px;
  }
}

.sin-proyectos {
  align-items: center;
  display: flex;
  flex-direction: column;
}

.sin-proyectos > .add-card,
.waves {
  margin-top: 120px;
}
</style>
