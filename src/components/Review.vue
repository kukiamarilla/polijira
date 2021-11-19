<template>
  <div class="container">
    <div>
      <span class="highlight">{{ review.autor.nombre }}</span>
    </div>

    <div v-if="editar">
      <TextArea title="Comentario" v-model="comentario" />
    </div>

    <div else>
      <p>{{ review.observacion }}</p>
    </div>

    <div>
      <div class="d-flex justify-content-space-between">
        <div>
          <span class="highlight">Fecha:</span> {{ review.fecha_creacion }}
        </div>

        <div class="acciones d-flex">
          <a
            v-if="hasPermission('modificar_reviews')"
            href="#"
            title="Editar Review"
            @click.prevent="$emit('modificar', review)"
          >
            <Icon icono="edit" size="16px" color="#bdbdbd" hover="#F25656" />
          </a>

          <a
            v-if="hasPermission('eliminar_reviews')"
            href="#"
            title="Borrar Review"
            @click.prevent="eliminar"
          >
            <Icon icono="delete" size="16px" color="#bdbdbd" hover="#F25656" />
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Icon from "@/components/Icon";

import reviewService from "@/services/reviewService";
import { mapGetters } from "vuex";

export default {
  components: { Icon },
  props: ["review"],
  computed: {
    ...mapGetters({
      hasPermission: "proyecto/hasPermission",
    }),
  },
  data() {
    return {
      editar: false,
    };
  },
  methods: {
    eliminar() {
      const confirmacion = confirm("¿Estás seguro de eliminar este review?");

      if (confirmacion) {
        reviewService.delete(this.review.id).then(() => {
          this.$emit("eliminar");
        });
      }
    },
  },
};
</script>

<style land="scss" scoped>
.container {
  border: 1px solid var(--gray-5);
  border-radius: 5px;
  margin-bottom: 8px;
  padding: 24px;
}

.acciones a {
  padding-left: 8px;
}

textarea {
  width: 100%;
}
</style>
