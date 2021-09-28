<template>
  <div class="sidebar">
    <div class="proyecto">
      <div class="brand">
        <h2>{{ proyecto.nombre }}</h2>
      </div>
      <div class="menu">
        <SidebarProyectoItem
          icono="home"
          texto="Inicio"
          :to="`/proyectos/${proyecto.id}`"
          :active="current == 'home'"
        />
        <SidebarProyectoItem
          icono="key"
          texto="Autorizacion"
          :to="`/proyectos/${proyecto.id}/autorizacion`"
          :active="current == 'autorizacion'"
          v-if="hasProyectoPermission('ver_roles_proyecto')"
        />
        <SidebarProyectoItem
          icono="team"
          texto="Miembros"
          :to="`/proyectos/${proyecto.id}/miembros`"
          :active="current == 'miembros'"
          v-if="hasProyectoPermission('ver_miembros')"
        />
      </div>
    </div>
  </div>
</template>

<script>
import SidebarProyectoItem from "@/components/SidebarProyectoItem";
import { mapGetters } from "vuex";
export default {
  props: ["proyecto", "current"],
  components: { SidebarProyectoItem },
  computed: {
    ...mapGetters({
      hasProyectoPermission: "proyecto/hasPermission",
    }),
  },
};
</script>

<style lang="scss" scoped>
.sidebar {
  min-height: calc(var(--app-min-height) - 128px);
  background-color: var(--primary-dark);
  width: 300px;
  left: 0;
  border-top-right-radius: 20px;
  .brand {
    padding: 32px 0;
    h2 {
      color: #fff;
      margin-left: 56px;
    }
  }
}
</style>