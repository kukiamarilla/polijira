<template>
  <div id="app">
    <Navbar />

    <router-view />
  </div>
</template>

<script>
import Navbar from "@/components/Navbar";
import authService from "@/services/authService";

export default {
  components: {
    Navbar,
  },
  mounted() {
    if (authService.isLoggedIn()) this.$store.commit("auth/login");
  },
};
</script>

<style>
#app {
  min-height: 100vh;
}
</style>
