<template>
  <div id="app">
    <Navbar />

    <router-view class="view" />
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

<style lang="scss" scoped>
#app {
  --app-min-height: 780px;
  min-height: var(--app-min-height);
}
</style>
