<template>
  <span :class="clase">{{ texto }}</span>
</template>

<script>
export default {
  props: { texto: String, direccion: String },
  computed: {
    clase() {
      return this.direccion ? `tooltip ${this.direccion}` : `tooltip derecha`;
    },
  },
};
</script>

<style lang="scss" scoped>
.tooltip {
  display: none;
}

:hover > .tooltip {
  background-color: black;
  border-radius: 10px;
  color: white;
  cursor: auto;
  display: block;
  font-family: "Roboto";
  font-size: 12px;
  padding: 5px 0;
  position: absolute;
  width: 109px;
}

.tooltip::before {
  background-color: black;
  content: "";
  height: 8px;
  position: absolute;
  width: 8px;
}

.tooltip.arriba {
  bottom: calc(100% + 8px);
  left: 50%;
  transform: translateX(-50%);
  &::before {
    left: 50%;
    top: 100%;
    transform: translate(-50%, -50%) rotate(45deg);
  }
}

.tooltip.abajo {
  left: 50%;
  top: calc(100% + 8px);
  transform: translateX(-50%);
  &::before {
    bottom: 100%;
    left: 50%;
    transform: translate(-50%, 50%) rotate(45deg);
  }
}

.tooltip.izquierda {
  right: calc(100% + 8px);
  top: 50%;
  transform: translateY(-50%);
  &::before {
    left: 100%;
    top: 50%;
    transform: translate(-50%, -50%) rotate(45deg);
  }
}

.tooltip.derecha {
  left: calc(100% + 8px);
  top: 50%;
  transform: translateY(-50%);
  &::before {
    right: 100%;
    top: 50%;
    transform: translate(50%, -50%) rotate(45deg);
  }
}
</style>
