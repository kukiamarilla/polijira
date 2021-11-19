<template>
  <div id="app">
    <LineChart v-bind="lineChartProps" />
  </div>
</template>

<script>
import sprintService from '@/services/sprintService.js'
import { Chart, registerables } from 'chart.js';
import { LineChart, useLineChart } from 'vue-chart-3';
import { ref, computed, defineComponent } from '@vue/composition-api';

Chart.register(...registerables);

export default defineComponent({
  props: ['sprint'],
  components: {
    LineChart,
  },
  setup({sprint}) {
    const horasTotales = ref(0);
    const idealData = ref([]);

    
    const options = ref({
      scales: {
        y: {
          title: 'Y Axis',
        }
      }
    })
    const data = ref([
      {
        dia: "2021-11-12",
        horas_restantes: 117,
      },
      {
        dia: "2021-11-13",
        horas_restantes: 110,
      },
      {
        dia: "2021-11-14",
        horas_restantes: 90,
      },
      {
        dia: "2021-11-15",
        horas_restantes: 84,
      },
      {
        dia: "2021-11-16",
        horas_restantes: 83,
      },
      {
        dia: "2021-11-17",
        horas_restantes: 70,
      },
      {
        dia: "2021-11-18",
        horas_restantes: 65,
      },
    ]);

    const calculateIdealData = () => {
      const ini = new Date(sprint.fecha_inicio).getTime();
      const fin = new Date(sprint.fecha_fin).getTime();
      const difDias = (fin - ini) / (1000 * 60 * 60 * 24);
      const pendiente = horasTotales.value / difDias;

      for(let i = 0; i <= difDias; i++) {
        const dia = new Date(ini + (i * 1000 * 60 * 60 * 24));
        idealData.value = [...idealData.value, {
          dia: dia.toISOString().split('T')[0],
          horas_restantes: horasTotales.value - (pendiente * i)
        }];
      }
    }

    sprintService.sprintBacklog(sprint.id).then(backlog => {
      backlog.forEach(item => {
        horasTotales.value += item.horas_estimadas;
      });
      calculateIdealData();
    });
    
    const chartData = computed(() => ({
      datasets: [
        {
          data: data.value,
          backgroundColor: '#431eff',
          borderColor: '#431eff',
          label: 'Real',
          parsing: {
            xAxisKey: 'dia',
            yAxisKey: 'horas_restantes',
          }
        },{
          data: idealData.value,
          backgroundColor: '#6be78d',
          borderColor: '#6be78d',
          label: 'Ideal',
          parsing: {
            xAxisKey: 'dia',
            yAxisKey: 'horas_restantes',
          }
        },
      ],
    }));

    const { lineChartProps, lineChartRef } = useLineChart({
      chartData,
    });

    return { chartData, lineChartProps, lineChartRef, options };
  },
});
</script>

<style scoped lang="scss">
#app {
  font-family: 'Roboto';
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
