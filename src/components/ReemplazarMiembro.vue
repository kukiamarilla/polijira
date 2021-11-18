<template>
  <Modal v-model="show" v-if="value">
    <h2>Modificar Miembro</h2>
    <div class="form-group">
      <p>
        <span class="highlight">Reemplazar a:</span>
        <br><br> {{value.miembro_proyecto.usuario.nombre}}
      </p>
      <br>
      <br>
      <p>
        <span class="highlight">Por: </span>
      </p>
      <Select :options="selectOptions" v-model="miembroSelected" />
      <div class="d-flex justify-content-flex-end">
        <Boton texto="Reemplazar" tema="primary" @click="reemplazar"/>
      </div>
    </div>
  </Modal>
</template>

<script>
import Modal from './Modal.vue'
import sprintService from '@/services/sprintService'
import miembroService from '@/services/miembroService'
import Select from './Select.vue'
import Boton from './Boton.vue'
import miembroSprintService from '@/services/miembroSprintService'
import Alert from '@/helpers/alert'

export default {
  components: { Modal, Select, Boton },
  props: ['value'],
  data() {
    return {
      show: false,
      miembros: [],
      miembrosSprint: [],
      miembroSelected: -1,
    }
  },
  watch: {
    value () {
      this.show = this.value !== null
      if(this.value)
        this.load()
    },
    show() {
      if(!this.show) {
        this.$emit('input', null)
      }
    },
  },
  computed: {
    miembrosFaltantes() {
      return this.miembros.filter(miembro => {
        return !this.miembrosSprint.find(miembroSprint => {
          return miembroSprint.miembro_proyecto.id === miembro.id
        })
      })
    },
    selectOptions() {
      return this.miembrosFaltantes.map(miembro => miembro.usuario.nombre)
    }
  },
  methods: {
    load() {
      miembroService.list(this.value.miembro_proyecto.proyecto.id).then(response => {
        this.miembros = response
      })
      sprintService.miembros(this.value.sprint).then(response => {
        this.miembrosSprint = response
      })
    },
    reemplazar() {
      const miembroSeleccionado = this.miembrosFaltantes[this.miembroSelected]

      miembroSprintService.reemplazar(this.value.id, {miembro: miembroSeleccionado.id}).then(() => {
        Alert.success('Miembro reemplazado')
        this.show = false
      })
    }
  }
}
</script>

<style lang="scss" scoped>
  .form-group {
    margin-top: 40px;
  }
</style>