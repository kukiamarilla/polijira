<template>
  <div id="app">
    <router-view class="view" />
    <Alert :show="alert.show" :message="alert.message" :type="alert.type" />
  </div>
</template>

<script>
import authService from "@/services/authService";
import Alert from "@/components/Alert";
import { mapState } from "vuex";

export default {
  components: {
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
