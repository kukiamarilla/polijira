<template>
  <div class="container">
    <div>
      <h2>Hacer Review</h2>
    </div>

    <div>
      <TextArea title="Comentario" v-model="comentario" />
    </div>

    <div class="d-flex justify-content-flex-end">
      <Boton texto="Cancelar" tema="secondary" @click="$emit('cerrar-crear')" />

      <Boton texto="Guardar" tema="primary" @click="crearReview" />
    </div>
  </div>
</template>

<script>
import TextArea from "@/components/TextArea";
import Boton from "@/components/Boton";

import reviewService from "@/services/reviewService";
import Alert from "@/helpers/alert";

export default {
  components: { TextArea, Boton },
  props: ["userStory"],
  data() {
    return {
      comentario: "",
    };
  },
  methods: {
    crearReview() {
      const payload = {
        user_story: this.userStory.id,
        observacion: this.comentario,
      };

      reviewService.create(payload).then(() => {
        Alert.success("Review creado exitosamente");
        this.$emit("creado");
      });
    },
  },
};
</script>

<style land="scss" scoped>
.container {
  padding: 24px 0;
}

h2 {
  margin-bottom: 68px;
}
</style>
