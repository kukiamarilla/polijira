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
      <br /><br />
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
import Alert from "@/helpers/alert";
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
    this.load();
  },
  data() {
    return {
      proyectos: [],
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
      usuarioSeleccionado: -1,
    };
  },
  computed: {
    usuariosSelect() {
      return this.usuarios.map((usuario) => usuario.nombre);
    },
  },
  methods: {
    load() {
      this.cargarProyectos();
      this.cargarUsuarios();
    },
    abrirCrearProyecto() {
      this.verCrearProyecto = true;
    },
    cargarProyectos() {
      proyectoService.list().then((proyectos) => {
        this.proyectos = proyectos;
      });
    },
    cargarUsuarios() {
      usuarioService.list().then((usuarios) => {
        this.usuarios = usuarios;
      });
    },
    crearProyecto() {
      const validacion =
        this.nuevo.nombre.length > 0 &&
        this.nuevo.fecha_inicio &&
        this.nuevo.fecha_fin &&
        new Date(this.nuevo.fecha_inicio) < new Date(this.nuevo.fecha_fin) &&
        this.nuevo.scrum_master;

      if (this.nuevo.nombre.length == 0) {
        Alert.error("El campo Nombre es obligatorio.");
        return;
      }
      if (!this.nuevo.fecha_inicio) {
        Alert.error("El campo Fecha de Inicio es obligatorio.");
        return;
      }
      if (
        this.nuevo.fecha_inicio.toISOString().substr(0, 10) <
        new Date().toISOString().substr(0, 10)
      ) {
        Alert.error("La Fecha de Inicio no puede estar en el pasado.");
        return;
      }
      if (!this.nuevo.fecha_fin) {
        Alert.error("El campo Fecha de Fin es obligatorio.");
        return;
      }
      if (new Date(this.nuevo.fecha_inicio) >= new Date(this.nuevo.fecha_fin)) {
        Alert.error(
          "La Fecha de Fin debe ser ser posterior a la fecha de Inicio."
        );
        return;
      }
      if (this.usuarioSeleccionado == -1) {
        Alert.error("El campo Scrum Master   es obligatorio.");
        return;
      }

      if (validacion) {
        let nuevo = this.nuevo;
        nuevo.fecha_inicio = nuevo.fecha_inicio.toISOString().substr(0, 10);
        nuevo.fecha_fin = nuevo.fecha_fin.toISOString().substr(0, 10);
        nuevo.scrum_master_id = nuevo.scrum_master.id;
        this.nuevo = nuevo;
        proyectoService.create(this.nuevo).then(() => {
          this.verCrearProyecto = false;
          Alert.success("El proyecto ha sido creado con éxito.");
          this.load();
        });
      } else {
        Alert.error("Error de validación.");
      }
    },
  },
  watch: {
    usuarioSeleccionado(nuevoValor) {
      this.nuevo.scrum_master = this.usuarios[nuevoValor];
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
