<template>
  <div id="app">
    <Navbar />

    <Alert :show="alert.show" :message="alert.message" :type="alert.type" />

    <router-view class="view" />
  </div>
</template>

<script>
import Navbar from "@/components/Navbar";
import authService from "@/services/authService";
import Alert from "@/components/Alert";

import { mapState } from "vuex";

export default {
  components: {
    Navbar,
    Alert,
  },
  mounted() {
    if (authService.isLoggedIn()) this.$store.commit("auth/login");
  },
  computed: {
    ...mapState({
      alert: (state) => state.alert.alert,
    }),
  },
};
</script>

<style lang="scss" scoped>
#app {
  --app-min-height: 780px;
  min-height: var(--app-min-height);
}
</style>
