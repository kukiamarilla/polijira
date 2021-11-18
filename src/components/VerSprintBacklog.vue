<template>
  <Modal v-model="show" height="550px" v-if="userStory">
    <h2 class="titulo">User Story</h2>

    <div class="datos-de-registro">
      <div class="fila">
        <p>
          <span class="highlight">Título:</span>
          {{ userStory.user_story.nombre }}
        </p>
        <p>
          <span class="highlight">Horas Estimadas:</span>
          {{ userStory.horas_estimadas }}
        </p>
      </div>
      <div class="fila">
        <p v-if="userStory.desarrollador">
          <span class="highlight">Miembro Asignado:</span>
          {{ userStory.desarrollador.miembro_proyecto.usuario.nombre }}
        </p>
        <p v-else>
          <span class="highlight">Miembro Asignado:</span>
          Nadie
          ( <a href="#" class="reasignar">Reasignar</a> )
        </p>
        <p>
          <span class="highlight">Prioridad:</span>
          {{ userStory.user_story.prioridad }}
        </p>
      </div>
      <div>
        <label class="highlight">Descripción:</label>
        <p class="multiline">{{ userStory.user_story.descripcion }}</p>
      </div>
    </div>

    <TabNavigation :tabs="tabs" default="reviews">
      <template #reviews>
        <Reviews/>
      </template>
      <template #actividades>
        <Actividades :sprintBacklog="userStory"/>
      </template>
    </TabNavigation>
  </Modal>
</template>

<script>
import Modal from "@/components/Modal";
import TabNavigation from "@/components/TabNavigation";
import Reviews from "@/components/Reviews";
import Actividades from "@/components/Actividades";

export default {
  components: {
    Modal,
    TabNavigation,
    Reviews,
    Actividades
  },
  props: ["value", "userStory"],
  computed: {},
  data() {
    return {
      tabs: [
        { 
          name: "reviews", 
          title: "Reviews" 
        },
        {
          name: "actividades", 
          title: "Actividades"
        }
      ],
    };
  },
  watch: {
    value() {
      this.show = this.value;
    },
    show() {
      if (!this.show) this.$emit("input", null);
    },
  },
  methods: {
    formatearFecha(date) {
      const fecha = new Date(date);

      const dia = fecha.getDate();
      const mes = fecha.getMonth() + 1;
      const año = fecha.getFullYear();

      return `${this.fill(dia)}/${this.fill(mes)}/${año}`;
    },
    fill(numero) {
      if (numero < 10) return `0${numero}`;
      else return numero;
    },
  },
};
</script>

<style lang="scss" scoped>
.titulo {
  margin-bottom: 64px;
}

.fila {
  display: flex;

  p {
    width: 50%;
  }
}

h4 {
  margin: 32px 0;
}

p {
  margin: 0;
  padding: 0 0 32px 0;
}

.multiline {
  padding: 32px;
}

.row {
  cursor: pointer;

  &:hover {
    background-color: var(--gray-5);
  }

  &.seleccionado {
    background-color: var(--primary);
    color: white;
    cursor: default;
  }
}

.pl-8 {
  padding-left: 8px;
}
.reasignar {
  color: var(--primary);
  text-decoration: none;
  &:hover {
    color: var(--primary-dark);
  }
}
</style>
