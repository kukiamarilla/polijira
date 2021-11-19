<template>
  <div>
    <Navbar />
    <div class="d-flex">
      <SidebarProyecto current="sprints" :proyecto="proyecto" />
      <div class="container shadow">
        <div class="d-flex header">
          <h2>Sprints de {{ proyecto.nombre }}</h2>
          <Boton
            texto="Crear Sprint"
            tema="primary"
            @click="crearSprintModal = true"
            v-if="
              !haTerminadoProyecto &&
              !sprints.some((sprint) => sprint.estado == 'P') &&
                proyecto.estado == 'A'
            "
          />
        </div>
        <Table height="400px" v-if="sprints.length > 0">
          <TableHeader>
            <Th width="10%">ID</Th>
            <Th width="15%">Nombre</Th>
            <Th width="15%">Inicio</Th>
            <Th width="15%">Fin</Th>
            <Th width="15%">Planificación</Th>
            <Th width="15%">Estado</Th>
            <Th width="15%">Acciones</Th>
          </TableHeader>
          <TableBody>
            <Tr v-for="(sprint, idx) in sprints" :key="idx">
              <Td width="10%">{{ sprint.id }}</Td>
              <Td width="15%">Sprint {{ sprint.numero }}</Td>
              <Td width="15%">{{sprint.fecha_inicio}}</Td>
              <Td
                width="15%"
                >{{sprint.fecha_fin_real ? sprint.fecha_fin_real : sprint.fecha_fin}}</Td
              >
              <Td width="15%"
                ><span
                  class="cutted-text"
                  >{{ sprint.estado_sprint_planning == "P" ? "Pendiente" :  sprint.estado_sprint_planning == "I" ? "Iniciado" : "Finalizado"}}</span
                ></Td
              >
              <Td width="15%"
                ><span
                  class="cutted-text"
                  >{{ sprint.estado == "P" ? "Pendiente" :  sprint.estado == "A" ? "Activo" : "Finalizado"}}</span
                ></Td
              >
              <Td width="15%">
                <div class="acciones" style="display: flex">
                  <a
                    href="#"
                    v-if="
                      hasProyectoPermissions(['planear_sprints']) &&
                        sprint.estado_sprint_planning == 'I'
                    "
                    title="Planificar Sprint"
                    @click.prevent="irAPlanificacion(sprint)"
                  >
                    <Icon
                      icono="watch"
                      size="16px"
                      color="#bdbdbd"
                      hover="#F25656"
                    />
                  </a>
                  <a
                    href="#"
                    v-if="
                      hasProyectoPermissions(['ver_sprints']) &&
                        (sprint.estado == 'A' || sprint.estado == 'F')
                    "
                    title="Ver Sprint"
                    @click.prevent="$router.push(`/proyectos/${proyecto.id}/sprints/${sprint.id}`)"
                  >
                    <Icon
                      icono="watch"
                      size="16px"
                      color="#bdbdbd"
                      hover="#F25656"
                    />
                  </a>
                  <a
                    href="#"
                    v-if="
                      hasProyectoPermissions(['planear_sprints']) &&
                        sprint.estado_sprint_planning == 'P'
                    "
                    @click.prevent="iniciarSprintPlanning(sprint)"
                  >
                    <Icon
                      icono="checklist"
                      size="16px"
                      color="#bdbdbd"
                      hover="#F25656"
                    />
                  </a>
                  <a
                    href="#"
                    v-if="
                      hasProyectoPermissions(['activar_sprints']) &&
                      sprint.estado_sprint_planning == 'F' &&
                      sprint.estado == 'P'
                    "
                    @click.prevent="activarSprint(sprint)"
                  >
                    <Icon
                      icono="play"
                      size="16px"
                      color="#bdbdbd"
                      hover="#F25656"
                    />
                  </a>
                  <a
                    href="#"
                    @click.prevent="eliminarSprint(sprint)"
                    v-if="
                      hasProyectoPermissions(['eliminar_sprints']) &&
                        sprint.estado == 'P' &&
                        sprint.estado_sprint_planning == 'P'
                    "
                  >
                    <Icon
                      icono="delete"
                      size="16px"
                      color="#bdbdbd"
                      hover="#F25656"
                    />
                  </a>
                </div>
              </Td>
            </Tr>
          </TableBody>
        </Table>
        <div class="empty" v-else>
          <h2>
            Aun no hay Sprints en el Proyecto.
            <a
              href="#"
              class="agregar"
              @click.prevent="crearSprintModal = true"
              v-if="proyecto.estado == 'A'"
              >Crear uno</a
            >
          </h2>
        </div>
      </div>
    </div>
    <CrearSprint
      v-model="crearSprintModal"
      v-if="hasProyectoPermissions(['crear_user_stories'])"
      @input="load"
    />
  </div>
</template>

<script>
import Navbar from "@/components/Navbar";
import SidebarProyecto from "@/components/SidebarProyecto";
import Icon from "@/components/Icon";
import { Table, TableHeader, TableBody, Th, Tr, Td } from "@/components/Table";
import sprintService from "@/services/sprintService";
import proyectoService from "@/services/proyectoService";
import { mapGetters, mapState } from "vuex";
import Boton from "@/components/Boton";
import CrearSprint from "@/components/CrearSprint";
import Alert from "@/helpers/alert";

export default {
  components: {
    Navbar,
    SidebarProyecto,
    Icon,
    Table,
    TableHeader,
    TableBody,
    Th,
    Tr,
    Td,
    Boton,
    CrearSprint,
  },
  created() {},
  mounted() {
    this.load();
  },
  computed: {
    haTerminadoProyecto() {
      return this.proyecto.estado === 'F' || this.proyecto.estado === 'C';
    },
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
    }),
  },
  data() {
    return {
      proyecto: {
        nombre: "",
      },
      sprints: [],
      crearSprintModal: false,
    };
  },
  methods: {
    load() {
      proyectoService.retrieve(this.$route.params["id"]).then((proyecto) => {
        this.proyecto = proyecto;
      });
      sprintService.list(this.$route.params["id"]).then((sprints) => {
        this.sprints = sprints;
      });
    },
    eliminarSprint(sprint) {
      sprintService.delete(sprint.id).then(() => {
        Alert.success("Sprint eliminado exitosamente");
        this.load();
      });
    },
    iniciarSprintPlanning(sprint) {
        sprintService.iniciarSprintPlanning(sprint.id).then(() => {
            Alert.success("Spring Planning iniciado.")
            this.$router.push(`/proyectos/${this.proyecto.id}/sprint-planning/${sprint.id}/paso-1`)
        })
    },
    activarSprint(sprint) {
        sprintService.activar(sprint.id).then(() => {
            Alert.success("Sprint activado exitosamente.")
            this.load();
        })
    },
    irAPlanificacion(sprint) {
     const paso = localStorage.getItem('sprint-planning-paso');
     this.$router.push(
          `/proyectos/${this.proyecto.id}/sprint-planning/${sprint.id}/paso-${ paso != null? paso : 1}`
        );
    }
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
.empty {
  height: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
  h2 {
    color: var(--gray-4);
    text-align: center;
    a.agregar {
      color: var(--primary-light);
      text-decoration: none;
      &:hover {
        color: var(--primary);
      }
    }
  }
}
span.cutted-text {
  width: 80%;
  display: block;
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
}
</style>
