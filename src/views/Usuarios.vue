<template>
  <div>
    <Sidebar />
    <div class="container shadow">
      <h2>Usuarios</h2>

      <Table height="300px">
        <TableHeader>
          <Th width="20%">ID</Th>
          <Th width="20%">Nombre</Th>
          <Th width="20%">Email</Th>
          <Th width="20%">Rol</Th>
          <Th width="20%">Activado</Th>
        </TableHeader>
        <TableBody>
          <Tr v-for="(usuario, idx) in usuarios" :key="idx">
            <Td width="20%">{{ usuario.id }}</Td>
            <Td width="20%">{{ usuario.nombre }}</Td>
            <Td width="20%">{{ usuario.email }}</Td>
            <Td width="20%">
              <div class="select-container">
                <Select :options="roles" v-model="usuario.rol.id" />
              </div>
            </Td>
            <Td width="20%">
              <Checkbox v-model="usuario.activo" />
            </Td>
          </Tr>
        </TableBody>
      </Table>
    </div>
    <Waves />
  </div>
</template>

<script>
import Sidebar from "@/components/Sidebar";
import Waves from "@/components/Waves";
import Checkbox from "@/components/Checkbox";
import Select from "@/components/Select";
import { Table, TableHeader, TableBody, Th, Tr, Td } from "@/components/Table";
import usuarioService from "@/services/usuarioService";

export default {
  components: {
    Sidebar,
    Waves,
    Checkbox,
    Select,
    Table,
    TableHeader,
    TableBody,
    Th,
    Tr,
    Td,
  },
  created() {
    if (!this.$store.getters["auth/hasPermission"]("ver_usuarios"))
      this.$router.back();
  },
  mounted() {
    usuarioService.list().then((usuarios) => {
      this.usuarios = usuarios.map((u) => ({ ...u, activo: u.estado == "A" }));
    });
  },
  data() {
    return {
      roles: {
        1: "Tirano",
        2: "Esclavo",
      },
      usuarios: [],
    };
  },
};
</script>

<style lang="scss" scoped>
.container {
  background-color: white;
  border-radius: 20px;
  left: 110px;
  height: var(--absolute-remaining-height);
  min-height: 300px;
  padding: 40px;
  position: absolute;
  right: 88px;
}

h2 {
  margin-bottom: 58px;
}
</style>
