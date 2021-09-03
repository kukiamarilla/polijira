<template>
  <div class="container">
    <Navbar :mostrarLogout="true" />

    <h1 class="text-center">
      No tienes permisos suficientes para acceder aquí.
    </h1>

    <div class="d-flex align-items-center justify-content-center">
      <Lottie
        height="300px"
        src="https://assets3.lottiefiles.com/private_files/lf30_j7ezldoy.json"
        width="300px"
      />

      <div>
        <span class="highlight">Te faltan los siguientes permisos:</span>
        <ul class="danger">
          <li>Permiso 1</li>
          <li>Permiso 2</li>
          <li>Permiso 3</li>
        </ul>
      </div>
    </div>

    <Waves />
  </div>
</template>

<script>
import Navbar from "@/components/Navbar.vue";
import Waves from "@/components/Waves.vue";
import Lottie from "@/components/Lottie.vue";

export default {
  components: {
    Waves,
    Lottie,
    Navbar,
  },
};
</script>

<style lang="scss" scoped>
.highlight,
ul.danger li {
  color: red;
}

ul {
  padding-left: 16px;
}
</style>
