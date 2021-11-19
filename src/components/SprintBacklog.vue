<template>
  <div>
    <Table>
      <TableHeader>
        <Th width="20%">ID</Th>
        <Th width="20%">Título</Th>
        <Th width="20%">Descripción</Th>
        <Th width="20%">Prioridad</Th>
        <Th width="20%">Acciones</Th>
      </TableHeader>
      <TableBody>
        <Tr v-for="us in sprintBacklog" :key="us.id">
          <Td width="20%">{{us.user_story.id}}</Td>
          <Td width="20%">{{us.user_story.nombre}}</Td>
          <Td width="20%"><span class="cutted-text">{{us.user_story.descripcion}}</span></Td>
          <Td width="20%">{{us.user_story.prioridad}}</Td>
          <Td width="20%">
            <a
              href="#"
              title="Ver User Story"
              @click.prevent="verSprintBacklog(us)"
            >
              <Icon
                icono="watch"
                size="16px"
                color="#bdbdbd"
                hover="#F25656"
              />
            </a>
          </Td>
        </Tr>
      </TableBody>
    </Table>
    <VerSprintBacklog v-model="verSprintBacklogShow" :userStory="verSprintBacklogSelected"/>
  </div>
</template>

<script>
import { Table, TableHeader, TableBody, Th, Tr, Td } from '@/components/Table' 
import sprintService from '@/services/sprintService'
import VerSprintBacklog from '@/components/VerSprintBacklog'
import Icon from '@/components/Icon'

export default {
  components: {
    Table,
    TableHeader,
    TableBody,
    Th,
    Tr,
    Td,
    VerSprintBacklog,
    Icon
  },
  data() {
    return {
      sprintBacklog: [],
      verSprintBacklogShow: false,
      verSprintBacklogSelected: null,
    }
  },
  mounted() {
    this.load()
  },
  methods: {
    load() {
      sprintService.sprintBacklog(this.$route.params.idSprint).then(sprintBacklog => {
        this.sprintBacklog = sprintBacklog
      })
    },
    verSprintBacklog(us) {
      this.verSprintBacklogSelected = us
      this.verSprintBacklogShow = true
    }
  },
}
</script>

<style lang="scss" scoped>
span.cutted-text{
  width: 80%;
  display: block;
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
}
</style>