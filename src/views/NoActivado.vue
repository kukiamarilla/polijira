<template>
  <div>
    <div class="container">
      <div class="content">
        <h1 class="large">
          Has iniciado sesión. <br />Sin embargo nadie ha activado tu cuenta.
        </h1>
        <lottie-vue-player
          src="https://assets3.lottiefiles.com/private_files/lf30_j7ezldoy.json"
          :theme="options.theme"
          :player-size="options.playerSize"
          :player-controls="false"
          style="width: 100%; height: 400px"
        />
      </div>
    </div>
    <Waves />
  </div>
</template>

<script>
import Waves from "@/components/Waves.vue";

export default {
  components: {
    Waves,
  },
  data() {
    return {
      options: {
        minimizable: false,
        playerSize: "standard",
        backgroundColor: "#fff",
        backgroundStyle: "color",
        theme: {
          controlsView: "standard",
          active: "light",
          light: {
            color: "#3D4852",
            backgroundColor: "#fff",
            opacity: "0.7",
          },
          dark: {
            color: "#fff",
            backgroundColor: "#202020",
            opacity: "0.7",
          },
        },
      },
    };
  },
};
</script>

<style lang="scss" scoped>
.container {
  display: flex;
  justify-content: center;
  .content {
    width: 70vw;
  }
}
h1 {
  text-align: center;
}
</style>