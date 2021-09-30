<template>
  <div>
    <Navbar />
    <Sidebar current="home" />

    <div class="container">
      <div v-if="proyectos.length > 0" class="proyectos">
        <ProyectoCard
          v-for="proyecto in proyectos"
          class="card"
          :proyecto="proyecto"
          :key="proyecto.id"
          @clickWatch="detalleProyecto(proyecto)"
          @clickDelete="deleteProyecto(proyecto)"
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
        <Select :options="usuariosSelect" v-model="nuevo.usuarioSeleccionado" />
      </InputSelect>

      <div class="d-flex justify-content-end">
        <Boton texto="Guardar" tema="primary" @click="crearProyecto" />
      </div>
    </Modal>
    <Modal v-model="verDetalleProyecto" width="498px">
      <h2>Detalle de Proyecto</h2>
      <br /><br />

      <InputText
        title="Nombre:"
        v-model="proyectoSelected.nombre"
        :disabled="
          !hasPermission('modificar_proyectos') ||
          proyectoSelected.estado != 'P'
        "
      />
      <InputDate
        title="Fecha de Inicio:"
        v-model="proyectoSelected.fecha_inicio"
        :disabled="
          !hasPermission('modificar_proyectos') ||
          proyectoSelected.estado != 'P'
        "
      />
      <InputDate
        title="Fecha de Fin:"
        v-model="proyectoSelected.fecha_fin"
        :disabled="
          !hasPermission('modificar_proyectos') ||
          proyectoSelected.estado != 'P'
        "
      />
      <label class="highlight">Scrum Master:</label>
      <InputSelect>
        <Select
          :options="usuariosSelect"
          v-model="proyectoSelected.usuarioSeleccionado"
          :disabled="
            !hasPermission('modificar_proyectos') ||
            proyectoSelected.estado != 'P'
          "
        />
      </InputSelect>

      <div class="d-flex justify-content-end">
        <Boton
          texto="Guardar"
          tema="primary"
          @click="modificarProyecto"
          v-if="
            hasPermission('modificar_proyectos') &&
            proyectoSelected.estado == 'P'
          "
        />
        &nbsp; &nbsp;
        <Boton
          texto="Iniciar Proyecto"
          tema="success"
          @click="activarProyecto"
          v-if="
            proyectoSelected.scrum_master.id == me.id &&
            proyectoSelected.estado == 'P'
          "
        />
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
import { mapGetters, mapState } from "vuex";

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
      verDetalleProyecto: false,
      nuevo: {
        id: "",
        nombre: "",
        fecha_inicio: "",
        fecha_fin: "",
        estado: "",
        scrum_master: {},
        usuarioSeleccionado: -1,
      },
      proyectoSelected: {
        id: "",
        nombre: "",
        fecha_inicio: "",
        fecha_fin: "",
        estado: "",
        scrum_master: {},
        usuarioSeleccionado: -1,
      },
      usuarios: [],
    };
  },
  computed: {
    ...mapGetters({
      hasPermission: "auth/hasPermission",
    }),
    ...mapState({
      me: (state) => state.auth.me,
    }),
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
        this.usuarios = usuarios.filter((u) => u.estado == "A");
      });
    },
    validar(proyecto) {
      if (proyecto.nombre.length == 0) {
        Alert.error("El campo Nombre es obligatorio.");
        return false;
      }
      if (!proyecto.fecha_inicio) {
        Alert.error("El campo Fecha de Inicio es obligatorio.");
        return false;
      }
      if (
        proyecto.fecha_inicio.toISOString().substr(0, 10) <
        new Date().toISOString().substr(0, 10)
      ) {
        Alert.error("La Fecha de Inicio no puede estar en el pasado.");
        return false;
      }
      if (!proyecto.fecha_fin) {
        Alert.error("El campo Fecha de Fin es obligatorio.");
        return false;
      }
      if (new Date(proyecto.fecha_inicio) >= new Date(proyecto.fecha_fin)) {
        Alert.error(
          "La Fecha de Fin debe ser ser posterior a la fecha de Inicio."
        );
        return false;
      }
      if (proyecto.usuarioSeleccionado == -1) {
        Alert.error("El campo Scrum Master es obligatorio.");
        return false;
      }
      return true;
    },
    crearProyecto() {
      let validacion = this.validar(this.nuevo);
      if (validacion) {
        let nuevo = this.nuevo;
        nuevo.scrum_master = this.usuarios[nuevo.usuarioSeleccionado];
        nuevo.fecha_inicio = nuevo.fecha_inicio.toISOString().substr(0, 10);
        nuevo.fecha_fin = nuevo.fecha_fin.toISOString().substr(0, 10);
        nuevo.scrum_master_id = nuevo.scrum_master.id;
        this.nuevo = nuevo;
        proyectoService.create(this.nuevo).then(() => {
          this.verCrearProyecto = false;
          Alert.success("El proyecto ha sido creado con éxito.");
          this.load();
        });
      }
    },
    deleteProyecto(proyecto) {
      let confimation = confirm(
        "¿Estás seguro que desea eliminar este proyecto?. Esta acción es irreversible."
      );
      if (confimation)
        proyectoService.delete(proyecto.id).then(() => {
          Alert.success("Proyecto eliminado exitosamente.");
          this.load();
        });
    },
    detalleProyecto(proyecto) {
      let proyectoCopy = { ...proyecto };
      proyectoCopy.fecha_inicio = new Date(
        proyectoCopy.fecha_inicio + "T00:00:00"
      );
      proyectoCopy.fecha_fin = new Date(proyectoCopy.fecha_fin + "T00:00:00");
      proyectoCopy.usuarioSeleccionado = this.usuarios.findIndex(
        (u) => u.id == proyectoCopy.scrum_master.id
      );
      this.proyectoSelected = proyectoCopy;
      this.verDetalleProyecto = true;
    },
    modificarProyecto() {
      let validacion = this.validar(this.proyectoSelected);

      if (validacion) {
        let proyecto = this.proyectoSelected;
        proyecto.scrum_master = this.usuarios[proyecto.usuarioSeleccionado];
        proyecto.fecha_inicio = proyecto.fecha_inicio
          .toISOString()
          .substr(0, 10);
        proyecto.fecha_fin = proyecto.fecha_fin.toISOString().substr(0, 10);
        proyecto.scrum_master_id = proyecto.scrum_master.id;
        this.proyectoSelected = {
          ...proyecto,
          scrum_master: proyecto.scrum_master.id,
        };
        proyectoService
          .update(this.proyectoSelected.id, this.proyectoSelected)
          .then(() => {
            this.verDetalleProyecto = false;
            Alert.success("El proyecto ha sido modificado con éxito.");
            this.load();
          });
      }
    },
    activarProyecto() {
      proyectoService.activar(this.proyectoSelected.id).then(() => {
        this.verDetalleProyecto = false;
        Alert.success("El proyecto ha sido activado con éxito.");
        this.load();
      });
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
