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
        <Table height="160px">
          <TableHeader>
            <Th width="20%">ID</Th>
            <Th width="40%">Nombre</Th>
            <Th width="40%">Acciones</Th>
          </TableHeader>
          <TableBody>
            <Tr v-for="rol in roles" :key="rol.id">
              <Td width="20%">{{ rol.id }}</Td>
              <Td width="40%">{{ rol.nombre }}</Td>
              <Td width="40%">
                <div class="acciones" style="display: flex">
                  <a href="#">
                    <Icon
                      icono="watch"
                      size="16px"
                      color="#bdbdbd"
                      hover="#51ABFF"
                    />
                  </a>
                  <a href="#">
                    <Icon
                      icono="delete"
                      size="16px"
                      color="#bdbdbd"
                      hover="#F25656"
                    />
                  </a>
                  <a href="#">
                    <Icon
                      icono="edit"
                      size="16px"
                      color="#bdbdbd"
                      hover="#FFB800"
                    />
                  </a>
                </div>
              </Td>
            </Tr>
          </TableBody>
        </Table>
      </div>

      <div class="box permissions shadow">
        <h2 class="title">Permisos</h2>
        <Table height="540px">
          <TableHeader>
            <Th width="20%">ID</Th>
            <Th width="40%">Nombre</Th>
            <Th width="40%">Código</Th>
          </TableHeader>
          <TableBody>
            <Tr v-for="permiso in permisos" :key="permiso.id">
              <Td width="20%">{{ permiso.id }}</Td>
              <Td width="40%">{{ permiso.nombre }}</Td>
              <Td width="40%">{{ permiso.codigo }}</Td>
            </Tr>
          </TableBody>
        </Table>
      </div>
    </div>

    <Waves class="waves" />
  </div>
</template>

<script>
import Sidebar from "@/components/Sidebar";
import Waves from "@/components/Waves";
import Boton from "@/components/Boton";
import Icon from "@/components/Icon";
import { Table, TableHeader, TableBody, Th, Tr, Td } from "@/components/Table";

export default {
  components: {
    Sidebar,
    Waves,
    Boton,
    Table,
    TableHeader,
    TableBody,
    Th,
    Tr,
    Td,
    Icon,
  },
  data() {
    return {
      roles: [
        {
          id: 1,
          nombre: "Administrador",
        },
        {
          id: 2,
          nombre: "Usuario",
        },
      ],
      permisos: [
        {
          id: 1,
          nombre: "Ver Usuario",
          codigo: "ver_usuario",
        },
        {
          id: 2,
          nombre: "Ver Usuario",
          codigo: "ver_usuario",
        },
        {
          id: 3,
          nombre: "Ver Usuario",
          codigo: "ver_usuario",
        },
        {
          id: 4,
          nombre: "Ver Usuario",
          codigo: "ver_usuario",
        },
        {
          id: 5,
          nombre: "Ver Usuario",
          codigo: "ver_usuario",
        },
        {
          id: 6,
          nombre: "Ver Usuario",
          codigo: "ver_usuario",
        },
        {
          id: 7,
          nombre: "Ver Usuario",
          codigo: "ver_usuario",
        },
        {
          id: 8,
          nombre: "Ver Usuario",
          codigo: "ver_usuario",
        },
        {
          id: 9,
          nombre: "Ver Usuario",
          codigo: "ver_usuario",
        },
        {
          id: 10,
          nombre: "Ver Usuario",
          codigo: "ver_usuario",
        },
        {
          id: 11,
          nombre: "Ver Usuario",
          codigo: "ver_usuario",
        },
        {
          id: 12,
          nombre: "Ver Usuario",
          codigo: "ver_usuario",
        },
        {
          id: 13,
          nombre: "Ver Usuario",
          codigo: "ver_usuario",
        },
        {
          id: 14,
          nombre: "Ver Usuario",
          codigo: "ver_usuario",
        },
        {
          id: 15,
          nombre: "Ver Usuario",
          codigo: "ver_usuario",
        },
        {
          id: 16,
          nombre: "Ver Usuario",
          codigo: "ver_usuario",
        },
      ],
    };
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
.acciones a {
  padding-right: 16px;
}
.waves {
  position: absolute;
  bottom: 0;
}
</style>
