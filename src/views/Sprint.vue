<template>
  <div>
    <Navbar />
    <div class="d-flex">
      <SidebarProyecto current="sprints" :proyecto="proyecto" />
      <div class="container shadow">
        <div class="d-flex justify-content-space-between">
          <h2>Sprint {{ sprint.numero }}</h2>

          <Boton
            v-if="sprint.estado === 'A'"
            texto="Finalizar Sprint"
            tema="success"
            @click="finalizarSprint"
          />
        </div>
        <br />
        <br />
        <TabNavigation :tabs="tabs" default="kanban">
          <template #kanban>
            <Kanban />
          </template>
          <template #miembros>
            <MiembrosSprint :sprint="sprint" />
          </template>
          <template #sprint-backlog>
            <SprintBacklog :sprint="sprint" />
          </template>
          <template #burndown-chart>
            <BurndownChart :sprint="sprint" />
          </template>
        </TabNavigation>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from "@/components/Navbar";
import SidebarProyecto from "@/components/SidebarProyecto";
import TabNavigation from "@/components/TabNavigation";
import Kanban from "@/components/Kanban";
import MiembrosSprint from "@/components/MiembrosSprint";
import SprintBacklog from "@/components/SprintBacklog";
import BurndownChart from "@/components/BurndownChart";
import Boton from "@/components/Boton";
import proyectoService from "@/services/proyectoService";
import sprintService from "@/services/sprintService";
import { mapGetters, mapState } from "vuex";

export default {
  components: {
    Navbar,
    SidebarProyecto,
    TabNavigation,
    Kanban,
    MiembrosSprint,
    SprintBacklog,
    BurndownChart,
    Boton,
  },
  created() {},
  mounted() {
    this.load();
  },
  computed: {
    ...mapGetters({
      hasPermission: "auth/hasPermission",
      hasPermissions: "auth/hasPermissions",
      hasAnyPermission: "auth/hasAnyPermission",
      hasProyectoPermission: "proyecto/hasPermission",
      hasProyectoPermissions: "proyecto/hasPermissions",
      hasProyectoAnyPermission: "proyecto/hasAnyPermission",
    }),
    ...mapState({
      me: (state) => state.auth.me,
    }),
  },
  data() {
    return {
      sprint: {
        id: 0,
        numero: 0,
        fecha_inicio: 0,
        fecha_fin: 0,
        estado: ""
      },
      proyecto: {
        id: 0,
        nombre: ""
      },
      tabs: [
        {
          name: "kanban",
          title: "Kanban"
        },
        {
          name: "miembros",
          title: "Miembros"
        },
        {
          name: "sprint-backlog",
          title: "Sprint Backlog"
        },
        {
          name: "burndown-chart",
          title: "Burndown Chart"
        }
      ]
    }
  },
  methods: {
    load() {
      sprintService.retrieve(this.$route.params["idSprint"]).then(sprint => {
        this.sprint = sprint
      })
      proyectoService.retrieve(this.$route.params["id"]).then(proyecto => {
        this.proyecto = proyecto
      })
    },
    finalizarSprint() {
      sprintService.finalizar(this.sprint.id).then(() => {
        this.load();
      });
    }
  },
};
</script>

<style lang="scss" scoped>
.container {
  background-color: white;
  border-radius: 20px;
  height: var(--absolute-remaining-height);
  min-height: 300px;
  padding: 40px;
  margin: 0 40px 40px 40px;
  right: 88px;
  width: calc(100% - 380px);
}
</style>
