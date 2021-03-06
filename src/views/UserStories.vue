<template>
  <div>
    <Navbar />
    <div class="d-flex">
      <SidebarProyecto current="user-stories" :proyecto="proyecto" />
      <div class="container shadow">
        <div class="d-flex header">
          <h2>User Stories de {{ proyecto.nombre }}</h2>
        </div>
        <Table height="400px" v-if="userStories.length > 0">
          <TableHeader>
            <Th width="10%">ID</Th>
            <Th width="15%">Nombre</Th>
            <Th width="45%">Descripción</Th>
            <Th width="10%">Prioridad</Th>
            <Th width="20%">Acciones</Th>
          </TableHeader>
          <TableBody>
            <Tr v-for="(userStory, idx) in userStories" :key="idx">
              <Td width="10%">{{ userStory.id }}</Td>
              <Td width="15%">{{ userStory.nombre }}</Td>
              <Td width="45%"
                ><span class="cutted-text">{{
                  userStory.descripcion
                }}</span></Td
              >
              <Td width="10%">{{ userStory.prioridad }}</Td>
              <Td width="20%">
                <div class="acciones" style="display: flex">
                  <a
                    href="#"
                    @click.prevent="verUserStory(userStory)"
                    v-if="hasProyectoPermissions(['ver_user_stories'])"
                  >
                    <Icon
                      icono="watch"
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
          <h2>Aun no hay User Stories en el Proyecto</h2>
        </div>
      </div>
    </div>
    <UserStory
      v-model="verModalUserStory"
      :userStory="userStory"
      @input="load"
      v-if="hasProyectoPermissions(['ver_user_stories'])"
    />
  </div>
</template>

<script>
import Navbar from "@/components/Navbar";
import SidebarProyecto from "@/components/SidebarProyecto";
import Icon from "@/components/Icon";
import { Table, TableHeader, TableBody, Th, Tr, Td } from "@/components/Table";
import userStoryService from "@/services/userStoryService";
import proyectoService from "@/services/proyectoService";
import Alert from "@/helpers/alert";
import { mapGetters, mapState } from "vuex";
import UserStory from "@/components/UserStory";

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
    UserStory,
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
    }),
    canActivate() {
      return this.hasPermission("activar_usuarios");
    },
    canDeactivate() {
      return this.hasPermission("desactivar_usuarios");
    },
    rolesSelect() {
      let rolesSelect = {};
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
      userStories: [],
      userStory: {
        id: 0,
        nombre: "",
      },
      verModalUserStory: false,
    };
  },
  methods: {
    load() {
      proyectoService.retrieve(this.$route.params["id"]).then((proyecto) => {
        this.proyecto = proyecto;
      });
      userStoryService.list(this.$route.params["id"]).then((userStories) => {
        this.userStories = userStories;
      });
    },
    asignarRol(userStory) {
      let actualizado = {
        usuario: userStory.usuario.id,
        rol: userStory.rolSelect,
        proyecto: userStory.proyecto.id,
      };
      userStoryService
        .update(userStory.id, actualizado)
        .then(() => {
          Alert.success("Se ha asignado correctamente el nuevo rol");
        })
        .catch(() => {
          this.load();
        });
    },
    verUserStory(userStory) {
      this.verModalUserStory = true;
      this.userStory = userStory;
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
.empty {
  height: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
  h2 {
    color: var(--gray-4);
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
