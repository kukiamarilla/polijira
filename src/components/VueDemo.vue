<template>
  <div class="hello">
    <Logo />
  </div>
</template>

<script>
import Logo from "@/components/Logo";
export default {
  name: "VueDemo",
  props: {},
  data() {
    return {};
  },
  components: {
    Logo,
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
</style>
