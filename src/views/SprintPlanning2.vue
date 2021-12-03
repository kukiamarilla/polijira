<template>
  <div>
    <Navbar />

    <div class="d-flex">
      <SidebarProyecto current="miembros" :proyecto="proyecto" />
      <div class="container shadow">
        <div class="header">
          <h2>Sprint Planning</h2>
          <br />
          <h4>Paso 2: Sprint Backlog</h4>
          <br /><br /><br />
        </div>
        <Table height="400px">
          <TableHeader>
            <Th width="5%">ID</Th>
            <Th width="25%">Nombre</Th>
            <Th width="25%">Descripción</Th>
            <Th width="15%">Prioridad</Th>
            <Th width="15%">Acciones</Th>
            <Th width="15%">Incluir</Th>
          </TableHeader>
          <TableBody>
            <Tr v-for="us in sprintBacklog" :key="us.user_story.id">
              <Td width="5%">{{ us.user_story.id }}</Td>
              <Td width="25%">{{ us.user_story.nombre }}</Td>
              <Td width="25%">{{ us.user_story.descripcion }}</Td>
              <Td width="15%">{{ us.user_story.prioridad }}</Td>
              <Td width="15%">
                <a
                    href="#"
                    @click.prevent="verUserStory(us.user_story)"
                  >
                    <Icon
                      icono="watch"
                      size="16px"
                      color="#bdbdbd"
                      hover="var(--primary)"
                    />
                  </a>
              </Td>
              <Td width="15%">
                <Checkbox v-model="us.included" @input="eliminarUS(us)" />
              </Td>
            </Tr>

            <Tr v-for="us in productBacklog" :key="us.id">
              <Td width="5%">{{ us.user_story.id }}</Td>
              <Td width="25%">{{ us.user_story.nombre }}</Td>
              <Td width="25%">{{ us.user_story.descripcion }}</Td>
              <Td width="15%">{{ us.user_story.prioridad }}</Td>
              <Td width="15%">
                <a
                    href="#"
                    @click.prevent="verUserStory(us.user_story)"
                  >
                    <Icon
                      icono="watch"
                      size="16px"
                      color="#bdbdbd"
                      hover="var(--primary)"
                    />
                  </a>
              </Td>
              <Td width="15%">
                <Checkbox v-model="us.included" @input="verPlanificacion(us)" />
              </Td>
            </Tr>
          </TableBody>
        </Table>
        <div class="d-flex justify-content-space-between align-items-center">
          <span>
            <span class="highlight">Capacidad del sprint:</span>
            {{ totalAsignado }} / {{ capacidadTotal }}
          </span>

          <Boton texto="Siguiente" @click="siguiente" tema="primary" />
        </div>
      </div>
    </div>

    <Modal v-model="verUSPlanning" @input="deshacerPlanUS" width="496px">
      <h1>Planificar User Story</h1>
      <br /><br />

      <label class="highlight">Título</label>
      <p>{{ userStory.user_story.nombre }}</p>

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
        <Boton texto="Guardar" tema="primary" @click="planificarUS" :disabled="loading"/>
      </div>
    </Modal>
    <UserStory v-model="verUserStorySelected" :userStory="verUserStorySelected"/>
  </div>
</template>

<script>
import Navbar from "@/components/Navbar";
import SidebarProyecto from "@/components/SidebarProyecto";
import { Table, TableHeader, TableBody, Th, Tr, Td } from "@/components/Table";
import sprintService from "@/services/sprintService";
import proyectoService from "@/services/proyectoService";
import Alert from "@/helpers/alert";
import { mapGetters, mapState } from "vuex";
import Checkbox from "@/components/Checkbox";
import InputNumber from "@/components/InputNumber";
import Boton from "@/components/Boton";
import Modal from "@/components/Modal";
import WeightedSelect from "@/components/WeightedSelect";
import UserStory from "@/components/UserStory";
import Icon from "@/components/Icon";

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
    Icon,
    WeightedSelect,
    UserStory
  },
  created() { 
  },
  mounted() {
    this.load();
  },
  computed: {
    capacidadesDeMiembros() {
      const capacidades = {};

      this.miembrosSprint.forEach((miembro) => {
        capacidades[miembro.id] = this.capacidadPorMiembro(miembro.miembro_proyecto);
      });

      return capacidades;
    },
    weightedMembers() {
      return this.miembrosSprint.map((miembro, idx) => {
        
        let horasAsignadas = this.sprintBacklog.filter(us => us.desarrollador.id === miembro.id).reduce((acc, us) => acc + us.horas_estimadas, 0);
        horasAsignadas += this.userStory.estimacion && this.miembroSelecto === idx ? this.userStory.estimacion : 0;

        return {
          text: miembro.nombre,
          currWeight: horasAsignadas,
          totalWeight: this.capacidadPorMiembro(miembro.miembro_proyecto),
        }
      });
    },
    horasAsignadasDeMiembros() {
      const usPlanning = this.productBacklog.filter((us) => us.included);
      const todosLosUS = [...usPlanning, ...this.sprintBacklog];

      const horasAsignadas = {};

      this.miembrosSprint.forEach((miembro) => {
        let asignado = 0;

        todosLosUS.forEach((us) => {
          if (us.desarrollador === miembro) {
            asignado += us.estimacion;
          }
        });

        horasAsignadas[miembro.id] = asignado;
      });

      return horasAsignadas;
    },
    totalAsignado() {
      let sumaAsignadas = 0;

      this.sprintBacklog.forEach((us) => {
        sumaAsignadas += us.horas_estimadas;
      });

      return sumaAsignadas;
    },
    capacidadTotal() {
      let capacidad = 0;
      this.miembrosSprint.forEach((miembro) => {
        capacidad += this.capacidadesDeMiembros[miembro.id];
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
      loading: false,
      proyecto: {
        nombre: "",
      },
      sprint: {
        planificador: 0,
        fecha_inicio: undefined,
        fecha_fin: undefined,
      },
      miembrosSprint: [],
      sprintBacklog: [],
      productBacklog: [],
      userStory: {
        id: "",
        user_story: {
          nombre: "",
          descripcion: "",
          prioridad: 0,
        },
        estimacion: 0,
        desarrollador: {},
        included: false,
      },
      miembroSelecto: -1,
      verUSPlanning: false,
      verUserStoryShow: true,
      verUserStorySelected: {
        nombre: "",
        descripcion: "",
        prioridad: 0,
      },
    };
  },
  methods: {
    load() {
      const idProyecto = this.$route.params["id"];
      const idSprint = this.$route.params["idSprint"];

      // cargamos el proyecto
      proyectoService.retrieve(idProyecto).then((proyecto) => {
        this.proyecto = proyecto;
      });


      // cargamos el sprint
      sprintService.retrieve(idSprint).then((sprint) => {
        this.sprint = sprint;
        if (!sprint.estado_planificacion == "I") this.$router.back();
        if (sprint.planificador != this.meProyecto.id) this.$router.back();
        const paso = localStorage.getItem("sprint-planning-paso");
        if(!paso) {
          this.$router.push(
            `/proyectos/${idProyecto}/sprint-planning/${idSprint}/paso-1`
          );
          return
        }
        if (!["1", "2"].includes(paso)){
          this.$router.push(
            `/proyectos/${idProyecto}/sprint-planning/${idSprint}/paso-${paso}`
          );
          return
        }
        localStorage.setItem("sprint-planning-paso", 2);
      });


      // cargamos el sprint backlog
      sprintService.sprintBacklog(idSprint).then((sprintBacklog) => {
        this.sprintBacklog = sprintBacklog.map((us) => ({
          ...us,
          included: true,
        }));
        // cargamos miembros del sprint
        sprintService.miembros(idSprint).then((miembrosSprint) => {
          this.miembrosSprint = miembrosSprint.map((ms) => {
            return { ...ms, nombre: ms.miembro_proyecto.usuario.nombre, horario: ms.miembro_proyecto.horario,  };
          });
        });
      });

      // cargamos el product backlog
      proyectoService.backlog(idProyecto).then((productBacklog) => {
        this.productBacklog = productBacklog.map((us) => ({
          ...us,
          included: false,
          desarrollador: null,
        }));
      });
    },
    verPlanificacion(userStory) {
      this.userStory = userStory;
      this.verUSPlanning = true;
    },
    planificarUS() {
      const payload = {
        user_story: this.userStory.user_story.id,
        horas_estimadas: this.userStory.estimacion,
        desarrollador: this.userStory.desarrollador.id,
      };
      this.loading = true;
      sprintService.agregarUserStory(this.sprint.id, payload).then(() => {
        this.loading = false;
        this.verUSPlanning = false;
        this.load();
        Alert.success("Se ha agregado el user story al sprint backlog");
      });
    },
    eliminarUS(userStory) {
      sprintService
        .eliminarUserStory(this.sprint.id, {
          sprint_backlog: userStory.id,
        })
        .then(() => {
          userStory.included = false;
          this.load();
          Alert.success("Se ha eliminado el user story del sprint backlog");
        });
    },
    asignarMiembro() {
      this.userStory.desarrollador = this.miembrosSprint[this.miembroSelecto];
    },
    deshacerPlanUS() {
      this.userStory.included = false;
      this.userStory.estimacion = 0;
      this.userStory.desarrollador = null;
      this.miembroSelecto = -1;
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
    siguiente() {
      this.$router.push(
        `/proyectos/${this.$route.params["id"]}/sprint-planning/${this.$route.params["idSprint"]}/paso-3`
      );
    },
    verUserStory(userStory) {
      this.verUserStoryShow = true,
      this.verUserStorySelected = userStory
    }
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
