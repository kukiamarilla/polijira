<template>
  <div>
    <Table>
      <TableHeader>
        <Th width="10%">ID</Th>
        <Th width="30%">Nombre</Th>
        <Th width="30%">Email</Th>
        <Th width="30%">Acciones</Th>
      </TableHeader>
      <TableBody>
        <Tr v-for="miembro in miembros" :key="miembro.id">
          <Td width="10%">{{miembro.miembro_proyecto.usuario.id}}</Td>
          <Td width="30%">{{miembro.miembro_proyecto.usuario.nombre}}</Td>
          <Td width="30%">{{miembro.miembro_proyecto.usuario.email}}</Td>
          <Td width="30%">
          </Td>
        </Tr>
      </TableBody>
    </Table>
  </div>
</template>

<script>
import { Table, TableHeader, TableBody, Th, Tr, Td } from '@/components/Table' 
import sprintService from '@/services/sprintService'

export default {
  components: {
    Table,
    TableHeader,
    TableBody,
    Th,
    Tr,
    Td
  },
  data() {
    return {
      miembros: []
    }
  },
  mounted() {
    this.load()
  },
  methods: {
    load() {
      sprintService.miembros(this.$route.params.idSprint).then(miembros => {
        this.miembros = miembros
      })
    }
  },
}
</script>

<style>

</style>