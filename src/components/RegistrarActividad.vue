<template>
  <div class="container">
    <br><br>
    <InputText
      title="Título:"
      v-model="actividad.titulo"
    />
    <TextArea
      title="Descripción:"
      v-model="actividad.descripcion"
    />
    <InputNumber
      title="Horas:"
      v-model="actividad.horas"
      :min="0"
    />
    <div class="d-flex justify-content-flex-end">
      <Boton texto="Cancelar" tema="secondary" @click="$emit('cerrar')"/>
      &nbsp;
      &nbsp;
      <Boton texto="Guardar" tema="primary" @click="crearActividad"/>
    </div>
  </div>
</template>

<script>

import InputText from '@/components/InputText';
import TextArea from '@/components/TextArea';
import InputNumber from '@/components/InputNumber';
import Boton from '@/components/Boton';
import Alert from '@/helpers/alert';
import userStoryService from '@/services/userStoryService';

export default {
  props: ["sprintBacklog"],
  components: {
    InputText,
    TextArea,
    InputNumber,
    Boton
  },
  data() {
    return {
      actividad: {
        titulo: '',
        descripcion: '',
        horas: 0,
        sprint_backlog: this.sprintBacklog.id
      }
    }
  },
  methods: {
    crearActividad() {
      userStoryService.registrarActividad(this.actividad).then(() => {
        Alert.success('Actividad registrada correctamente');
        this.$emit('cerrar');
      })
    }
  }
}
</script>

<style lang="scss" scoped>

</style>