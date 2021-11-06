<template>
  <div>
    <Navbar />

    <div class="d-flex">
      <SidebarProyecto current="miembros" :proyecto="proyecto" />
      <div class="container shadow">
        <div class="header">
          <h2>Sprint Planning</h2>
          <br />
          <h4>Paso 3: Confirmación</h4>
          <br /><br /><br />
        </div>
        <Table height="400px">
          <TableHeader>
            <Th width="10%">ID</Th>
            <Th width="20%">Nombre</Th>
            <Th width="10%">Prioridad</Th>
            <Th width="20%">Asignado a</Th>
            <Th width="20%">Estado de la Estimación</Th>
            <Th width="20%">Estimación</Th>
          </TableHeader>
          <TableBody>
            <Tr v-for="(userStory, index) in sprintBacklog" :key="index">
              <Td width="10%">{{userStory.user_story.id}}</Td>
              <Td width="20%">{{userStory.user_story.nombre}}</Td>
              <Td width="10%">{{userStory.user_story.prioridad}}</Td>
              <Td width="20%">{{userStory.desarrollador.miembro_proyecto.usuario.nombre}}</Td>
              <Td width="20%">{{userStory.estado_estimacion == "p" ? "Parcialmente estimado" : "Completamente Estimado"}}</Td>
              <Td width="20%">{{userStory.horas_estimadas}}</Td>
            </Tr>
          </TableBody>
        </Table>
        <div class="d-flex justify-content-space-between align-items-center">
          <span>
            <span class="highlight">Capacidad del sprint:</span>
            {{ totalAsignado }} / {{ capacidadTotal }}
          </span>

          <Boton texto="Finalizar"  tema="primary" @click="finalizar" :disabled="!enableFinalizar" />
        </div>
      </div>
    </div>

  </div>
</template>

<script>

import { mapState } from 'vuex'

import proyectoService from '@/services/proyectoService.js'
import sprintService from '@/services/sprintService.js'

import Boton from '@/components/Boton.vue'
import Table from '@/components/Table/Table.vue'
import TableHeader from '@/components/Table/TableHeader.vue'
import TableBody from '@/components/Table/TableBody.vue'
import Th from '@/components/Table/Th.vue'
import Tr from '@/components/Table/Tr.vue'
import Td from '@/components/Table/Td.vue'
import SidebarProyecto from '@/components/SidebarProyecto.vue'
import Navbar from '@/components/Navbar.vue'

import Alert from '@/helpers/alert'


export default {
  components: {
    Boton,
    Table,
    TableHeader,
    TableBody,
    Th,
    Tr,
    Td,
    SidebarProyecto,
    Navbar
  },
  data() {
    return {
      proyecto: {
        id: 0,
        nombre: '',
      },
      sprint: {
        planificador: 0,
        fecha_inicio: undefined,
        fecha_fin: undefined,
      },
      sprintBacklog: [],
      miembros: [],
    }
  },
  computed: {
    totalAsignado() {
      let total = 0
      this.sprintBacklog.forEach(userStory => {
        total += userStory.horas_estimadas
      })
      return total
    },
    capacidadTotal() {
      let total = 0
      this.miembros.forEach(miembro => {
        total += this.capacidadPorMiembro(miembro.miembro_proyecto)
      })
      return total
    },
    enableFinalizar() {
      return this.sprintBacklog.every(userStory => userStory.estado_estimacion == "C")
    },
    ...mapState({
      me: (state) => state.auth.me,
      meProyecto: (state) => state.proyecto.me,
    }),
  },
  mounted() {
    this.load();
  },
  methods: {
    load() {
      let idProyecto = this.$route.params.id;
      let idSprint = this.$route.params.idSprint
      proyectoService.retrieve(idProyecto).then(proyecto => {
        this.proyecto = proyecto;
      });
      sprintService.retrieve(idSprint).then(sprint => {
        this.sprint = sprint;
        if(!sprint.estado_planificacion == "P") this.$router.back();
        if (sprint.planificador != this.meProyecto.id) this.$router.back();
        if(!sprint.estado_planificacion == "P") this.$router.back();
        let paso = localStorage.getItem("sprint-planning-paso");
        if(!paso) {
          this.$router.push(
            `/proyectos/${idProyecto}/sprint-planning/${idSprint}/paso-1`
          );
          return
        }
        if (!["2", "3"].includes(paso)){
          this.$router.push(
            `/proyectos/${idProyecto}/sprint-planning/${idSprint}/paso-${paso}`
          );
          return
        }
        localStorage.setItem("sprint-planning-paso", 3);
      });
      sprintService.sprintBacklog(idSprint).then(sprintBacklog => {
        this.sprintBacklog = sprintBacklog;
      });
      sprintService.miembros(idSprint).then(miembros => {
        this.miembros = miembros;
      });
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
    finalizar() {
      let idSprint = this.$route.params.idSprint
      sprintService.finalizarSprintPlanning(idSprint).then(() => {
        Alert.success("Sprint Planning finalizado.");
        this.$router.push({ name: 'Sprints', params: { id: this.proyecto.id } });
      });
    },
  }  
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
