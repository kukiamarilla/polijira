<template>
  <div class="card card-add" v-on:click="handleClick">
    <Icon icono="add" color="currentColor" size="38px" />
  </div>
</template>

<script>
import Icon from "@/components/Icon";

export default {
  data() {
    return {};
  },
  components: {
    Icon,
  },
  methods: {
    handleClick() {
      this.$emit("click");
    },
  },
};
</script>

<style scoped>
.card-add {
  align-items: center;
  background-color: transparent;
  border: 3px dashed currentColor;
  border-radius: 10px;
  color: var(--gray-4);
  cursor: pointer;
  display: flex;
  height: 190px;
  justify-content: center;
  width: 381px;
}

.card-add:hover {
  color: var(--primary-light);
}
</style>
