<template>
  <div class="card shadow">
    <h3>{{ proyecto.nombre }}</h3>

    <div class="estado">
      <span class="highlight" :style="{ color: colorEstado }">
        {{ estadoTexto }}
      </span>
    </div>

    <Boton
      texto="Ir al Proyecto"
      tema="primary"
      width="100%"
      @click="$router.push(`/proyectos/${proyecto.id}`)"
    />

    <IconosPlegables
      @clickDelete="$emit('clickDelete')"
      @clickWatch="$emit('clickWatch')"
      :hideDelete="proyecto.estado != 'P'"
    />
  </div>
</template>

<script>
import Boton from "@/components/Boton";
import IconosPlegables from "@/components/IconosPlegables";

export default {
  props: ["proyecto"],
  data() {
    return {};
  },
  components: {
    Boton,
    IconosPlegables,
  },
  computed: {
    estadoTexto() {
      let estados = {
        F: "Finalizado",
        A: "Activo",
        P: "Pendiente",
        C: "Cancelado",
      };
      return estados[this.proyecto.estado];
    },
    colorEstado() {
      switch (this.proyecto.estado) {
        case "F":
          return "var(--success)";
        case "A":
          return "var(--warning)";
        case "C":
          return "var(--danger)";
        case "P":
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
