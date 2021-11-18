<template>
  <div>
    <div v-if="verListaReviews">
      <div
        v-if="hasPermission('crear_reviews')"
        class="d-flex justify-content-flex-end"
      >
        <Boton texto="Hacer Review" tema="primary" @click="crearReview" />
      </div>

      <div class="reviews">
        <Review
          v-for="review in reviews"
          :review="review"
          :key="review.id"
          @eliminar="loadReviews"
          @modificar="modificarReview"
        />
      </div>
    </div>

    <CrearReview
      v-if="hasPermission('crear_reviews') && verCrearReview"
      :userStory="userStory"
      v-on:creado="loadReviews"
      v-on:cerrar-crear="verCrearReview = false"
    />

    <ModificarReview
      v-if="hasPermission('modificar_reviews') && verModificarReview"
      @cerrar="
        verModificarReview = false;
        loadReviews();
      "
      :review="reviewModificar"
    />
  </div>
</template>

<script>
import Boton from "@/components/Boton";
import Review from "@/components/Review";
import CrearReview from "@/components/CrearReview";
import ModificarReview from "@/components/ModificarReview";

import userStoryService from "@/services/userStoryService";
import { mapGetters } from "vuex";

export default {
  components: { Boton, Review, CrearReview, ModificarReview },
  props: ["userStory"],
  computed: {
    verListaReviews() {
      return !this.verCrearReview && !this.verModificarReview;
    },
    ...mapGetters({
      hasPermission: "proyecto/hasPermission",
    }),
  },
  data() {
    return {
      reviews: [],
      reviewModificar: null,
      verCrearReview: false,
      verModificarReview: false,
    };
  },
  created() {
    this.loadReviews();
  },
  methods: {
    loadReviews() {
      userStoryService.reviews(this.userStory.id).then((result) => {
        this.reviews = result;
      });
    },
    crearReview() {
      if (this.verCrearReview) this.verCrearReview = false;
      else this.verCrearReview = true;
    },
    modificarReview(review) {
      this.reviewModificar = review;
      this.verCrearReview = false;
      this.verModificarReview = true;
    },
  },
};
</script>

<style land="scss" scoped>
.reviews {
  margin-top: 16px;
}
</style>
