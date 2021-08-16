<template>
  <nav>
    <Logo class="logo" />
    <div class="opciones">
      <Boton tema="primary" texto="Cerrar Sesión" @click="logout()"></Boton>
    </div>
  </nav>
</template>

<script>
import Logo from "@/components/Logo";
import Boton from "@/components/Boton";
import authService from "@/services/authService";

export default {
  components: {
    Logo,
    Boton,
  },
  methods: {
    logout() {
      authService.logout();
      this.$router.push({ name: "Login" });
    },
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
