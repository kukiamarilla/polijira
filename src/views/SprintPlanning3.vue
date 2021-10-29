<template>
  <div>
    <Navbar />

    <div class="d-flex">
      <SidebarProyecto current="miembros" :proyecto="proyecto" />
      <div class="container shadow">
        <div class="header">
          <h2>Spring Planning</h2>
          <br />
          <h4>Paso 3: Finalización</h4>
          <br /><br /><br />
        </div>
        <Table height="400px">
          <TableHeader>
            <Th width="5%">ID</Th>
            <Th width="25%">Nombre</Th>
            <Th width="25%">Desarrollador</Th>
            <Th width="25%">Prioridad</Th>
            <Th width="15%">Estado de la estimación</Th>
            <Th width="15%">Estimación</Th>
          </TableHeader>
          <TableBody>
            <Tr v-for="us in sprintBacklog" :key="us.user_story.id">
              <Td width="5%">{{ us.user_story.id }}</Td>
              <Td width="25%">{{ us.user_story.nombre }}</Td>
              <Td width="25%">{{
                us.user_story.desarrollador.miembro_proyecto.usuario.nombre
              }}</Td>
              <Td width="25%">{{ us.user_story.prioridad }}</Td>
              <Td width="15%">{{ us.user_story.estado_estimacion }}</Td>
              <Td width="15%">{{ us.sprint.estimacion }}</Td>
            </Tr>
          </TableBody>
        </Table>
        <div class="d-flex justify-content-space-between align-items-center">
          <span>
            <span class="highlight">Capacidad del sprint:</span>
            {{ totalAsignado }} / {{ capacidadTotal }}
          </span>

          <Boton texto="Finalizar" @click="finalizar" tema="primary" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from "@/components/Navbar";
import SidebarProyecto from "@/components/SidebarProyecto";
import { Table, TableHeader, TableBody, Th, Tr, Td } from "@/components/Table";
import sprintService from "@/services/sprintService";
import proyectoService from "@/services/proyectoService";
import miembroService from "@/services/miembroService";
import { mapGetters, mapState } from "vuex";
import Boton from "@/components/Boton";

export default {
  components: {
    Navbar,
    SidebarProyecto,
    Table,
    TableHeader,
    TableBody,
    Th,
    Tr,
    Td,
    Boton,
  },
  created() {},
  mounted() {
    this.load();
    localStorage.setItem("spring-planning-paso", 3);
  },
  computed: {
    capacidadesDeMiembros() {
      const capacidades = {};

      this.miembrosSprint.forEach((miembro) => {
        capacidades[miembro.id] = this.capacidadPorMiembro(miembro);
      });

      return capacidades;
    },
    horasAsignadasDeMiembros() {
      const usPlanning = this.productBacklog.filter((us) => us.included);
      const todosLosUS = [...usPlanning, ...this.sprintBacklog];

      const horasAsignadas = {};

      this.miembrosSprint.forEach((miembro) => {
        let asignado = 0;

        todosLosUS.forEach((us) => {
          if (us.desarrollador === miembro) {
            asignado += us.estimacion;
          }
        });

        horasAsignadas[miembro.id] = asignado;
      });

      return horasAsignadas;
    },
    totalAsignado() {
      let sumaAsignadas = 0;

      for (let miembro in this.horasAsignadasDeMiembros) {
        sumaAsignadas += this.horasAsignadasDeMiembros[miembro];
      }

      return sumaAsignadas;
    },
    capacidadTotal() {
      let capacidad = 0;
      this.miembrosSprint.forEach((miembro) => {
        capacidad += this.capacidadesDeMiembros[miembro.id];
      });
      return capacidad;
    },
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
      meProyecto: (state) => state.proyecto.me,
    }),
  },
  data() {
    return {
      proyecto: {
        nombre: "",
      },
      sprint: {
        planificador: 0,
        fecha_inicio: undefined,
        fecha_fin: undefined,
      },
      miembrosSprint: [],
      sprintBacklog: [],
    };
  },
  methods: {
    async load() {
      const paso = localStorage.getItem("sprint-planning");
      const idProyecto = this.$route.params["id"];
      const idSprint = this.$route.params["idSprint"];

      // cargamos el proyecto
      proyectoService.retrieve(idProyecto).then((proyecto) => {
        this.proyecto = proyecto;
      });

      // cargamos los miembros del proyecto temporalmente,
      // para usar los datos del usuario
      const miembrosProyecto = await miembroService
        .list(idProyecto)
        .then((miembros) => miembros);

      // cargamos el sprint
      sprintService.retrieve(idSprint).then((sprint) => {
        this.sprint = sprint;
        if (!sprint.planificador) this.$router.back();
        if (sprint.planificador != this.meProyecto.id) this.$router.back();
        if (![null, 2].includes(paso))
          this.$router.push(
            `/proyectos/${idProyecto}/sprint-planning/${idSprint}/paso-${paso}`
          );
      });

      // cargamos miembros del sprint
      sprintService.miembros(idSprint).then((miembrosSprint) => {
        this.miembrosSprint = miembrosSprint.map((ms) => {
          const mp = miembrosProyecto.find((m) => m.id === ms.miembro_proyecto);
          return { ...ms, nombre: mp.usuario.nombre, horario: mp.horario };
        });
      });

      // cargamos el sprint backlog
      sprintService.sprintBacklog(idSprint).then((sprintBacklog) => {
        this.sprintBacklog = sprintBacklog.map((us) => ({
          ...us,
          included: true,
        }));
      });
    },
    capacidadPorMiembro(miembro) {
      const ini = new Date(this.sprint.fecha_inicio).getTime();
      const fin = new Date(this.sprint.fecha_fin).getTime();
      let capacidad = 0;
      let horario = this.horarioToArray(miembro.horario);
      for (let curr = ini; curr <= fin; curr += 1000 * 60 * 60 * 24) {
        capacidad += horario[new Date(curr).getDay()];
      }
      return capacidad;
    },
    horarioToArray(horario) {
      return [
        horario.domingo,
        horario.lunes,
        horario.martes,
        horario.miercoles,
        horario.jueves,
        horario.viernes,
        horario.sabado,
      ];
    },
    finalizar() {},
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

.d-flex.header {
  margin-bottom: 58px;
  justify-content: space-between;
}
.acciones a {
  margin-left: 16px;
}
</style>
