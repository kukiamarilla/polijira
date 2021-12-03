<template>
  <div class="wrapper">
    <div class="container">
      <div class="logo">
        <Logo />
      </div>
      <div class="header-info">
        <h1>Reporte de Sprint Activo</h1>
        <br>
        <br>
        <br>
        <span class="highlight">Proyecto: </span> {{$store.state.proyecto.me.proyecto.nombre}}
        <br>
        <br>
        <span class="highlight">Sprint: </span> Sprint {{sprint.numero}}
        <br>
        <br>
        <span class="highlight">Fecha: </span> {{now}}
      </div>
      <div class="chart">
        <BurndownChart :sprint="sprint" v-if="sprint.id != 0" :disableAnimation="true"/>
        <br>
        <br>
        <div class="d-flex justify-content-space-around">
          <p>Horas Estimadas Totales: {{sprintBacklog.reduce((acc, us) => acc + us.horas_estimadas, 0)}}</p>
          <p>Horas Trabajadas Totales: {{sprintBacklog.reduce((acc, us) => acc + us.actividades.reduce((acc, actividad) => acc + actividad.horas, 0), 0)}}</p>
        </div>
      </div>
      <div class="table-container">
        <h4>User Stories</h4>
        <Table>
          <TableHeader>
            <Th width="20%">ID</Th>
            <Th width="20%">Título</Th>
            <Th width="20%">Asignado a</Th>
            <Th width="20%">Horas Estimadas</Th>
            <Th width="20%">Horas Trabajadas</Th>
          </TableHeader>
          <TableBody>
            <Tr v-for="us in sprintBacklog" :key="us.id">
              <Td width="20%">{{us.user_story.id}}</Td>
              <Td width="20%">{{us.user_story.nombre}}</Td>
              <Td width="20%">
                {{us.desarrollador.miembro_proyecto.usuario.nombre}}
              </Td>
              <Td width="20%">{{us.horas_estimadas}}</Td>
              <Td width="20%">
                {{us.actividades.reduce((total, actividad) => total + actividad.horas, 0)}}
              </Td>
            </Tr>
          </TableBody>
        </Table>  
      </div>
    </div>
  </div>
</template>

<script>
import {Table, TableHeader, TableBody, Td, Th, Tr } from "@/components/Table";
import { Chart, registerables } from 'chart.js';
import { defineComponent, ref, watch  } from "@vue/composition-api";
import Waves from '@/components/Waves.vue';
import Logo from '@/components/Logo.vue';
import sprintService from "@/services/sprintService";
import BurndownChart from "../BurndownChart.vue";

Chart.register(...registerables);

export default defineComponent({
    props: ['sprint'],
    components: {
        Table,
        TableHeader,
        TableBody,
        Td,
        Th,
        Tr,
        Waves,
        Logo,
        BurndownChart
    },

    setup(props) {
      const date = new Date();
      const now = ref(`${date.getDate().toString().padStart(2, "0")}/${(date.getMonth() + 1).toString().padStart(2, "0")}/${date.getFullYear()} ${date.getHours().toString().padStart(2, "0")}:${date.getMinutes().toString().padStart(2, "0")}`);
      const sprintBacklog = ref([])

      watch(() => props.sprint, (sprint) => {
        if (sprint.id != 0) {
          sprintService.sprintBacklog(sprint.id).then(response => {
            sprintBacklog.value = response;
          })
        }
      })
      return {
        now,
        sprintBacklog
      };
    }
})
</script>

<style scoped lang="scss">
.wrapper {
  display: flex;
  align-items: center;
  background-color: #fff;
  flex-direction: column;
  padding: 60px;
  position: relative;
  min-height: 900px;
}
.container {
  width: 100%;
}
.chart {
  margin-top: 64px;
}
.table-container {
  margin-top: 64px;
  display: flex;
  flex-direction: column;
  gap: 32px;
}
.header-info {
  margin-top: 64px;
  h1 {
    text-align: center;
  }
}
.logo {
  display: flex;
  justify-content: center;
  opacity: 0.7;
}
</style>