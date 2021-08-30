<template>
  <div>
    <Sidebar />
    <div class="container shadow">
      <h2>Usuarios</h2>

      <div class="table">
        <div class="header">
          <div class="row">
            <div style="width: 5%">ID</div>
            <div style="width: 25%">Nombre</div>
            <div style="width: 25%">Email</div>
            <div style="width: 25%">Rol</div>
            <div style="width: 20%">Activado</div>
          </div>
        </div>
        <div class="body">
          <div class="row" v-for="(usuario, idx) in usuarios" :key="idx">
            <div style="width: 5%">{{ usuario.ID }}</div>
            <div style="width: 25%">{{ usuario.Nombre }}</div>
            <div style="width: 25%">{{ usuario.Email }}</div>
            <div style="width: 25%">
              <Select :options="roles" v-model="usuario.Rol" />
            </div>
            <div style="width: 20%">
              <Checkbox v-model="usuario.Activado" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <Waves />
  </div>
</template>

<script>
import Sidebar from "@/components/Sidebar";
import Waves from "@/components/Waves";
import Checkbox from "@/components/Checkbox";
import Select from "@/components/Select";

export default {
  components: {
    Sidebar,
    Waves,
    Checkbox,
    Select,
  },
  data() {
    return {
      roles: {
        1: "Tirano",
        2: "Esclavo",
      },
      usuarios: [
        {
          ID: 1,
          Nombre: "Isaac Gabriel Amarilla Benítez",
          Email: "sc.amarilla@gmail.com",
          Rol: 1,
          Activado: true,
        },
        {
          ID: 2,
          Nombre: "Ramon Francisco Perdomo Rivas",
          Email: "rperdomorivas@gmail.com",
          Rol: 2,
          Activado: true,
        },
        {
          ID: 3,
          Nombre: "Nerea Monserrat Ortiz Martinez",
          Email: "nmoortiz@gmail.com",
          Rol: 2,
          Activado: true,
        },
        {
          ID: 4,
          Nombre: "Jorge Sebastián Cane Avalos",
          Email: "canesi12@gmail.com",
          Rol: 2,
          Activado: true,
        },
      ],
    };
  },
};
</script>

<style lang="scss" scoped>
.container {
  background-color: white;
  border-radius: 20px;
  left: 110px;
  height: var(--absolute-remaining-height);
  min-height: 300px;
  padding: 40px;
  position: absolute;
  right: 88px;
}

h2 {
  margin-bottom: 58px;
}
.table {
  --space-between-rows: 12px;
  --space-between-columns: 36px;
  height: 400px;
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
