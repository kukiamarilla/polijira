<template>
  <div class="sidebar">
    <div class="principales">
      <IconLink
        class="icono"
        icono="home"
        descripcion="Home"
        link="/"
        :activo="current == 'home'"
      />
      <IconLink
        class="icono"
        icono="team"
        descripcion="Equipo"
        link="/usuarios"
        v-if="hasPermission('ver_usuarios')"
        :activo="current == 'usuarios'"
      />
      <IconLink
        class="icono"
        icono="key"
        descripcion="Autorización"
        link="/autorizacion"
        v-if="hasPermissions(['ver_roles', 'ver_permisos'])"
        :activo="current == 'autorizacion'"
      />
      <IconLink
        class="icono"
        icono="protected"
        descripcion="Plantillas de Rol de Proyecto"
        link="/plantilla-rol-proyecto"
        v-if="hasPermissions(['ver_roles', 'ver_permisos'])"
        :activo="current == 'plantilla-rol-proyecto'"
      />
    </div>

    <IconLink
      class="icono"
      icono="logout"
      descripcion="Cerrar Sesión"
      @click="logout"
    />
  </div>
</template>

<script>
import IconLink from "@/components/IconLink";
import { mapGetters } from "vuex";

export default {
  props: ["current"],
  components: {
    IconLink,
  },
  computed: {
    ...mapGetters({
      hasPermission: "auth/hasPermission",
      hasPermissions: "auth/hasPermissions",
      hasAnyPermission: "auth/hasAnyPermission",
    }),
  },
  methods: {
    logout() {
      this.$store.commit("auth/logout");
      this.$router.push("/login");
    },
  },
};
</script>

<style lang="scss" scoped>
.sidebar {
  align-items: center;
  background-color: white;
  border-radius: 0px 20px 20px 0px;
  box-shadow: 4px 0px 8px rgba(0, 0, 0, 0.125);
  display: flex;
  flex-direction: column;
  height: calc(100% - 8rem - 75px);
  justify-content: space-between;
  left: 0;
  min-height: 300px;
  position: absolute;
  padding: 20px;
  top: 128px;
  width: 65px;
  z-index: 1;
}

.principales {
  display: flex;
  flex-direction: column;
}

.icono {
  margin: 20px 0;
}
</style>
