<template>
  <div class="container">
    <h1>{{ titulo }}</h1>

    <lottie-vue-player
      src="https://assets2.lottiefiles.com/packages/lf20_0tue65cn.json"
      :theme="options.theme"
      :player-size="options.playerSize"
      :player-controls="false"
      style="width: 100%; height: auto;"
    />
  </div>
</template>

<script>
export default {
  props: { titulo: String },
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
  height: 486px;
  width: 565px;
}
</style>
