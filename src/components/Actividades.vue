<template>
  <div>
    <div class="d-flex justify-content-flex-end">
      <Boton tema="primary" texto="Registrar Actividad" @click="registrar = true" v-if="sprintBacklog.desarrollador.miembro_proyecto.id == me.id"></Boton>
    </div>
    <div class="actividades" v-if="!registrar && !modificar">
      <Actividad v-for="actividad in actividades" :key="actividad.id" :actividad="actividad" @eliminar="load" @modificar="modificarActividad"/>
    </div>
    <RegistrarActividad v-if="registrar &&  sprintBacklog.desarrollador.miembro_proyecto.id == me.id" @cerrar="registrar = false; load()" :sprintBacklog="sprintBacklog"/>
    <ModificarActividad v-if="modificar &&  sprintBacklog.desarrollador.miembro_proyecto.id == me.id" @cerrar="modificar = false; load()" :actividad="actividadModificar"/>
  </div>
</template>

<script>
import Boton from '@/components/Boton.vue'
import RegistrarActividad from '@/components/RegistrarActividad.vue'
import ModificarActividad from '@/components/ModificarActividad.vue'
import Actividad from '@/components/Actividad.vue'
import userStoryService from '@/services/userStoryService'
import { mapState } from 'vuex'

export default {
  props: ['sprintBacklog'],
  components: {
    Boton,
    Actividad,
    RegistrarActividad,
    ModificarActividad
  },
  data() {
    return {
      actividades: [],
      registrar: false,
      modificar: false,
      actividadModificar: null,
    }
  },
  computed: {
    ...mapState("proyecto", ["me"])
  },
  mounted() {
    this.load()
  },
  methods: {
    load() {
      userStoryService.actividades(this.sprintBacklog.id).then(actividades => {
        this.actividades = actividades
      })
    },
    modificarActividad(actividad) {
      this.actividadModificar = actividad
      this.modificar = true
    }
  }
}
</script>

<style lang="scss" scoped>
.actividades {
  margin-top: 16px;
}
</style>