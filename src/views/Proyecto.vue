<template>
  <div>
    <Navbar />
    <div class="body">
      <SidebarProyecto :proyecto="proyecto" current="home" />
      <div class="d-flex content">
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
        <div class="backlog">
          <ProductBacklog />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import proyectoService from "@/services/proyectoService";
import Boton from "@/components/Boton";
import Navbar from "@/components/Navbar";
import Alert from "@/helpers/alert";
import SidebarProyecto from "@/components/SidebarProyecto";
import ProductBacklog from "@/components/ProductBacklog";
import { mapGetters } from "vuex";

export default {
  components: {
    Navbar,
    Boton,
    SidebarProyecto,
    ProductBacklog,
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
    };
  },
  computed: {
    ...mapGetters({
      hasAnyPermission: "proyecto/hasAnyPermission",
      hasPermission: "proyecto/hasPermission",
    }),
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
.iniciar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 40px;
}
</style>