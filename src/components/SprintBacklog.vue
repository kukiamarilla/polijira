<template>
  <div>
    <br>
    <div class="d-flex justify-content-flex-end">
      <Boton texto="Generar Reporte" tema="info"  @click="generatePdf()"/>
    </div>
    <br>
    <br>
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
    
    <VueHtml2Pdf
    :enable-download="true"
    :show-layout="false"
    :preview-modal="false"
    filename="sprint-backlog"
    :pdf-quality="2"
    :manual-pagination="true"
    pdf-format="legal"
    pdf-orientation="portrait"
    ref="pdfGenerator"
    >
      <SprintBacklogReport slot="pdf-content" :sprintBacklog="sprintBacklog" :sprint="sprint"/>
    </VueHtml2Pdf>
    <VerSprintBacklog v-model="verSprintBacklogShow" :userStory="verSprintBacklogSelected"/>
  </div>
</template>

<script>
import { Table, TableHeader, TableBody, Th, Tr, Td } from '@/components/Table' 
import sprintService from '@/services/sprintService'
import VerSprintBacklog from '@/components/VerSprintBacklog'
import Icon from '@/components/Icon'
import Boton from '@/components/Boton'
import SprintBacklogReport from '@/components/Reportes/SprintBacklogReport'
import VueHtml2Pdf from 'vue-html2pdf'

export default {
  props: ['sprint'],
  components: {
    Table,
    TableHeader,
    TableBody,
    Th,
    Tr,
    Td,
    VerSprintBacklog,
    Icon,
    VueHtml2Pdf,
    Boton,
    SprintBacklogReport
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
    },
    generatePdf(){
      this.$refs.pdfGenerator.generatePdf()
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