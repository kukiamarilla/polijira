<template>
  <nav>
    <Logo class="logo" />
  </nav>
</template>

<script>
import Logo from "@/components/Logo";

export default {
  components: {
    Logo,
  },
};
</script>

<style scoped>
nav {
  height: 8rem;
  top: 0;
  width: 100%;
  z-index: 1;
}

nav .logo {
  margin: 2rem 0 2rem 4rem;
}
</style>
