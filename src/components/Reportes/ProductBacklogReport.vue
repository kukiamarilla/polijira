<template>
  <div class="wrapper">
    <div class="container">
      <div class="logo">
        <Logo />
      </div>
      <div class="header-info">
        <h1>Reporte de Product Backlog</h1>
        <br />
        <br />
        <br />
        <span class="highlight">Proyecto: </span>
        {{ proyecto.nombre }}
        <br />
        <br />
        <span class="highlight">Estado del Proyecto: </span>
        <span v-if="proyecto.estado == 'A'">Activo</span>
        <span v-if="proyecto.estado == 'F'">Finalizado</span>
        <span v-if="proyecto.estado == 'P'">Pendiente</span>
        <span v-if="proyecto.estado == 'C'">Cancelado</span>
        <br />
        <br />
        <span class="highlight">Fecha: </span> {{ now }}
      </div>
      <div class="chart">
        <DoughnutChart v-bind="doughnutChartProps" />
        <br />
        <br />
        <div class="d-flex justify-content-space-around">
          <p>Pendientes: {{ data[0] }}</p>
          <p>Cancelados: {{ data[1] }}</p>
          <p>Lanzados: {{ data[2] }}</p>
        </div>
      </div>
      <div class="table-container">
        <h4>User Stories</h4>
        <Table>
          <TableHeader>
            <Th width="20%">ID</Th>
            <Th width="20%">Título</Th>
            <Th width="20%">Estado</Th>
          </TableHeader>
          <TableBody>
            <Tr v-for="us in productBacklog" :key="us.id">
              <Td width="20%">{{ us.id }}</Td>
              <Td width="20%">{{ us.nombre }}</Td>
              <Td width="20%">
                <span v-if="us.estado == 'P'">
                  <span class="text-warning">Pendiente</span>
                </span>
                <span v-if="us.estado == 'C'">
                  <span class="text-danger">Cancelado</span>
                </span>
                <span v-if="us.estado == 'R'">
                  <span class="texgt-success">Lanzado</span>
                </span>
              </Td>
            </Tr>
          </TableBody>
        </Table>
      </div>
    </div>
  </div>
</template>

<script>
import { Table, TableHeader, TableBody, Td, Th, Tr } from "@/components/Table";
import { DoughnutChart, useDoughnutChart } from "vue-chart-3";
import { Chart, registerables } from "chart.js";
import { defineComponent, computed, ref } from "@vue/composition-api";
import Waves from "@/components/Waves.vue";
import Logo from "@/components/Logo.vue";

Chart.register(...registerables);

export default defineComponent({
  props: ["productBacklog", "proyecto"],
  components: {
    Table,
    TableHeader,
    TableBody,
    Td,
    Th,
    Tr,
    Waves,
    DoughnutChart,
    Logo,
  },

  setup(props) {
    const date = new Date();
    const now = ref(
      `${date.getDate().toString().padStart(2, "0")}/${(date.getMonth() + 1)
        .toString()
        .padStart(2, "0")}/${date.getFullYear()} ${date
        .getHours()
        .toString()
        .padStart(2, "0")}:${date.getMinutes().toString().padStart(2, "0")}`
    );
    const data = computed(() => [
      props.productBacklog.filter((us) => us.estado == "P").length,
      props.productBacklog.filter((us) => us.estado == "C").length,
      props.productBacklog.filter((us) => us.estado == "R").length,
    ]);

    const chartData = computed(() => {
      return {
        labels: ["Pendiente", "Cancelado", "Lanzado"],
        datasets: [
          {
            label: "Estados",
            backgroundColor: ["#ffb800", "#7b61ff", "#f25656", "#6be78d"],
            data: data.value,
          },
        ],
      };
    });
    const { doughnutChartProps, doughnutChartRef } = useDoughnutChart({
      chartData,
    });
    return {
      chartData,
      doughnutChartProps,
      doughnutChartRef,
      now,
      data,
    };
  },
});
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
