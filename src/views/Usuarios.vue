<template>
  <div>
    <Sidebar />
    <div class="container shadow">
      <h2>Usuarios</h2>

      <Table>
        <TableHeader>
          <Th width="20%">ID</Th>
          <Th width="20%">Nombre</Th>
          <Th width="20%">Email</Th>
          <Th width="20%">Rol</Th>
          <Th width="20%">Activado</Th>
        </TableHeader>
        <TableBody>
          <Tr v-for="(usuario, idx) in usuarios" :key="idx">
            <Td width="20%">{{ usuario.ID }}</Td>
            <Td width="20%">{{ usuario.Nombre }}</Td>
            <Td width="20%">{{ usuario.Email }}</Td>
            <Td width="20%">
              <Select :options="roles" v-model="usuario.Rol" />
            </Td>
            <Td width="20%">
              <Checkbox v-model="usuario.Activado" />
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
  data() {
    return {
      roles: {
        1: "Tirano",
        2: "Esclavo",
      },
      usuarios: [
        {
          ID: 1,
          Nombre: "Isaac Gabriel Amarilla Benítez",
          Email: "sc.amarilla@gmail.com",
          Rol: 1,
          Activado: true,
        },
        {
          ID: 2,
          Nombre: "Ramon Francisco Perdomo Rivas",
          Email: "rperdomorivas@gmail.com",
          Rol: 2,
          Activado: true,
        },
        {
          ID: 3,
          Nombre: "Nerea Monserrat Ortiz Martinez",
          Email: "nmoortiz@gmail.com",
          Rol: 2,
          Activado: true,
        },
        {
          ID: 4,
          Nombre: "Jorge Sebastián Cane Avalos",
          Email: "canesi12@gmail.com",
          Rol: 2,
          Activado: true,
        },
      ],
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
