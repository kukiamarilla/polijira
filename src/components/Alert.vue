<template>
  <Modal :value="show" width="735px">
    <div class="alert-container">
      <h2>{{ title }}</h2>

      <Icon :icono="icon" :color="iconColor" size="105px" />

      <div class="highlight" v-html="message"></div>

      <Boton texto="Aceptar" tema="primary" v-on:click="hideAlert" />
    </div>
  </Modal>
</template>

<script>
import Modal from "@/components/Modal";
import Icon from "@/components/Icon";
import Boton from "@/components/Boton";

import { mapMutations } from "vuex";

export default {
  props: { show: Boolean, message: String, type: String },
  computed: {
    title() {
      return this.type === "success" ? "Éxito" : "Error";
    },
    icon() {
      return this.type === "success" ? "success" : "warning";
    },
    iconColor() {
      return this.type === "success" ? "var(--success)" : "var(--danger)";
    },
  },
  components: {
    Modal,
    Icon,
    Boton,
  },
  methods: {
    ...mapMutations("alert", ["hideAlert"]),
  },
};
</script>

<style lang="scss" scoped>
.alert-container {
  align-items: center;
  display: flex;
  flex-direction: column;
}

h2 {
  align-self: flex-start;
  margin-bottom: 28px;
}

.highlight {
  margin-bottom: 64px;
  margin-top: 28px;
}
</style>
