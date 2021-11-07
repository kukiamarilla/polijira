<template>
  <Modal v-model="show" width="496px">
    <h1>Nuevo Sprint</h1>
    <br><br>
    <InputDate
      title="Fecha de Inicio:"
      v-model="sprint.fecha_inicio"
    />
    <InputDate
      title="Fecha de Finalización:"
      v-model="sprint.fecha_fin"
    />
    <div class="d-flex justify-content-flex-end">
      <Boton texto="Guardar" tema="primary" @click="crearSprint"/>
    </div>
  </Modal>
</template>

<script>
import Modal from '@/components/Modal';
import InputDate from '@/components/InputDate';
import Boton from '@/components/Boton';
import sprintService from '@/services/sprintService';
import Alert from '@/helpers/alert';

export default {
  components: {
    Modal,
    InputDate,
    Boton
  },
  props: ["value"],
  data() {
    return {
      show: false,
      sprint: {
        fecha_inicio: "",
        fecha_fin: "",
        proyecto: this.$route.params["id"]
      }
    }
  },
  watch: {
    value() {
      this.show = this.value;
    },
    show() {
      if(!this.show) 
        this.$emit("input", false)
    }
  },
  methods: {
    crearSprint() {
      sprintService.create(this.sprint).then(() => {
        this.$emit('input', false);
        Alert.success("Sprint creado exitosamente")
      })
    }
  }
}
</script>

<style>
  .justify-content-flex-end{
    justify-content: flex-end;
  }
</style>