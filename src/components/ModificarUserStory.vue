<template>
  <Modal v-model="show" width="496px">
    <h1>Modificar User Story</h1>
    <br><br>
    <InputText
      title="Nombre:"
      v-model="userStoryUpdating.nombre"
    />
    <TextArea
      title="Descripción:"
      v-model="userStoryUpdating.descripcion"
    />
    <InputNumber
      title="Prioridad:"
      v-model="userStoryUpdating.prioridad"
      :min="1"
      :max="10"
    />
    <div class="d-flex justify-content-flex-end">
      <Boton texto="Actualizar" tema="primary" @click="crearUserStory"/>
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
  props: ["value", "userStory"],
  data() {
    return {
      show: false,
      userStoryUpdating: {
        nombre: "",
        descripcion: "",
        prioridad: "",
        proyecto: parseInt(this.$route.params["id"])
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
    },
    userStory() {
      this.userStoryUpdating = this.userStory
    }

  },
  methods: {
    crearUserStory() {
      userStoryService.update(this.userStory.id, this.userStory).then(() => {
        this.$emit('input', false);
        Alert.success("User Story modificado exitosamente")
      })
    }
  }
}
</script>

<style lang="scss" scoped>
  .justify-content-flex-end{
    justify-content: flex-end;
  }
</style>