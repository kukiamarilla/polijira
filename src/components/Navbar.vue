<template>
  <nav>
    <Logo class="logo" />
    <div class="opciones">
      <Boton tema="primary" texto="Cerrar Sesión"></Boton>
    </div>
  </nav>
</template>

<script>
import Logo from "@/components/Logo";
import Boton from "@/components/Boton";

export default {
  components: {
    Logo,
    Boton,
  },
};
</script>

<style scoped lang="scss">
nav {
  height: 8rem;
  top: 0;
  width: 100%;
  z-index: 1;
  display: flex;
  justify-content: space-between;
  padding: 2rem 4rem 2rem 4rem;
  .opciones {
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
}
</style>
