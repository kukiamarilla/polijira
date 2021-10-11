<template>
  <Modal v-model="show" width="496px">
    <h1>Nuevo User Story</h1>
    <br><br>
    <InputText
      title="Nombre:"
      v-model="userStory.nombre"
    />
    <TextArea
      title="Descripción:"
      v-model="userStory.descripcion"
    />
    <InputNumber
      title="Prioridad:"
      v-model="userStory.prioridad"
      :min="1"
      :max="10"
    />
    <div class="d-flex justify-content-flex-end">
      <Boton texto="Guardar" tema="primary" @click="crearUserStory"/>
    </div>
  </Modal>
</template>

<script>
import Modal from '@/components/Modal';
import InputText from '@/components/InputText';
import TextArea from '@/components/TextArea';
import InputNumber from '@/components/InputNumber';
import Boton from '@/components/Boton';
import userStoryService from '@/services/userStoryService';
import Alert from '@/helpers/alert';

export default {
  components: {
    Modal,
    InputText,
    TextArea,
    InputNumber,
    Boton
  },
  props: ["value"],
  data() {
    return {
      show: false,
      userStory: {
        nombre: "",
        descripcion: "",
        prioridad: "",
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
    crearUserStory() {
      userStoryService.create(this.userStory).then(() => {
        this.$emit('input', false);
        Alert.success("User Story creado exitosamente")
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