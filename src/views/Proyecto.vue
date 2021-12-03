<template>
  <div>
    <Navbar />
    <div class="body">
      <SidebarProyecto :proyecto="proyecto" current="home" />
      <div class="d-flex content">
        <div class="cabecera">
          <h1>Bienvenido a {{ proyecto.nombre }}</h1>

          <div
            class="iniciar"
            v-if="hasPermission('activar_proyecto') && proyecto.estado == 'P'"
          >
            <Boton
              texto="Iniciar Proyecto"
              tema="success"
              v-if="proyecto.estado == 'P'"
              @click="activarProyecto(proyecto)"
            />
          </div>

          <div
            class="terminar d-flex justify-content-flex-end"
            v-if="proyecto.estado === 'A'"
          >
            <Boton
              texto="Cancelar Proyecto"
              tema="danger"
              v-if="hasPermission('cancelar_proyecto')"
              @click="cancelar"
            />

            <Boton
              texto="Finalizar Proyecto"
              tema="success"
              v-if="hasPermission('finalizar_proyecto')"
              @click="finalizar"
            />
          </div>
        </div>
        <div class="accesos-directos">
          <template v-for="(accesoDirecto, idx) in accesosDirectos" >
            <div :key="idx" v-if="accesoDirecto.tienePermiso">
              <CardLink
                :titulo="accesoDirecto.titulo"
                :icono="accesoDirecto.icono"
                :link="accesoDirecto.link"
                :resaltado="accesoDirecto.resaltado"
              />
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import proyectoService from "@/services/proyectoService";
import sprintService from "@/services/sprintService";
import Boton from "@/components/Boton";
import Navbar from "@/components/Navbar";
import Alert from "@/helpers/alert";
import SidebarProyecto from "@/components/SidebarProyecto";
import CardLink from "@/components/CardLink";
import { mapGetters, mapState } from "vuex";

export default {
  components: {
    Navbar,
    Boton,
    SidebarProyecto,
    CardLink,
  },
  data() {
    return {
      proyecto: {
        id: 0,
        nombre: "",
        fecha_inicio: "",
        fecha_fin: "",
        scrum_master: {
          id: 0,
          nombre: "",
          email: "",
        },
      },
      accesosDirectos: [],
      sprintActivo: {
        id: 0,
        nombre: "",
        fecha_inicio: "",
        fecha_fin: "",
        estado: "",
      },
    };
  },
  computed: {
    ...mapState({
      me: (state) => state.proyecto.me,
    }),
    ...mapGetters({
      hasAnyPermission: "proyecto/hasAnyPermission",
      hasPermission: "proyecto/hasPermission",
    }),
  },
  watch: {
    me() {
      this.cargarAccesosDirectos()
    }
  },
  mounted() {
    this.load();
  },
  methods: {
    activarProyecto(proyecto) {
      proyectoService.activar(proyecto.id).then(() => {
        Alert.success("El proyecto ha sido activado con éxito.");
        this.load();
      });
    },
    load() {
      proyectoService.retrieve(this.$route.params["id"]).then((proyecto) => {
        this.proyecto = proyecto;
        this.cargarAccesosDirectos();
      });
      sprintService.list(this.$route.params["id"]).then((sprints) => {
        this.sprintActivo = sprints.find((sprint) => sprint.estado == 'A') ?? this.sprintActivo;
      });
    },
    cargarAccesosDirectos() {
      const id = this.proyecto.id;

      this.accesosDirectos = [
        {
          titulo: "Miembros",
          icono: "team",
          link: `/proyectos/${id}/miembros`,
          tienePermiso: this.hasPermission("ver_miembros"),
        },
        {
          titulo: "Autorización",
          icono: "key",
          link: `/proyectos/${id}/autorizacion`,
          tienePermiso: this.hasAnyPermission([
            "ver_roles_proyecto",
            "ver_permisos_proyecto",
          ]),
        },
        {
          titulo: "User Stories",
          icono: "card",
          link: `/proyectos/${id}/user-stories`,
          tienePermiso: this.hasPermission("ver_user_stories"),
        },
        {
          titulo: "Product Backlog",
          icono: "box",
          link: `/proyectos/${id}/backlog`,
          tienePermiso: this.hasPermission("ver_user_stories"),
        },
        {
          titulo: "Sprints",
          icono: "flag",
          link: `/proyectos/${id}/sprints`,
          tienePermiso: true,
        },
        {
          titulo: "Sprint Activo",
          icono: "flag",
          link: `/proyectos/${id}/sprints/${this.sprintActivo.id}`,
          resaltado: true,
          tienePermiso: this.sprintActivo.id != 0,
        },
      ];
    },
    finalizar() {
      proyectoService.finalizar(this.proyecto.id).then(() => {
        Alert.success("El proyecto ha sido finalizado con éxito.");
        this.load();
      });
    },
    cancelar() {
      proyectoService.cancelar(this.proyecto.id).then(() => {
        Alert.success("El proyecto ha sido cancelado con éxito.");
        this.load();
      });
    },
  },
};
</script>

<style lang="scss" scoped>
.body {
  display: flex;
}

.content {
  flex-direction: column;
  width: calc(100% - 380px);
  margin: 0 40px;
}

.cabecera {
  align-items: center;
  display: flex;
  justify-content: space-between;
  margin-bottom: 46px;
}

.iniciar {
  flex-shrink: 0;
  margin-left: 40px;
}

.accesos-directos {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(276px, 1fr));
  gap: 40px;
  place-items: center;

  & > div {
    max-width: 100%;
    min-width: 276px;
  }
}

.terminar > button {
  margin-left: 16px;
}
</style>
