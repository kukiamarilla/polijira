<template>
  <div class="container">
    <br /><br />

    <TextArea title="Descripción:" v-model="reviewModificar.observacion" />

    <div class="d-flex justify-content-flex-end">
      <Boton texto="Cancelar" tema="secondary" @click="$emit('cerrar')" />

      &nbsp; &nbsp;

      <Boton texto="Actualizar" tema="primary" @click="actualizar" />
    </div>
  </div>
</template>

<script>
import TextArea from "@/components/TextArea";
import Boton from "@/components/Boton";
import Alert from "@/helpers/alert";
import reviewService from "@/services/reviewService";

export default {
  props: ["review"],
  components: {
    TextArea,
    Boton,
  },
  data() {
    return {
      reviewModificar: this.review,
    };
  },
  watch: {
    review() {
      this.reviewModificar = this.review;
    },
  },
  methods: {
    actualizar() {
      reviewService
        .update(this.reviewModificar.id, this.reviewModificar)
        .then(() => {
          Alert.success("Review actualizada correctamente");
          this.$emit("cerrar");
        });
    },
  },
};
</script>

<style></style>
