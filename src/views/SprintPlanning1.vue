<template>
  <div>
    <Navbar />
    <div class="d-flex">
      <SidebarProyecto current="miembros" :proyecto="proyecto" />
      <div class="container shadow">
        <div class="header">
          <h2>Spring Planning</h2>
          <br />
          <h4>Paso 1: Elegir miembros de Sprint</h4>
          <br /><br /><br />
        </div>
        <Table height="400px">
          <TableHeader>
            <Th width="20%">ID</Th>
            <Th width="20%">Nombre</Th>
            <Th width="20%">Email</Th>
            <Th width="20%">Rol</Th>
            <Th width="20%">Incluir</Th>
          </TableHeader>
          <TableBody>
            <Tr v-for="(miembro, idx) in miembros" :key="idx">
              <Td width="20%">{{ miembro.usuario.id }}</Td>
              <Td width="20%">{{ miembro.usuario.nombre }}</Td>
              <Td width="20%">{{ miembro.usuario.email }}</Td>
              <Td width="20%">
                {{ miembro.rol.nombre }}
              </Td>
              <Td width="20%">
                <Checkbox
                  v-model="miembro.included"
                  @input="
                    miembro.included
                      ? agregarMiembro(miembro)
                      : eliminarMiembro(miembro)
                  "
                />
              </Td>
            </Tr>
          </TableBody>
        </Table>
        <div class="d-flex justify-content-space-between align-items-center">
          <div>
            <span class="highlight">Capacidad del sprint:</span>
            {{ capacidad }} hs.
          </div>
          <Boton texto="Siguiente" @click="siguiente" tema="primary" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from "@/components/Navbar";
import SidebarProyecto from "@/components/SidebarProyecto";
import { Table, TableHeader, TableBody, Th, Tr, Td } from "@/components/Table";
import miembroService from "@/services/miembroService";
import sprintService from "@/services/sprintService";
import proyectoService from "@/services/proyectoService";
import Alert from "@/helpers/alert";
import { mapGetters, mapState } from "vuex";
import Checkbox from "@/components/Checkbox";
import Boton from "@/components/Boton";

export default {
  components: {
    Navbar,
    SidebarProyecto,
    Table,
    TableHeader,
    TableBody,
    Th,
    Tr,
    Td,
    Checkbox,
    Boton,
  },
  created() {},
  mounted() {
    this.load();
    localStorage.setItem("spring-planning-paso", 1);
  },
  computed: {
    capacidad() {
      let capacidad = 0;
      this.miembrosSprint.forEach((ms) => {
        capacidad += this.capacidadPorMiembro(
          this.miembros.find((miembro) => miembro.id == ms.miembro_proyecto)
        );
      });
      return capacidad;
    },
    ...mapGetters({
      hasPermission: "auth/hasPermission",
      hasPermissions: "auth/hasPermissions",
      hasAnyPermission: "auth/hasAnyPermission",
      hasProyectoPermission: "proyecto/hasPermission",
      hasProyectoPermissions: "proyecto/hasPermissions",
      hasProyectoAnyPermission: "proyecto/hasAnyPermission",
    }),
    ...mapState({
      me: (state) => state.auth.me,
      meProyecto: (state) => state.proyecto.me,
    }),
  },
  data() {
    return {
      proyecto: {
        nombre: "",
      },
      sprint: {
        planificador: 0,
      },
      miembros: [],
      miembrosSprint: [],
      miembro: {
        horario: {
          id: 0,
          lunes: 0,
          martes: 0,
          miercoles: 0,
          jueves: 0,
          viernes: 0,
          sabado: 0,
          domingo: 0,
        },
      },
      agregarMiembroModal: false,
      modificarMiembroModal: false,
    };
  },
  methods: {
    load() {
      const paso = localStorage.getItem("sprint-planning");
      const idProyecto = this.$route.params["id"];
      const idSprint = this.$route.params["idSprint"];
      proyectoService.retrieve(idProyecto).then((proyecto) => {
        this.proyecto = proyecto;
      });
      sprintService.retrieve(idSprint).then((sprint) => {
        this.sprint = sprint;
        if (!sprint.planificador) this.$router.back();
        if (sprint.planificador != this.meProyecto.id) this.$router.back();
        if (![null, 1].includes(paso))
          this.$router.push(
            `/proyecto/${idProyecto}/sprint-planning/${idSprint}/paso-${paso}`
          );
      });
      sprintService.miembros(idSprint).then((miembrosSprint) => {
        this.miembrosSprint = miembrosSprint;
        miembroService.list(idProyecto).then((miembros) => {
          miembros = miembros.map((miembro) => ({
            ...miembro,
            included: miembrosSprint
              .map((x) => x.miembro_proyecto)
              .includes(miembro.id),
          }));
          this.miembros = miembros;
        });
      });
    },
    agregarMiembro(miembro) {
      sprintService
        .agregarMiembro(this.sprint.id, { miembro: miembro.id })
        .then(() => {
          this.load();
          Alert.success("Se ha agregado el miembro al sprint");
        });
    },
    eliminarMiembro(miembro) {
      miembro = this.miembrosSprint.find(
        (ms) => ms.miembro_proyecto == miembro.id
      );
      sprintService
        .eliminarMiembro(this.sprint.id, { miembro_sprint: miembro.id })
        .then(() => {
          this.load();
          Alert.success("Se ha eliminado el miembro");
        });
    },
    horarioToArray(horario) {
      return [
        horario.domingo,
        horario.lunes,
        horario.martes,
        horario.miercoles,
        horario.jueves,
        horario.viernes,
        horario.sabado,
      ];
    },
    capacidadPorMiembro(miembro) {
      const ini = new Date(this.sprint.fecha_inicio).getTime();
      const fin = new Date(this.sprint.fecha_fin).getTime();
      let capacidad = 0;
      let horario = this.horarioToArray(miembro.horario);
      for (let curr = ini; curr <= fin; curr += 1000 * 60 * 60 * 24) {
        capacidad += horario[new Date(curr).getDay()];
      }
      return capacidad;
    },
    siguiente() {
      this.$router.push(
        `/proyectos/${this.$route.params["id"]}/sprint-planning/${this.$route.params["idSprint"]}/paso-2`
      );
    },
  },
};
</script>

<style lang="scss" scoped>
.container {
  background-color: white;
  border-radius: 20px;
  height: var(--absolute-remaining-height);
  min-height: 300px;
  padding: 40px;
  margin: 0 40px 40px 40px;
  right: 88px;
  width: calc(100% - 380px);
}

.d-flex.header {
  margin-bottom: 58px;
  justify-content: space-between;
}
.acciones a {
  margin-left: 16px;
}
</style>
