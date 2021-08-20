<template>
  <div>
    <div class="container">
      <div class="content">
        <h1>
          Has iniciado sesión. <br />Sin embargo nadie ha activado tu cuenta.
        </h1>

        <Lottie
          height="400px"
          src="https://assets3.lottiefiles.com/private_files/lf30_j7ezldoy.json"
          width="100%"
        />
      </div>
    </div>

    <Waves />
  </div>
</template>

<script>
import Waves from "@/components/Waves.vue";
import Lottie from "@/components/Lottie.vue";

export default {
  components: {
    Waves,
    Lottie,
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
