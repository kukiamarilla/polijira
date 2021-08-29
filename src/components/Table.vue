<template>
  <div class="table">
    <div class="header">
      <div class="row">
        <div v-for="th in headers" :key="th.name" :style="{ width: th.width }">
          {{ th.name }}
        </div>
      </div>
    </div>
    <div class="body">
      <div class="row" v-for="(tr, rowIdx) in rows" :key="rowIdx">
        <div
          v-for="(td, col, colIdx) in tr"
          :key="`${rowIdx}-${colIdx}`"
          :style="{ width: colWidth(col) }"
        >
          {{ td }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      headers: [
        { name: "ID", width: "5%" },
        { name: "Nombre", width: "25%" },
        { name: "Email", width: "25%" },
        { name: "Rol", width: "25%" },
        { name: "Activado", width: "20%" },
      ],
      rows: [
        {
          ID: 1,
          Nombre: "Isaac Gabriel Amarilla Benítez",
          Email: "sc.amarilla@gmail.com",
          Rol: "Tirano",
          Activado: "activado",
        },
        {
          ID: 2,
          Nombre: "Ramon Francisco Perdomo Rivas",
          Email: "rperdomorivas@gmail.com",
          Rol: "Esclavo",
          Activado: "activado",
        },
        {
          ID: 3,
          Nombre: "Nerea Monserrat Ortiz Martinez",
          Email: "nmoortiz@gmail.com",
          Rol: "Esclavo",
          Activado: "activado",
        },
        {
          ID: 4,
          Nombre: "Jorge Sebastián Cane Avalos",
          Email: "canesi12@gmail.com",
          Rol: "Esclavo",
          Activado: "activado",
        },
      ],
    };
  },
  computed: {
    colWidthMap() {
      const map = {};

      for (const th of this.headers) {
        map[th.name] = th.width;
      }

      return map;
    },
  },
  methods: {
    colWidth(colName) {
      return this.colWidthMap[colName];
    },
  },
};
</script>

<style lang="scss" scoped>
.table {
  --space-between-rows: 12px;
  --space-between-columns: 36px;
  height: 150px;
}

.body {
  padding-top: var(--space-between-rows);
  max-height: 100%;
  overflow: scroll;
}

.header {
  border-bottom: 1px solid var(--gray-4);
  border-top: 1px solid var(--gray-4);
  overflow-y: scroll;
  padding: 16px 0;
}

.row {
  display: flex;
}

.body > .row {
  display: flex;
  padding-bottom: var(--space-between-rows);
  padding-top: var(--space-between-rows);
}

.header > .row > div {
  font-weight: bold;

  & + div {
    padding-left: var(--space-between-columns);
  }
}

.body > .row > div + div {
  padding-left: var(--space-between-columns);
}
</style>
