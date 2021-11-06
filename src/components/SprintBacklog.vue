<template>
  <Modal v-model="show" height="550px" v-if="userStory">
    <h2 class="titulo">User Story</h2>

    <div class="datos-de-registro">
      <div class="fila">
        <p>
          <span class="highlight">Título:</span> {{ userStory.user_story.nombre }}
        </p>
        <p>
          <span class="highlight">Horas Estimadas:</span> {{ userStory.horas_estimadas }}
        </p>
      </div>
      <div class="fila">
        <p>
          <span class="highlight">Miembro Asignado:</span> {{ userStory.desarrollador.miembro_proyecto.usuario.nombre }}
        </p>
        <p>
          <span class="highlight">Prioridad:</span>
          {{ userStory.user_story.prioridad }}
        </p>
      </div>
      <div>
        <label class="highlight">Descripción:</label>
        <p class="multiline">{{ userStory.user_story.descripcion }}</p>
      </div>
    </div>

    <!-- <h4>Versiones del User Story</h4>
    <Table height="200px" v-if="us.registros.length > 0">
      <TableHeader>
        <Th class="pl-8" width="10%">ID</Th>
        <Th width="45%">Autor</Th>
        <Th width="45%">Fecha de creación</Th>
      </TableHeader>
      <TableBody>
        <Tr
          v-for="(registro, idx) in us.registros"
          :class="{ seleccionado: seleccionado == idx }"
          :key="registro.id"
          @click.native="verRegistro(idx)"
        >
          <Td class="pl-8" width="10%">{{ registro.id }}</Td>
          <Td width="45%">{{ registro.autor.usuario.nombre }}</Td>
          <Td width="45%">{{ formatearFecha(registro.fecha) }}</Td>
        </Tr>
      </TableBody>
    </Table> -->
  </Modal>
</template>

<script>
import Modal from "@/components/Modal";
// import Table from "@/components/Table/Table";
// import TableHeader from "@/components/Table/TableHeader";
// import TableBody from "@/components/Table/TableBody";
// import Th from "@/components/Table/Th";
// import Tr from "@/components/Table/Tr";
// import Td from "@/components/Table/Td";

export default {
  components: {
    Modal,
    // Table,
    // TableHeader,
    // TableBody,
    // Th,
    // Tr,
    // Td,
  },
  props: ["value", "userStory"],
  computed: {
  },
  data() {
    return {
      seleccionado: 0,
      show: false,
    };
  },
  watch: {
    value() {
      this.show = this.value;
    },
    show() {
      if (!this.show) this.$emit("input", null);
    },
  },
  methods: {
    formatearFecha(date) {
      const fecha = new Date(date);

      const dia = fecha.getDate();
      const mes = fecha.getMonth() + 1;
      const año = fecha.getFullYear();

      return `${this.fill(dia)}/${this.fill(mes)}/${año}`;
    },
    fill(numero) {
      if (numero < 10) return `0${numero}`;
      else return numero;
    }
  },
};
</script>

<style lang="scss" scoped>
.titulo {
  margin-bottom: 64px;
}

.fila {
  display: flex;

  p {
    width: 50%;
  }
}

h4 {
  margin: 32px 0;
}

p {
  margin: 0;
  padding: 0 0 32px 0;
}

.multiline {
  padding: 32px;
}

.row {
  cursor: pointer;

  &:hover {
    background-color: var(--gray-5);
  }

  &.seleccionado {
    background-color: var(--primary);
    color: white;
    cursor: default;
  }
}

.pl-8 {
  padding-left: 8px;
}
</style>
