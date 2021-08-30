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
  --app-height: 100vh;
  --app-min-height: 780px;

  height: var(--app-height);
  min-height: var(--app-min-height);

  & > .view {
    height: calc(var(--app-height) - var(--header-height));
    min-height: calc(var(--app-min-height) - var(--header-height));
  }
}
</style>
