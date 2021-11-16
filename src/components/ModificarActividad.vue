<template>
  <div class="container">
    <br><br>
    <InputText
      title="Título:"
      v-model="actividadModificar.titulo"
    />
    <TextArea
      title="Descripción:"
      v-model="actividadModificar.descripcion"
    />
    <InputNumber
      title="Horas:"
      v-model="actividadModificar.horas"
      :min="0"
    />
    <div class="d-flex justify-content-flex-end">
      <Boton texto="Cancelar" tema="secondary" @click="$emit('cerrar')"/>
      &nbsp;
      &nbsp;
      <Boton texto="Actualizar" tema="primary" @click="actualizarActividad"/>
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
    props: ['actividad'],
    components: {
        InputText,
        TextArea,
        InputNumber,
        Boton
    },
    data() {
      return {
        actividadModificar: this.actividad
      }
    },
    watch: {
      actividad() {
        this.actividadModificar = this.actividad
      }
    },
    methods: {
      actualizarActividad() {
        userStoryService.actualizarActividad(this.actividadModificar.id, this.actividadModificar).then(() => {
          Alert.success('Actividad actualizada correctamente')
          this.$emit('cerrar')
        })
      }
    }
}
</script>

<style>

</style>