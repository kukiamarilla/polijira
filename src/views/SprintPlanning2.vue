<template>
  <div>
    <Navbar />

    <div class="d-flex">
      <SidebarProyecto current="miembros" :proyecto="proyecto" />
      <div class="container shadow">
        <div class="header">
          <h2>Spring Planning</h2>
          <br />
          <h4>Paso 2: Sprint Backlog</h4>
          <br /><br /><br />
        </div>
        <Table height="400px">
          <TableHeader>
            <Th width="5%">ID</Th>
            <Th width="25%">Título</Th>
            <Th width="25%">Descripción</Th>
            <Th width="15%">Prioridad</Th>
            <Th width="15%">Acciones</Th>
            <Th width="15%">Incluir</Th>
          </TableHeader>
          <TableBody>
            <Tr v-for="us in productBacklog" :key="us.id">
              <Td width="5%">{{ us.id }}</Td>
              <Td width="25%">{{ us.titulo }}</Td>
              <Td width="25%">{{ us.descripcion }}</Td>
              <Td width="15%">{{ us.prioridad }}</Td>
              <Td width="15%">{{ "[Acciones]" }}</Td>
              <Td width="15%">
                <Checkbox v-model="us.included" @input="verPlanificacion(us)" />
              </Td>
            </Tr>
          </TableBody>
        </Table>
        <div class="d-flex justify-content-space-between align-items-center">
          <div>
            <span class="highlight">Capacidad del sprint:</span>
            {{ capacidadesDeMiembros }} / {{ weightedMembers }} /
            {{ horasAsignadasDeMiembros }} / {{ totalAsignado }} /
            {{ capacidadTotal }}
          </div>
          <div>
            <Boton
              class="mr-2"
              texto="Anterior"
              @click="anterior"
              tema="primary"
            />

            <Boton texto="Siguiente" @click="siguiente" tema="primary" />
          </div>
        </div>
      </div>
    </div>

    <Modal v-model="agregarUSModal" width="496px">
      <h1>Planificar User Story</h1>
      <br /><br />

      <label class="highlight">Título</label>
      <p>{{ userStory.nombre }}</p>

      <InputNumber
        title="Estimación en horas:"
        v-model="userStory.estimacion"
        :min="0"
      />

      <label class="highlight">Asignar a:</label>
      <WeightedSelect
        :options="weightedMembers"
        v-model="miembroSelecto"
        @input="asignarMiembro()"
      />

      <div class="d-flex justify-content-flex-end">
        <Boton texto="Guardar" tema="primary" @click="planificarUS" />
      </div>
    </Modal>
  </div>
</template>

<script>
import Navbar from "@/components/Navbar";
import SidebarProyecto from "@/components/SidebarProyecto";
import { Table, TableHeader, TableBody, Th, Tr, Td } from "@/components/Table";
import sprintService from "@/services/sprintService";
import proyectoService from "@/services/proyectoService";
import miembroService from "@/services/miembroService";
import Alert from "@/helpers/alert";
import { mapGetters, mapState } from "vuex";
import Checkbox from "@/components/Checkbox";
import InputNumber from "@/components/InputNumber";
import Boton from "@/components/Boton";
import Modal from "@/components/Modal";
import WeightedSelect from "@/components/WeightedSelect";

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
    InputNumber,
    Boton,
    Modal,
    WeightedSelect,
  },
  created() {},
  mounted() {
    this.load();
    localStorage.setItem("spring-planning-paso", 2);
  },
  computed: {
    capacidadesDeMiembros() {
      const capacidades = {};

      this.miembrosSprint.forEach((miembro) => {
        capacidades[miembro.id] = this.capacidadPorMiembro(miembro);
      });

      return capacidades;
    },
    weightedMembers() {
      return this.miembrosSprint.map((miembro) => ({
        text: miembro.nombre,
        currWeight: this.horasAsignadasDeMiembros[miembro.id],
        totalWeight: this.capacidadesDeMiembros[miembro.id],
      }));
    },
    horasAsignadasDeMiembros() {
      const horasAsignadas = {};

      this.miembrosSprint.forEach((miembro) => {
        let asignado = 0;

        this.userStoriesIncluidos.forEach((us) => {
          if (us.miembroAsignado === miembro) {
            asignado += us.estimacion;
          }
        });

        horasAsignadas[miembro.id] = asignado;
      });

      return horasAsignadas;
    },
    totalAsignado() {
      let sumaAsignadas = 0;

      for (let miembro in this.horasAsignadasDeMiembros) {
        sumaAsignadas += this.horasAsignadasDeMiembros[miembro];
      }

      return sumaAsignadas;
    },
    capacidadTotal() {
      let capacidad = 0;
      this.miembrosSprint.forEach((miembro) => {
        capacidad += this.capacidadesDeMiembros[miembro.id];
      });
      return capacidad;
    },
    userStoriesIncluidos() {
      return this.productBacklog.filter((us) => us.included);
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
        fecha_inicio: undefined,
        fecha_fin: undefined,
      },
      miembrosSprint: [],
      miembroSprint: {
        nombre: "",
        horario: {
          domingo: 0,
          lunes: 0,
          martes: 0,
          miercoles: 0,
          jueves: 0,
          viernes: 0,
          sabado: 0,
        },
      },
      productBacklog: [
        {
          id: 1,
          titulo: "us1",
          descripcion: "descri",
          estimacion: 0,
          prioridad: 2,
          miembroAsignado: {},
          included: false,
        },
        {
          id: 2,
          titulo: "us2",
          descripcion: "perlus",
          estimacion: 0,
          prioridad: 3,
          miembroAsignado: {},
          included: false,
        },
        {
          id: 3,
          titulo: "us3",
          descripcion: "lusca",
          estimacion: 0,
          prioridad: 1,
          miembroAsignado: {},
          included: false,
        },
      ],
      userStory: {
        id: "",
        titulo: "",
        descripcion: "",
        estimacion: 0,
        prioridad: 0,
        miembroAsignado: {},
        included: false,
      },
      miembroSelecto: -1,
      agregarUSModal: false,
    };
  },
  methods: {
    async load() {
      const paso = localStorage.getItem("sprint-planning");
      const idProyecto = this.$route.params["id"];
      const idSprint = this.$route.params["idSprint"];
      proyectoService.retrieve(idProyecto).then((proyecto) => {
        this.proyecto = proyecto;
      });
      let miembrosProyecto;
      await miembroService.list(idProyecto).then((miembros) => {
        miembrosProyecto = miembros;
      });
      sprintService.retrieve(idSprint).then((sprint) => {
        this.sprint = sprint;
        if (!sprint.planificador) this.$router.back();
        if (sprint.planificador != this.meProyecto.id) this.$router.back();
        if (![null, 2].includes(paso))
          this.$router.push(
            `/proyectos/${idProyecto}/sprint-planning/${idSprint}/paso-${paso}`
          );
      });
      sprintService.miembros(idSprint).then((miembrosSprint) => {
        this.miembrosSprint = miembrosSprint.map((ms) => {
          const mp = miembrosProyecto.find((m) => m.id === ms.miembro_proyecto);
          return { ...ms, nombre: mp.usuario.nombre, horario: mp.horario };
        });
      });
    },
    verPlanificacion(userStory) {
      if (userStory.included) {
        this.userStory = userStory;
        this.agregarUSModal = true;
      }
    },
    planificarUS() {},
    asignarMiembro() {
      this.userStory.miembroAsignado = this.miembrosSprint[this.miembroSelecto];
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
    anterior() {
      this.$router.push(
        `/proyectos/${this.$route.params["id"]}/sprint-planning/${this.$route.params["idSprint"]}/paso-1`
      );
    },
    siguiente() {
      this.$router.push(
        `/proyectos/${this.$route.params["id"]}/sprint-planning/${this.$route.params["idSprint"]}/paso-3`
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
