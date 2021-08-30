<template>
  <div>
    <Sidebar />

    <div class="container">
      <div class="box create-role shadow">
        <h2 class="title">Nuevo Rol</h2>

        <label class="highlight">Nombre</label>
        <input type="text" />

        <div class="align-self-end">
          <Boton texto="Guardar" tema="primary" width="163px" />
        </div>
      </div>

      <div class="box role-list shadow">
        <h2 class="title">Roles</h2>
      </div>

      <div class="box permissions shadow">
        <h2 class="title">Permisos</h2>
      </div>
    </div>

    <Waves class="waves" />
  </div>
</template>

<script>
import Sidebar from "@/components/Sidebar";
import Waves from "@/components/Waves";
import Boton from "@/components/Boton";

export default {
  components: {
    Sidebar,
    Waves,
    Boton,
  },
};
</script>

<style lang="scss" scoped>
.container {
  display: grid;
  gap: 24px;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  height: 100%;
  padding: 0 64px 75px 128px;
  position: relative;
  width: 100%;
  z-index: 1;

  .box {
    background-color: white;
    border-radius: 20px;
    padding: 40px;
  }

  .title {
    margin-bottom: 40px;
  }

  label {
    margin-bottom: 14px;
  }

  input[type="text"] {
    border: 1px solid var(--gray-4);
    border-radius: 5px;
    margin-bottom: 32px;
    padding: 8px 16px;
    width: 100%;
  }

  .create-role {
    display: flex;
    flex-direction: column;
    grid-column: 1 / 2;
    grid-row: 1 / 2;
  }

  .role-list {
    grid-column: 1 / 2;
    grid-row: 2 / 3;
  }

  .permissions {
    grid-column: 2 / 3;
    grid-row: 1 / 3;
  }
}

.waves {
  position: absolute;
  bottom: 0;
}
</style>
