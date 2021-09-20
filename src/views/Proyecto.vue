<template>
  <div>
    <Navbar />
    <div class="body">
      <SidebarProyecto :proyecto="proyecto" current="home" />
      <ProductBacklog />
    </div>
  </div>
</template>

<script>
import proyectoService from "@/services/proyectoService";
import Navbar from "@/components/Navbar";
import SidebarProyecto from "@/components/SidebarProyecto";
import ProductBacklog from "@/components/ProductBacklog";

export default {
  components: {
    Navbar,
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
  mounted() {
    proyectoService.retrieve(this.$route.params["id"]).then((proyecto) => {
      this.proyecto = proyecto;
    });
  },
};
</script>

<style scoped>
.body {
  display: flex;
}
</style>