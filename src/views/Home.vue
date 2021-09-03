<template>
  <div>
    <Navbar />
    <Sidebar />

    <div class="container">
      <div v-if="proyectos.length > 0" class="proyectos">
        <ProyectoCard
          v-for="proyecto in proyectos"
          class="card"
          :nombre="proyecto.nombre"
          :estado="proyecto.estado"
          :key="proyecto.id"
        />

        <CardAdd @click="abrirCrearProyecto" />
      </div>
      <div v-else class="sin-proyectos">
        <h1 class="text-center">
          Aun no hay ningún proyecto creado. Crea uno.
        </h1>

        <CardAdd class="add-card m-auto" @click="abrirCrearProyecto" />
      </div>
    </div>

    <Modal v-model="verCrearProyecto" width="498px">
      <h2>Crear Proyecto</h2>

      <InputText title="Nombre:" v-model="nuevo.nombre" />
      <InputDate title="Fecha de Inicio:" v-model="nuevo.fecha_inicio" />
      <InputDate title="Fecha de Fin:" v-model="nuevo.fecha_fin" />
      <label class="highlight">Scrum Master:</label>
      <InputSelect>
        <Select :options="usuariosSelect" v-model="usuarioSeleccionado" />
      </InputSelect>

      <div class="d-flex justify-content-end">
        <Boton texto="Guardar" tema="primary" @click="crearProyecto" />
      </div>
    </Modal>

    <Waves class="waves" />
  </div>
</template>

<script>
import Navbar from "@/components/Navbar.vue";
import Sidebar from "@/components/Sidebar";
import CardAdd from "@/components/CardAdd.vue";
import Waves from "@/components/Waves";
import ProyectoCard from "@/components/ProyectoCard";
import Modal from "@/components/Modal";
import InputText from "@/components/InputText";
import InputDate from "@/components/InputDate";
import Boton from "@/components/Boton";
import Select from "@/components/Select";
import InputSelect from "@/components/InputSelect";

import proyectoService from "@/services/proyectoService";
import usuarioService from "@/services/usuarioService";

export default {
  components: {
    Navbar,
    Sidebar,
    CardAdd,
    Waves,
    ProyectoCard,
    Modal,
    InputText,
    InputDate,
    Boton,
    Select,
    InputSelect,
  },
  mounted() {
    this.cargarProyectos();
    this.cargarUsuarios();
  },
  data() {
    return {
      proyectos: [
        {
          id: "1",
          nombre: "Proyecto 1",
          fecha_inicio: "2021-09-02",
          fecha_fin: "2021-10-02",
          estado: "Pendiente",
          scrum_master: {},
        },
      ],
      verCrearProyecto: false,
      nuevo: {
        id: "",
        nombre: "",
        fecha_inicio: "",
        fecha_fin: "",
        estado: "",
        scrum_master: {},
      },
      usuarios: [],
      usuarioSeleccionado: 0,
    };
  },
  computed: {
    usuariosSelect() {
      return this.usuarios.map((usuario) => usuario.nombre);
    },
  },
  methods: {
    abrirCrearProyecto() {
      this.verCrearProyecto = true;
    },
    cargarProyectos() {
      proyectoService.list().then(() => {});
    },
    cargarUsuarios() {
      usuarioService.list().then((data) => {
        this.usuarios = data;
      });
    },
    crearProyecto() {
      const validacion =
        this.nuevo.nombre.lenght > 0 &&
        this.nuevo.fecha_inicio &&
        this.nuevo.fecha_fin &&
        this.nuevo.fecha_inicio < this.nuevo.fecha_fin &&
        this.nuevo.scrum_master;

      if (validacion) {
        proyectoService.create(this.nuevo).then(() => {
          this.verCrearProyecto = false;
        });
      }
    },
  },
  watch: {
    usuarioSeleccionado(nuevoValor) {
      this.nuevo.scrum_master = this.usuariosSelect[nuevoValor];
    },
  },
};
</script>

<style lang="scss" scoped>
.container {
  margin-left: 110px;
  margin-right: 32px;
}

.proyectos {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 40px;
  place-items: center;

  & > .card {
    max-width: 100%;
    min-width: 300px;
  }
}

.sin-proyectos {
  align-items: center;
  display: flex;
  flex-direction: column;
}

.sin-proyectos > .add-card {
  margin-top: 120px;
}
</style>
