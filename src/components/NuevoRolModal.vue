<template>
  <div>
    <Modal v-model="show" @input="$emit('input', show)">
      <h1>Seleccione los Permisos</h1>
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
              <Checkbox v-model="permiso.selected" />
            </Td>
          </Tr>
        </TableBody>
      </Table>
      <div style="display: flex; justify-content: flex-end; margin-top: 30px">
        <Boton
          texto="Guardar"
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
  props: ["value", "permisos"],
  watch: {
    permisos() {
      this.permisosSelection = this.permisos.map((permiso) => ({
        ...permiso,
        selected: false,
      }));
    },
    value() {
      this.show = this.value;
    },
  },
  data() {
    return {
      permisosSelection: (this.permisosSelection = this.permisos.map(
        (permiso) => ({
          ...permiso,
          selected: false,
        })
      )),
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
  },
};
</script>

<style>
</style>