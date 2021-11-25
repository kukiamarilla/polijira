<template>
  <div class="wrapper">
    <div class="container">
      <div class="logo">
        <Logo />
      </div>
      <div class="header-info">
        <h1>Reporte de Sprint Backlog</h1>
        <br>
        <br>
        <br>
        <span class="highlight">Proyecto: </span> {{$store.state.proyecto.me.proyecto.nombre}}
        <br>
        <br>
        <span class="highlight">Sprint: </span> Sprint {{sprint.numero}}
        <br>
        <br>
        <span class="highlight">Estado del Sprint: </span> 
        <span v-if="sprint.estado == 'P'"> Pendiente</span>
        <span v-if="sprint.estado == 'A'"> Activo</span>
        <span v-if="sprint.estado == 'F'"> Finalizado</span>
        <br>
        <br>
        <span class="highlight">Fecha: </span> {{now}}
      </div>
      <div class="chart">
        <DoughnutChart v-bind="doughnutChartProps"/>
        <br>
        <br>
        <div class="d-flex justify-content-space-around">
          <p>Pendientes: {{data[0]}}</p>
          <p>Por Terminar: {{data[1]}}</p>
          <p>Cancelados: {{data[2]}}</p>
          <p>Lanzados: {{data[3]}}</p>
        </div>
      </div>
      <div class="table-container">
        <h4>User Stories</h4>
        <Table>
          <TableHeader>
            <Th width="20%">ID</Th>
            <Th width="20%">Título</Th>
            <Th width="20%">Estado</Th>
            <Th width="20%">Horas Estimadas</Th>
            <Th width="20%">Horas Trabajadas</Th>
          </TableHeader>
          <TableBody>
            <Tr v-for="us in sprintBacklog" :key="us.id">
              <Td width="20%">{{us.user_story.id}}</Td>
              <Td width="20%">{{us.user_story.nombre}}</Td>
              <Td width="20%">
                <span v-if="us.user_story.estado == 'P' && us.estado_kanban != 'N'">
                  <span class="text-warning">Pendiente</span>
                </span>
                <span v-if="us.user_story.estado == 'P' && us.estado_kanban == 'N'">
                  <span class="text-primary">Por Terminar</span>
                </span>
                <span v-if="us.user_story.estado == 'C'">
                  <span class="text-danger">Cancelado</span>
                </span>
                <span v-if="us.user_story.estado == 'R'">
                  <span class="texgt-success">Lanzado</span>
                </span>
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
import { DoughnutChart, useDoughnutChart} from "vue-chart-3";
import { Chart, registerables } from 'chart.js';
import { defineComponent, computed, ref  } from "@vue/composition-api";
import Waves from '@/components/Waves.vue';
import Logo from '@/components/Logo.vue';

Chart.register(...registerables);

export default defineComponent({
    props: ['sprintBacklog', 'sprint'],
    components: {
        Table,
        TableHeader,
        TableBody,
        Td,
        Th,
        Tr,
        Waves,
        DoughnutChart,
        Logo
    },

    setup(props) {
      const date = new Date();
      const now = ref(`${date.getDate().toString().padStart(2, "0")}/${(date.getMonth() + 1).toString().padStart(2, "0")}/${date.getFullYear()} ${date.getHours().toString().padStart(2, "0")}:${date.getMinutes().toString().padStart(2, "0")}`);
      const data = computed(() => [
        props.sprintBacklog.filter(us => us.user_story.estado == 'P' && us.estado_kanban != 'N').length,
        props.sprintBacklog.filter(us => us.user_story.estado == 'P' && us.estado_kanban == 'N').length,
        props.sprintBacklog.filter(us => us.user_story.estado == 'C').length,
        props.sprintBacklog.filter(us => us.user_story.estado == 'R').length
      ]);
      
      const chartData = computed(() => {
        return {
          labels: ["Pendiente", "Por Terminar", "Cancelado", "Lanzado"],
          datasets: [
            {
              label: "Estados",
              backgroundColor: ["#ffb800", "#7b61ff", "#f25656", "#6be78d"],
              data: data.value,
            },
          ],
       }
      });
      const { doughnutChartProps, doughnutChartRef } = useDoughnutChart({
        chartData,
      });
      return {
        chartData,
        doughnutChartProps,
        doughnutChartRef,
        now,
        data
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