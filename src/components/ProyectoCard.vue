<template>
  <div class="card shadow">
    <h3>{{ nombre }}</h3>

    <div class="estado">
      <span class="highlight" :style="{ color: colorEstado }">
        {{ estado }}
      </span>
    </div>

    <Boton texto="Ir al Proyecto" tema="primary" width="100%" />

    <IconosPlegables />
  </div>
</template>

<script>
import Boton from "@/components/Boton";
import IconosPlegables from "@/components/IconosPlegables";

export default {
  props: { nombre: String, estado: String },
  data() {
    return {};
  },
  components: {
    Boton,
    IconosPlegables,
  },
  computed: {
    colorEstado() {
      switch (this.estado) {
        case "Finalizado":
          return "var(--success)";
        case "En Curso":
          return "var(--warning)";
        case "Cancelado":
          return "var(--danger)";
        case "Pendiente":
          return "var(--info)";
        default:
          return "currentColor";
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.card {
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  height: 190px;
  justify-content: space-between;
  padding: 24px;
  position: relative;
  width: 381px;
}

h3 {
  line-height: 1;
}

.highlight::before {
  background-color: currentColor;
  border-radius: 6px;
  content: "";
  display: inline-block;
  height: 8px;
  margin-right: 12px;
  width: 8px;
}

.plegable {
  position: absolute;
  right: 12px;
  top: 12px;
}
</style>
