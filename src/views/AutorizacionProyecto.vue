<template>
  <div>
    <Navbar />
    <div class="d-flex">
      <SidebarProyecto current="autorizacion" :proyecto="proyecto" />

      <div class="container">
        <div class="box role-list shadow" v-if="hasPermission('ver_roles')">
          <h2 class="title">Roles de {{ proyecto.nombre }}</h2>
          <Table height="160px">
            <TableHeader>
              <Th width="20%">ID</Th>
              <Th width="40%">Nombre</Th>
              <Th width="40%">Acciones</Th>
            </TableHeader>
            <TableBody>
              <Tr v-for="rol in roles" :key="rol.id">
                <Td width="20%">{{ rol.id }}</Td>
                <Td width="40%">{{ rol.nombre }}</Td>
                <Td width="40%">
                  <div class="acciones" style="display: flex">
                    <a href="#" @click.prevent="verRol(rol)">
                      <Icon
                        icono="watch"
                        size="16px"
                        color="#bdbdbd"
                        hover="#51ABFF"
                      />
                    </a>
                    <a
                      href="#"
                      @click.prevent="eliminarRol(rol)"
                      v-if="rol.nombre != 'Scrum Master'"
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
                      @click.prevent="abrirModificarModal(rol)"
                      v-if="rol.nombre != 'Scrum Master'"
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

        <div class="box create-role shadow">
          <h2 class="title">Nuevo Rol</h2>
          <InputText title="Nombre" v-model="nuevoRol.nombre" />
          <div class="align-self-end">
            <Boton
              texto="Siguiente"
              tema="primary"
              width="163px"
              @click="seleccionarPermisos"
            />
          </div>
        </div>

        <div class="box permissions shadow">
          <h2 class="title">Permisos</h2>
          <Table height="540px">
            <TableHeader>
              <Th width="20%">ID</Th>
              <Th width="40%">Nombre</Th>
              <Th width="40%">Código</Th>
            </TableHeader>
            <TableBody>
              <Tr v-for="permiso in permisos" :key="permiso.id">
                <Td width="20%">{{ permiso.id }}</Td>
                <Td width="40%">{{ permiso.nombre }}</Td>
                <Td width="40%">{{ permiso.codigo }}</Td>
              </Tr>
            </TableBody>
          </Table>
        </div>
      </div>
    </div>
    <NuevoRolModal
      :permisos="permisos"
      v-model="nuevoRolModal"
      @save="crearRol($event)"
    />
    <VerRolProyectoModal
      :permisos="permisos"
      v-model="verRolModal"
      :rol="rolSelected"
      :disabled="rolSelected.nombre == 'Scrum Master'"
    />
    <Modal v-model="modificarRolModal" height="350px">
      <h1>Modificar Rol</h1>
      <br /><br /><br />
      <InputText title="Nombre" v-model="rolSelected.nombre" />
      <br /><br />
      <Boton
        texto="Guardar"
        tema="primary"
        width="163px"
        @click="modificarRol()"
      />
    </Modal>
  </div>
</template>

<script>
import Navbar from "@/components/Navbar";
import NuevoRolModal from "@/components/NuevoRolModal";
import VerRolProyectoModal from "@/components/VerRolProyectoModal";
import Modal from "@/components/Modal";
import SidebarProyecto from "@/components/SidebarProyecto";
import Boton from "@/components/Boton";
import Icon from "@/components/Icon";
import InputText from "@/components/InputText";
import { mapGetters, mapState } from "vuex";
import { Table, TableHeader, TableBody, Th, Tr, Td } from "@/components/Table";
import permisoProyectoService from "@/services/permisoProyectoService";
import proyectoService from "@/services/proyectoService";
import rolProyectoService from "@/services/rolProyectoService";
import Alert from "@/helpers/alert";

export default {
  components: {
    Navbar,
    SidebarProyecto,
    Boton,
    Table,
    TableHeader,
    TableBody,
    Th,
    Tr,
    Td,
    Icon,
    InputText,
    NuevoRolModal,
    VerRolProyectoModal,
    Modal,
  },
  created() {},
  mounted() {
    this.load();
  },
  computed: {
    ...mapState({
      me: (state) => state.auth.me,
    }),
    ...mapGetters({
      hasAnyPermission: "auth/hasAnyPermission",
      hasPermission: "auth/hasPermission",
    }),
  },
  data() {
    return {
      proyecto: {
        nombre: "",
      },
      buscar: "",
      nuevoRolModal: false,
      verRolModal: false,
      modificarRolModal: false,
      rolSelected: {
        nombre: "",
        permisos: [],
      },
      nuevoRol: {
        nombre: "",
        proyecto: 0,
        permisos: [],
      },
      roles: [],
      permisos: [],
    };
  },
  methods: {
    load() {
      permisoProyectoService.list().then((permisos) => {
        this.permisos = permisos;
      });
      rolProyectoService.list(this.$route.params["id"]).then((roles) => {
        this.roles = roles;
      });
      proyectoService.retrieve(this.$route.params["id"]).then((proyecto) => {
        this.proyecto = proyecto;
        this.nuevoRol = { ...this.nuevoRol, proyecto: proyecto.id };
      });
    },
    seleccionarPermisos() {
      this.nuevoRolModal = true;
    },
    crearRol(permisos) {
      let nuevoRol = this.nuevoRol;
      nuevoRol.permisos = permisos;
      this.nuevoRol = nuevoRol;
      rolProyectoService.create(this.nuevoRol).then((rol) => {
        Alert.success("El Rol se ha creado correctamente.");
        this.roles = [...this.roles, rol];
      });
      this.nuevoRolModal = false;
    },
    verRol(rol) {
      this.rolSelected = rol;
      this.verRolModal = true;
    },
    eliminarRol(rol) {
      let confirmation = confirm(
        "¿Está seguro que desea eliminar este rol?. Esta acción es irreversible."
      );
      if (confirmation)
        rolProyectoService.delete(rol.id).then(() => {
          Alert.success("Rol eliminado correctamente.");
          this.load();
        });
    },
    abrirModificarModal(rol) {
      this.rolSelected = rol;
      this.modificarRolModal = true;
    },
    modificarRol() {
      rolProyectoService
        .update(this.rolSelected.id, this.rolSelected)
        .then(() => {
          Alert.success("Rol modificado correctamente.");
          this.load();
          this.modificarRolModal = false;
        });
    },
  },
};
</script>

<style lang="scss" scoped>
.container {
  display: grid;
  gap: 24px;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  height: 100%;
  padding: 0 40px 40px 40px;
  position: relative;
  width: calc(100% - 340px);
  .box {
    background-color: white;
    border-radius: 20px;
    padding: 40px;
  }

  .title {
    margin-bottom: 40px;
  }

  .create-role {
    display: flex;
    flex-direction: column;
    grid-column: 1 / 2;
    grid-row: 2 / 3;
  }

  .role-list {
    grid-column: 1 / 2;
    grid-row: 1 / 2;
  }

  .permissions {
    grid-column: 2 / 3;
    grid-row: 1 / 3;
  }
}
.acciones a {
  padding-right: 16px;
}
.waves {
  position: absolute;
  bottom: 0;
}
</style>
