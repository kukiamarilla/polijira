<template>
  <nav>
    <Logo class="logo" />
    <div class="opciones">
      <Boton
        tema="primary"
        texto="Cerrar Sesión"
        @click="logout()"
        v-if="mostrarLogout"
      ></Boton>
    </div>
  </nav>
</template>

<script>
import { mapState } from "vuex";

import Logo from "@/components/Logo";
import Boton from "@/components/Boton";
import authService from "@/services/authService";

export default {
  components: {
    Logo,
    Boton,
  },
  data() {
    return {
      rutasConLogoutEnNavbar: ["No Activado", "No Autorizado"],
    };
  },
  computed: {
    mostrarLogout() {
      const rutaActual = this.$router.currentRoute.name;
      return this.rutasConLogoutEnNavbar.includes(rutaActual);
    },
    ...mapState({
      isLoggedIn: (state) => state.auth.isLoggedIn,
    }),
  },
  methods: {
    logout() {
      authService.logout();
      this.$store.commit("auth/logout");
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
