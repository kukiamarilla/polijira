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
import plantillaService from "@/services/plantillaService";
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
    ...mapGetters({
      hasPermission: "auth/hasPermission",
    }),
    ...mapState({
      me: (state) => state.auth.me,
    }),
    canEdit() {
      return this.hasPermission("modificar_plantillas") && !this.disabled;
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
        plantillaService.agregarPermiso(this.rol.id, permiso).then(() => {
          Alert.success("El permiso se agregó exitosamente.");
        });
      } else {
        plantillaService.eliminarPermiso(this.rol.id, permiso).then(() => {
          Alert.success("El permiso se removió exitosamente.");
        });
      }
    },
  },
};
</script>

<style>
</style>