<template>
  <div class="container">
    <div class="d-flex">
      <div class="description">
        <span class="highlight">{{actividad.titulo}}</span>
        <br>
        <p>{{actividad.descripcion}}</p>
      </div>
      <div class="metadata">
        <span class="highlight">Hecho por: </span>{{actividad.desarrollador.nombre}}
        <br>
        <br>
        <span class="highlight">Horas trabajadas: </span> {{actividad.horas}} hs.
        <br>
        <br>
        <span class="highlight">Fecha: </span> {{actividad.fecha_creacion}}
      </div>
    </div>
    <div class="d-flex justify-content-flex-end">
      <a
        href="#"
        title="Modificar Actividades"
        v-if="actividad.desarrollador.id == me.id"
        @click.prevent="$emit('modificar', actividad)"
      >
        <Icon
          icono="edit"
          size="16px"
          color="#bdbdbd"
          hover="var(--primary)"
        />
      </a>
      &nbsp;
      &nbsp;
      <a
        href="#"
        title="Eliminar Actividades"
        v-if="actividad.desarrollador.id == me.id"
        @click.prevent="eliminar"
      >
        <Icon
          icono="delete"
          size="16px"
          color="#bdbdbd"
          hover="#F25656"
        />
      </a>
    </div>
  </div>
</template>

<script>
import Icon from '@/components/Icon.vue'
import userStoryService from '@/services/userStoryService'
import { mapState } from 'vuex'

export default {
  props: ['actividad'],
  components: {
    Icon
  },
  computed: {
    ...mapState("auth", ["me"])
  },
  methods: {
    eliminar() {
      const confirmacion = confirm("¿Estás seguro de eliminar esta actividad?")
      if (confirmacion) {
        userStoryService.eliminarActividad(this.actividad.id).then(() => {
          this.$emit('eliminar')
        })
      }
    }
  }
}
</script>

<style lang="scss" scoped>
  .container {
    width: 100%;
    padding: 24px;
    border: var(--gray-5) solid 1px;
    margin-bottom: 8px;
    border-radius: 5px;
  }
  .description {
    flex: 5

  }
  .metadata {
    flex: 2;
    margin-left: 32px;
  }
</style>