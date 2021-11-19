<template>
  <Modal v-model="show" height="550px" v-if="userStory">
    <h2 class="titulo">User Story</h2>

    <div class="datos-de-registro">
      <div class="fila">
        <p>
          <span class="highlight">Estado:</span>
          {{ userStory.user_story.estado == "P" ? "Pendiente" : "" }}
          {{ userStory.user_story.estado == "R" ? "Lanzado" : "" }}
          {{ userStory.user_story.estado == "C" ? "Cancelado" : "" }}
        </p>
      </div>
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
          <span v-if="userStory.sprint.estado !== 'F'">
            <a href="#" class="reasignar" @click.prevent="showReasignar = true">
              (Reasignar)
            </a>
          </span>
        </p>
        <p>
          <span class="highlight">Prioridad:</span>
          {{ userStory.user_story.prioridad }}
        </p>
      </div>
      <div class="fila" v-if="showReasignar">
        <div style="flex: 1">
          <span class="highlight">Asignar a:</span> &nbsp;<Select
            :options="selectOptions"
            v-model="miembroSelected"
            @input="reasignar"
          />
        </div>
      </div>
      <br />
      <br />
      <div>
        <label class="highlight">Descripción:</label>
        <p class="multiline">{{ userStory.user_story.descripcion }}</p>
      </div>
    </div>
    <div class="d-flex justify-content-flex-end">
      <div class="botone">
        <Boton
          tema="danger"
          texto="Cancelar"
          @click="cancelar"
          v-if="
            userStory.user_story.estado == 'P' &&
            hasPermission('cancelar_user_stories')
          "
        />
        &nbsp; &nbsp;
        <Boton
          tema="success"
          texto="Lanzar"
          @click="lanzar"
          v-if="
            userStory.user_story.estado == 'P' &&
            hasPermission('lanzar_user_stories') &&
            userStory.estado_kanban == 'N'
          "
        />
      </div>
    </div>

    <TabNavigation :tabs="tabs" default="reviews">
      <template #actividades>
        <Actividades :sprintBacklog="userStory" />
      </template>
      <template #reviews>
        <Reviews :userStory="userStory" />
      </template>
    </TabNavigation>
  </Modal>
</template>

<script>
import Modal from "@/components/Modal";
import TabNavigation from "@/components/TabNavigation";
import Reviews from "@/components/Reviews";
import Actividades from "@/components/Actividades";
import Select from './Select.vue';
import { mapGetters } from 'vuex';
import sprintService from '@/services/sprintService';
import userStoryService from '@/services/userStoryService';
import Alert from '@/helpers/alert';
import Boton from "@/components/Boton";

export default {
  components: {
    Modal,
    TabNavigation,
    Reviews,
    Actividades,
    Select,
    Boton,
  },
  props: ["value", "userStory"],
  computed: {
    ...mapGetters({
      hasPermission: "proyecto/hasPermission",
    }),
    selectOptions() {
      return this.miembrosSprint.map(miembro => miembro.miembro_proyecto.usuario.nombre);
    }
  },
  data() {
    return {
      miembrosSprint: [],
      showReasignar: false,
      miembroSelected: -1,
      show: false,
      tabs: [
        {
          name: "actividades",
          title: "Actividades",
        },
        {
          name: "reviews",
          title: "Reviews",
        },
      ],
    };
  },
  watch: {
    value() {
      this.show = this.value;
      this.loadMiembros();
    },
    show() {
      if (!this.show) this.$emit("input", false);
    },
  },
  methods: {
    loadMiembros() {
      if (this.userStory && !this.userStory.desarrollador && this.hasPermission("modificar_miembros_sprint")) {
        sprintService.miembros(this.userStory.sprint.id).then(response => {
          this.miembrosSprint = response;
        });
      }
    },
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
    reasignar() {
      let reasignado = this.miembrosSprint[this.miembroSelected];
      let confirmar  = confirm(`¿Está seguro que desea reasignar el User Story a ${reasignado.miembro_proyecto.usuario.nombre}?`);
      if(confirmar) {
        userStoryService.reasignar(this.userStory.id, reasignado.id).then(() => {
          this.userStory.desarrollador = reasignado;
          this.showReasignar = false;
          Alert.success("Se ha reasignado el User Story correctamente");
        });
      }
    },
    lanzar() {
      const confirmar = confirm(
        "¿Está seguro que desea lanzar esta User Story?"
      );
      if (confirmar) {
        userStoryService.lanzar(this.userStory.user_story.id).then(() => {
          Alert.success("User Story lanzado!");
          this.userStory.user_story.estado = "R";
        });
      }
    },
    cancelar() {
      const confirmar = confirm(
        "¿Está seguro que desea cancelar esta User Story?"
      );
      if (confirmar) {
        userStoryService.cancelar(this.userStory.user_story.id).then(() => {
          Alert.success("User Story cancelado.");
          this.userStory.user_story.estado = "C";
        });
      }
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
