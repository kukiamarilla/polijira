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
            <div class="d-flex" style="gap: 16px">
              <a
                href="#"
                title="Reemplazar miembro"
              >
                <Icon
                  icono="reemplazar"
                  size="16px"
                  color="#bdbdbd"
                  hover="var(--primary)"
                />
              </a>
              <a
                href="#"
                title="Eliminar miembro"
                @click.prevent="eliminar(miembro)"
              >
                <Icon
                  icono="delete"
                  size="16px"
                  color="#bdbdbd"
                  hover="var(--danger)"
                />
              </a>
            </div>
          </Td>
        </Tr>
      </TableBody>
    </Table>
  </div>
</template>

<script>
import { Table, TableHeader, TableBody, Th, Tr, Td } from '@/components/Table' 
import sprintService from '@/services/sprintService'
import Icon from '@/components/Icon.vue'
import miembroSprintService from '@/services/miembroSprintService'
export default {
  components: {
    Table,
    TableHeader,
    TableBody,
    Th,
    Tr,
    Td,
    Icon
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
    },
    eliminar(miembro) {
      miembroSprintService.eliminar(miembro.id).then(() => {
        this.load()
      })
    }
  },
}
</script>

<style lang="scss" scoped>

</style>