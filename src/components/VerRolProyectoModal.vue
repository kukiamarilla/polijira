<template>
  <div>
    <Modal v-model="show" @input="$emit('input', show)">
      <h1>{{ rol.nombre }}</h1>
      <br /><br /><br />

      <Table height="350px">
        <TableHeader>
          <Th width="10%">ID</Th>
          <Th width="30%">Nombre</Th>
          <Th width="30%">Código</Th>
          <Th width="30%">Seleccionado</Th>
        </TableHeader>
        <TableBody>
          <Tr v-for="permiso in permisosSelection" :key="permiso.id">
            <Td width="10%">{{ permiso.id }}</Td>
            <Td width="30%">{{ permiso.nombre }}</Td>
            <Td width="30%">{{ permiso.codigo }}</Td>
            <Td width="30%">
              <Checkbox
                v-if="!haTerminadoProyecto"
                v-model="permiso.selected"
                :disabled="!canEdit"
                @input="toggle(permiso)"
              />
            </Td>
          </Tr>
        </TableBody>
      </Table>
      <div style="display: flex; justify-content: flex-end; margin-top: 30px">
        <Boton
          v-if="!haTerminadoProyecto"
          texto="Aceptar"
          tema="primary"
          width="163px"
          size="small"
          @click="save"
        />
      </div>
    </Modal>
  </div>
</template>

<script>
import Modal from "@/components/Modal";
import Boton from "@/components/Boton";
import Checkbox from "@/components/Checkbox";
import { Table, TableHeader, TableBody, Th, Tr, Td } from "@/components/Table";
import { mapGetters, mapState } from "vuex";
import rolProyectoService from "@/services/rolProyectoService";
import Alert from "@/helpers/alert";

export default {
  components: {
    Modal,
    Boton,
    Table,
    TableHeader,
    TableBody,
    Th,
    Tr,
    Td,
    Checkbox,
  },
  props: ["value", "permisos", "rol", "disabled"],
  computed: {
    haTerminadoProyecto() {
      return this.rol.proyecto.estado === 'F' || this.rol.proyecto.estado === 'C';
    },
    ...mapGetters({
      hasPermission: "proyecto/hasPermission",
    }),
    ...mapState({
      me: (state) => state.proyecto.me,
    }),
    canEdit() {
      return (
        !this.disabled &&
        this.hasPermission("modificar_roles_proyecto") &&
        this.rol.id != this.me.rol.id
      );
    },
  },
  watch: {
    rol() {
      this.permisosSelection = this.permisos.map((permiso) => ({
        ...permiso,
        selected: this.rol.permisos.some((p) => p.id == permiso.id),
      }));
    },
    value() {
      this.show = this.value;
    },
  },
  data() {
    return {
      permisosSelection: this.permisos.map((permiso) => ({
        ...permiso,
        selected: this.rol.permisos.some((p) => p.id == permiso.id),
      })),
      show: false,
    };
  },
  methods: {
    save() {
      this.show = false;
      this.$emit(
        "save",
        this.permisosSelection.filter((permiso) => permiso.selected)
      );
      this.$emit("input", this.show);
    },
    toggle(permiso) {
      if (permiso.selected) {
        rolProyectoService.agregarPermiso(this.rol.id, permiso).then(() => {
          Alert.success("El permiso se agregó exitosamente.");
        });
      } else {
        rolProyectoService.eliminarPermiso(this.rol.id, permiso).then(() => {
          Alert.success("El permiso se removió exitosamente.");
        });
      }
    },
  },
};
</script>

<style lang="scss" scoped></style>
