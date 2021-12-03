<template>
  <div>
    <Navbar />
    <div class="d-flex">
      <SidebarProyecto current="estimacion" :proyecto="proyecto" />
      <div class="container shadow">
        <div class="header">
          <h2>Estimaciones Pendientes</h2>
          <br /><br /><br />
        </div>
        <Table height="400px" v-if="userStories.length > 0">
          <TableHeader>
            <Th width="10%">ID</Th>
            <Th width="20%">Nombre</Th>
            <Th width="30%">Descripción</Th>
            <Th width="20%">Prioridad</Th>
            <Th width="20%">Acciones</Th>
          </TableHeader>
          <TableBody>
            <Tr v-for="userStory in userStories" :key="userStory.id">
              <Td width="10%">{{ userStory.user_story.id }}</Td>
              <Td width="20%">{{ userStory.user_story.nombre }}</Td>
              <Td width="30%"><span class="cutted-text">{{ userStory.user_story.descripcion }}</span></Td>
              <Td width="20%">{{ userStory.user_story.prioridad }}</Td>
              <Td width="20%">
                <div class="acciones d-flex">

                  <a
                      href="#"
                      @click.prevent="verUserStory(userStory.user_story)"
                    >
                      <Icon
                        icono="watch"
                        size="16px"
                        color="#bdbdbd"
                        hover="var(--primary)"
                      />
                  </a>
                  <a
                      href="#"
                      @click.prevent="estimarUserStory(userStory)"
                    >
                      <Icon
                        icono="clock"
                        size="16px"
                        color="#bdbdbd"
                        hover="var(--primary)"
                      />
                  </a>
                </div>
              </Td>
            </Tr>
          </TableBody>
        </Table>
        <div class="empty" v-else>
          <h2>
            No hay User Stories pendientes de estimación.
          </h2>
        </div>
      </div>
    </div>
    <Modal v-model="verUSPlanning" width="496px">
      <h1>Estimar User Story</h1>
      <br /><br />

      <label class="highlight">Título: </label>
      <p>{{ estimating.user_story.nombre }}</p>

      <InputNumber
        title="Estimación en horas:"
        v-model="estimating.horas_estimadas"
        :min="0"
      />

      <div class="d-flex justify-content-flex-end">
        <Boton texto="Estimar" tema="primary" @click="enviarEstimacion" :disabled="loading"/>
      </div>
    </Modal>
    <UserStory v-model="userStory" :userStory="userStory"/>
  </div>
</template>

<script>
import { mapGetters, mapState } from "vuex";

import proyectoService from "@/services/proyectoService";
import sprintService from "@/services/sprintService";

import SidebarProyecto from "@/components/SidebarProyecto";
import Navbar from "@/components/Navbar";
import {Table, TableHeader, TableBody, Th, Tr, Td} from '@/components/Table';
import Icon from '@/components/Icon';
import UserStory from '@/components/UserStory';
import Modal from '@/components/Modal';
import InputNumber from '@/components/InputNumber';
import Boton from '@/components/Boton';

import Alert from '@/helpers/alert';

export default {
  components: {
    Navbar,
    SidebarProyecto,
    Table,
    TableHeader,
    TableBody,
    Th,
    Tr,
    Td,
    Icon,
    UserStory,
    Modal,
    InputNumber,
    Boton
  },
  created() {},
  mounted() {
    this.load();
  },
  computed: {
    ...mapGetters({
      hasPermission: "auth/hasPermission",
      hasPermissions: "auth/hasPermissions",
      hasAnyPermission: "auth/hasAnyPermission",
      hasProyectoPermission: "proyecto/hasPermission",
      hasProyectoPermissions: "proyecto/hasPermissions",
      hasProyectoAnyPermission: "proyecto/hasAnyPermission",
    }),
    ...mapState({
      me: (state) => state.auth.me,
      meProyecto: (state) => state.proyecto.me,
    }),
  },
  data() {
    return {
      loading: false,
      proyecto: {
        nombre: "",
      },
      userStories: [],
      userStory: {
        nombre: "",
        descripcion: "",
        prioridad: "",
      },
      verUSPlanning: false,
      estimating: {
        user_story:{
          nombre: "",
          descripcion: "",
          prioridad: "",
        },
        horas_estimadas: 0,
      },
    };
  },
  methods: {
    load() {
      let idProyecto = this.$route.params.id;
      proyectoService.retrieve(idProyecto).then((proyecto) => {
        this.proyecto = proyecto;
      });
      proyectoService.estimacionesPendientes(idProyecto).then((userStories) => {
        this.userStories = userStories;
      });
    },
    verUserStory(userStory) {
      this.userStory = userStory;
    },
    estimarUserStory(userStory) {
      this.estimating = {...userStory, estimacion: 0};
      this.verUSPlanning = true;
    },
    enviarEstimacion() {
      this.loading = true;
      sprintService.responderEstimacion(this.estimating.id, this.estimating).then(() => {
        this.loading = false;
        Alert.success("User Story estimado.");
        this.load();
        this.verUSPlanning = false;
      });
    },
  },
};
</script>

<style lang="scss" scoped>
.container {
  background-color: white;
  border-radius: 20px;
  height: var(--absolute-remaining-height);
  min-height: 300px;
  padding: 40px;
  margin: 0 40px 40px 40px;
  right: 88px;
  width: calc(100% - 380px);
}

.d-flex.header {
  margin-bottom: 58px;
  justify-content: space-between;
}
.acciones a {
  margin-left: 16px;
}
span.cutted-text {
  width: 80%;
  display: block;
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
}
.empty {
  height: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
  h2 {
    color: var(--gray-4);
    text-align: center;
  }
}
</style>
