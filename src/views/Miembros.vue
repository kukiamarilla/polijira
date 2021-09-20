<template>
  <div>
    <Navbar />
    <div class="d-flex">
      <SidebarProyecto current="miembros" :proyecto="proyecto" />
      <div class="container shadow">
        <div class="d-flex header">
          <h2>Miembros de {{ proyecto.nombre }}</h2>
          <Boton
            tema="primary"
            texto="Agregar Miembro"
            @click="agregarMiembroModal = true"
          />
        </div>
        <Table height="400px">
          <TableHeader>
            <Th width="20%">ID</Th>
            <Th width="20%">Nombre</Th>
            <Th width="20%">Email</Th>
            <Th width="20%">Rol</Th>
            <Th width="20%">Acciones</Th>
          </TableHeader>
          <TableBody>
            <Tr v-for="(miembro, idx) in miembros" :key="idx">
              <Td width="20%">{{ miembro.usuario.id }}</Td>
              <Td width="20%">{{ miembro.usuario.nombre }}</Td>
              <Td width="20%">{{ miembro.usuario.email }}</Td>
              <Td width="20%">
                <div
                  class="select-container"
                  v-if="
                    miembro.usuario.id != me.id &&
                    miembro.rol.nombre != 'Scrum Master'
                  "
                >
                  <Select
                    :options="rolesSelect"
                    v-model="miembro.rolSelect"
                    @input="asignarRol(miembro)"
                  />
                </div>
                <template v-else>
                  {{ miembro.rol.nombre }}
                </template>
              </Td>
              <Td width="20%">
                <div class="acciones" style="display: flex">
                  <a
                    href="#"
                    @click.prevent="eliminarMiembro(miembro)"
                    v-if="me.rol.id != miembro.rol.id"
                  >
                    <Icon
                      icono="delete"
                      size="16px"
                      color="#bdbdbd"
                      hover="#F25656"
                    />
                  </a>
                  <a
                    href="#"
                    @click.prevent="modificarHorario(miembro)"
                    v-if="me.rol.id != miembro.rol.id"
                  >
                    <Icon
                      icono="edit"
                      size="16px"
                      color="#bdbdbd"
                      hover="#FFB800"
                    />
                  </a>
                </div>
              </Td>
            </Tr>
          </TableBody>
        </Table>
      </div>
    </div>
    <AgregarMiembroModal v-model="agregarMiembroModal" @input="load" />
    <ModificarMiembroModal
      v-model="modificarMiembroModal"
      @input="load"
      :miembro="miembro"
    />
  </div>
</template>

<script>
import Navbar from "@/components/Navbar";
import SidebarProyecto from "@/components/SidebarProyecto";
import Icon from "@/components/Icon";
import Boton from "@/components/Boton";
import Select from "@/components/Select";
import { Table, TableHeader, TableBody, Th, Tr, Td } from "@/components/Table";
import miembroService from "@/services/miembroService";
import rolProyectoService from "@/services/rolProyectoService";
import proyectoService from "@/services/proyectoService";
import Alert from "@/helpers/alert";
import { mapGetters, mapState } from "vuex";
import AgregarMiembroModal from "@/components/AgregarMiembroModal";
import ModificarMiembroModal from "@/components/ModificarMiembroModal";

export default {
  components: {
    Navbar,
    SidebarProyecto,
    Icon,
    Boton,
    Select,
    Table,
    TableHeader,
    TableBody,
    Th,
    Tr,
    Td,
    AgregarMiembroModal,
    ModificarMiembroModal,
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
    }),
    ...mapState({
      me: (state) => state.auth.me,
    }),
    canActivate() {
      return this.hasPermission("activar_usuarios");
    },
    canDeactivate() {
      return this.hasPermission("desactivar_usuarios");
    },
    rolesSelect() {
      let rolesSelect = [];
      this.roles
        .filter((rol) => rol.nombre != "Scrum Master")
        .forEach((rol) => (rolesSelect[rol.id] = rol.nombre));
      return rolesSelect;
    },
  },
  data() {
    return {
      proyecto: {
        nombre: "",
      },
      roles: [],
      miembros: [],
      miembro: {
        horario: {
          id: 0,
          lunes: 0,
          martes: 0,
          miercoles: 0,
          jueves: 0,
          viernes: 0,
          sabado: 0,
          domingo: 0,
        },
      },
      agregarMiembroModal: false,
      modificarMiembroModal: false,
    };
  },
  methods: {
    load() {
      proyectoService.retrieve(this.$route.params["id"]).then((proyecto) => {
        this.proyecto = proyecto;
      });
      rolProyectoService.list(this.$route.params["id"]).then((roles) => {
        this.roles = roles;
        miembroService.list(this.$route.params["id"]).then((miembros) => {
          this.miembros = miembros.map((m) => ({
            ...m,
            rolSelect: this.roles.find((rol) => m.rol.id == rol.id).id,
          }));
          this.miembros = this.miembros.sort(
            (a, b) => a.usuario.id > b.usuario.id
          );
        });
      });
    },
    asignarRol(miembro) {
      let actualizado = {
        usuario: miembro.usuario.id,
        rol: miembro.rolSelect,
        proyecto: miembro.proyecto.id,
      };
      miembroService
        .update(miembro.id, actualizado)
        .then(() => {
          Alert.success("Se ha asignado correctamente el nuevo rol");
        })
        .catch(() => {
          this.load();
        });
    },
    eliminarMiembro(miembro) {
      let confimation = confirm(
        "Estás seguro que desea eliminar este miembro?"
      );
      if (confimation)
        miembroService.delete(miembro.id).then(() => {
          this.load();
          Alert.success("Se ha eliminado el miembro");
        });
    },
    modificarHorario(miembro) {
      this.miembro = miembro;
      this.modificarMiembroModal = true;
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
</style>
