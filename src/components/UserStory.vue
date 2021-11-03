<template>
  <Modal v-model="show" height="550px" v-if="us">
    <h2 class="titulo">User Story</h2>

    <div class="datos-de-registro">
      <div class="fila">
        <p>
          <span class="highlight">Título:</span> {{ us.registros[seleccionado].nombre_despues }}
        </p>
      </div>
      <div class="fila">
        <p>
          <span class="highlight">Prioridad:</span>
          {{ us.registros[seleccionado].prioridad_despues }}
        </p>
      </div>
      <div>
        <label class="highlight">Descripción:</label>
        <p class="multiline">{{ us.registros[seleccionado].descripcion_despues }}</p>
      </div>
    </div>

    <h4>Versiones del User Story</h4>
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
    </Table>
  </Modal>
</template>

<script>
import Modal from "@/components/Modal";
import Table from "@/components/Table/Table";
import TableHeader from "@/components/Table/TableHeader";
import TableBody from "@/components/Table/TableBody";
import Th from "@/components/Table/Th";
import Tr from "@/components/Table/Tr";
import Td from "@/components/Table/Td";

export default {
  components: {
    Modal,
    Table,
    TableHeader,
    TableBody,
    Th,
    Tr,
    Td,
  },
  props: ["value", "userStory"],
  computed: {
    miembroAsignado() {
      const dev = this.userStory.registros[this.seleccionado].desarrollador_despues;
      return dev ? dev : "No asignado.";
    },
    horasAsignadas() {
      const horas = this.userStory.registros[this.seleccionado].horas_estimadas_despues;
      return horas ? horas : "No estimado.";
    },
  },
  data() {
    return {
      seleccionado: 0,
      show: false,
      us: null
    };
  },
  watch: {
    value() {
      this.show = this.value != null;
      this.verRegistro(0);
    },
    show() {
      if (!this.show) this.$emit("input", null);
    },
    userStory() {
      this.us = {...this.userStory, registros: this.userStory.registros.sort((a, b) => a.id < b.id)}
    }
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
    },
    verRegistro(registro) {
      this.seleccionado = registro;
    },
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
