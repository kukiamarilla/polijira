<template>
  <div id="app">
    <Navbar />

    <router-view />
  </div>
</template>

<script>
import Navbar from "@/components/Navbar";

export default {
  components: {
    Navbar,
  },
};
</script>

<style>
html {
  font-size: 16px;
}

body {
  margin: 0;
}

#app {
  margin-top: 8rem;
}
</style>
