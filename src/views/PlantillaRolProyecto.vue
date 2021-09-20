<template>
  <div>
    <Navbar />
    <Sidebar current="plantilla-rol-proyecto" />

    <div class="container">
      <div
        class="box plantilla-template-list shadow"
        v-if="hasPermission('ver_plantillas')"
      >
        <h2 class="title">Plantillas de Roles de Proyecto</h2>
        <Table height="160px">
          <TableHeader>
            <Th width="20%">ID</Th>
            <Th width="40%">Nombre</Th>
            <Th width="40%">Acciones</Th>
          </TableHeader>
          <TableBody>
            <Tr v-for="plantilla in plantillas" :key="plantilla.id">
              <Td width="20%">{{ plantilla.id }}</Td>
              <Td width="40%">{{ plantilla.nombre }}</Td>
              <Td width="40%">
                <div class="acciones" style="display: flex">
                  <a href="#" @click.prevent="verPlantilla(plantilla)">
                    <Icon
                      icono="watch"
                      size="16px"
                      color="#bdbdbd"
                      hover="#51ABFF"
                    />
                  </a>
                  <a
                    href="#"
                    @click.prevent="eliminarPlantilla(plantilla)"
                    v-if="
                      hasPermission('eliminar_plantillas') &&
                      plantilla.nombre != 'Scrum Master'
                    "
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
                    @click.prevent="abrirModificarModal(plantilla)"
                    v-if="
                      hasPermission('modificar_plantillas') &&
                      plantilla.nombre != 'Scrum Master'
                    "
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

      <div
        class="box create-plantilla-template shadow"
        v-if="hasPermission('crear_plantillas')"
      >
        <h2 class="title">Nueva Plantilla de Rol de Proyecto</h2>
        <InputText title="Nombre" v-model="nuevaPlantilla.nombre" />
        <div class="align-self-end">
          <Boton
            texto="Siguiente"
            tema="primary"
            width="163px"
            @click="seleccionarPermisos"
          />
        </div>
      </div>

      <div
        class="box permissions shadow"
        v-if="hasPermission('ver_plantillas')"
      >
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
    <NuevoRolModal
      :permisos="permisos"
      v-model="nuevaPlantillaModal"
      @save="crearPlantilla($event)"
    />
    <VerPlantillaRolModal
      :permisos="permisos"
      v-model="verPlantillaModal"
      :rol="plantillaSelected"
      :disabled="plantillaSelected.nombre == 'Scrum Master'"
    />
    <Modal v-model="modificarPlantillaModal" height="350px">
      <h1>Modificar Plantilla</h1>
      <br /><br /><br />
      <InputText title="Nombre" v-model="plantillaSelected.nombre" />
      <br /><br />
      <Boton
        texto="Guardar"
        tema="primary"
        width="163px"
        @click="modificarPlantilla()"
      />
    </Modal>
    <Waves class="waves" />
  </div>
</template>

<script>
import Navbar from "@/components/Navbar";
import NuevoRolModal from "@/components/NuevoRolModal";
import VerPlantillaRolModal from "@/components/VerPlantillaRolModal";
import Modal from "@/components/Modal";
import Sidebar from "@/components/Sidebar";
import Waves from "@/components/Waves";
import Boton from "@/components/Boton";
import Icon from "@/components/Icon";
import InputText from "@/components/InputText";
import { mapGetters, mapState } from "vuex";
import { Table, TableHeader, TableBody, Th, Tr, Td } from "@/components/Table";
import permisoProyectoService from "@/services/permisoProyectoService";
import plantillaService from "@/services/plantillaService";
import Alert from "@/helpers/alert";

export default {
  components: {
    Navbar,
    Sidebar,
    Waves,
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
    VerPlantillaRolModal,
    Modal,
  },
  created() {
    if (!this.hasAnyPermission(["ver_plantillas", "ver_permisos"]))
      this.$router.back();
  },
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
      buscar: "",
      nuevaPlantillaModal: false,
      verPlantillaModal: false,
      modificarPlantillaModal: false,
      plantillaSelected: {
        nombre: "",
        permisos: [],
      },
      nuevaPlantilla: {
        nombre: "",
        permisos: [],
      },
      plantillas: [],
      permisos: [],
    };
  },
  methods: {
    load() {
      permisoProyectoService.list().then((permisos) => {
        this.permisos = permisos;
      });
      plantillaService.list().then((plantillas) => {
        this.plantillas = plantillas;
      });
    },
    seleccionarPermisos() {
      this.nuevaPlantillaModal = true;
    },
    crearPlantilla(permisos) {
      let nuevaPlantilla = this.nuevaPlantilla;
      nuevaPlantilla.permisos = permisos;
      this.nuevaPlantilla = nuevaPlantilla;
      plantillaService.create(this.nuevaPlantilla).then((plantilla) => {
        Alert.success("La plantilla se ha creado correctamente.");
        this.plantillas = [...this.plantillas, plantilla];
      });
      this.nuevaPlantillaModal = false;
    },
    verPlantilla(plantilla) {
      this.plantillaSelected = plantilla;
      this.verPlantillaModal = true;
    },
    eliminarPlantilla(plantilla) {
      let confirmation = confirm(
        "¿Está seguro que desea eliminar esta Plantilla?. Esta acción es irreversible."
      );
      if (confirmation)
        plantillaService.delete(plantilla.id).then(() => {
          Alert.success("Plantilla eliminada correctamente.");
          this.load();
        });
    },
    abrirModificarModal(plantilla) {
      this.plantillaSelected = plantilla;
      this.modificarPlantillaModal = true;
    },
    modificarPlantilla() {
      plantillaService
        .update(this.plantillaSelected.id, this.plantillaSelected)
        .then(() => {
          Alert.success("Plantilla modificada correctamente.");
          this.load();
          this.modificarPlantillaModal = false;
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
  padding: 0 64px 75px 128px;
  position: relative;
  width: 100%;
  .box {
    background-color: white;
    border-radius: 20px;
    padding: 40px;
  }

  .title {
    margin-bottom: 40px;
  }

  .create-plantilla-template {
    display: flex;
    flex-direction: column;
    grid-column: 1 / 2;
    grid-row: 2 / 3;
  }

  .plantilla-template-list {
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
