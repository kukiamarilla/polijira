<template>
  <div class="menu-derecho">
    <svg viewBox="0 0 592 780" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path
        fill-rule="evenodd"
        clip-rule="evenodd"
        d="M70.8611 0C25.0621 121.263 0 252.705 0 390C0 527.295 25.0622 658.737 70.8611 780H592V0L70.8611 0Z"
        :fill="colorFondo"
      />
    </svg>

    <div class="accion centrado-absoluto">
      <h1 class="frase">{{ frase }}</h1>
      <Boton :texto="botonTexto" tema="secondary" />
    </div>
  </div>
</template>

<script>
import Boton from "@/components/Boton";

export default {
  props: { color: String, frase: String, botonTexto: String },
  computed: {
    colorFondo() {
      return this.color ? this.color : "purple";
    },
  },
  components: {
    Boton,
  },
};
</script>

<style scoped>
.menu-derecho {
  height: 100%;
  overflow: hidden;
  min-height: 550px;
  position: absolute;
  right: 0;
  top: 0;
}

.menu-derecho svg {
  height: 100%;
}

.accion {
  align-items: center;
  display: flex;
  flex-direction: column;
  width: 100%;
}

.frase {
  color: white;
  margin-bottom: 3.375rem;
}
</style>
