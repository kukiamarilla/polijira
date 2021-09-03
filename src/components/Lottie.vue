<template>
  <lottie-vue-player
    :src="src"
    :theme="options.theme"
    :player-size="options.playerSize"
    :player-controls="false"
    :style="{ width: width, height: height }"
  />
</template>

<script>
export default {
  props: { src: String, width: String, height: String },
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
