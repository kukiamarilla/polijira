<template>
  <div>
    <Modal v-model="show" @input="$emit('input', show)">
      <h2>Nuevo Miembro</h2>
      <div class="form-group">
        <label for="usuario" class="highlight">Usuario</label>
        <br /><br />
        <Select v-model="miembro.usuario" :options="usuariosSelect" />
      </div>
      <div class="form-group">
        <label for="rol" class="highlight">Rol</label>
        <br /><br />
        <Select v-model="miembro.rol" :options="rolesSelect" />
      </div>
      <div class="form-group">
        <label for="horario" class="highlight">Horario (en horas)</label>
        <br /><br />
        <div
          class="d-flex"
          style="justify-content: space-between; width: 90%; margin-left: 5%"
        >
          <Counter
            label="Lunes"
            v-model="miembro.horario.lunes"
            style="width: 40px"
            :min="0"
            :max="24"
          />
          <Counter
            label="Martes"
            v-model="miembro.horario.martes"
            style="width: 40px"
            :min="0"
            :max="24"
          />
          <Counter
            label="Miércoles"
            v-model="miembro.horario.miercoles"
            style="width: 40px"
            :min="0"
            :max="24"
          />
          <Counter
            label="Jueves"
            v-model="miembro.horario.jueves"
            style="width: 40px"
            :min="0"
            :max="24"
          />
          <Counter
            label="Viernes"
            v-model="miembro.horario.viernes"
            style="width: 40px"
            :min="0"
            :max="24"
          />
          <Counter
            label="Sábado"
            v-model="miembro.horario.sabado"
            style="width: 40px"
            :min="0"
            :max="24"
          />
          <Counter
            label="Domingo"
            v-model="miembro.horario.domingo"
            style="width: 40px"
            :min="0"
            :max="24"
          />
        </div>
        <div class="d-flex" style="justify-content: flex-end; margin-top: 32px">
          <Boton texto="Guardar" tema="primary" @click="save" />
        </div>
      </div>
    </Modal>
  </div>
</template>

<script>
import Modal from "@/components/Modal";
import Select from "@/components/Select";
import Counter from "@/components/Counter";
import Boton from "@/components/Boton";
import usuarioService from "@/services/usuarioService";
import miembroService from "@/services/miembroService";
import rolProyectoService from "@/services/rolProyectoService";
import Alert from "@/helpers/alert";
import { mapGetters, mapState } from "vuex";

export default {
  components: {
    Modal,
    Select,
    Counter,
    Boton,
  },
  props: ["value"],
  data() {
    return {
      show: false,
      usuarios: [],
      roles: [],
      miembros: [],
      miembro: {
        usuario: -1,
        rol: -1,
        proyecto: 0,
        horario: {
          lunes: 8,
          martes: 8,
          miercoles: 8,
          jueves: 8,
          viernes: 8,
          sabado: 0,
          domingo: 0,
        },
      },
    };
  },
  mounted() {
    this.load();
    this.show = this.value;
  },
  computed: {
    ...mapGetters({
      hasPermission: "auth/hasPermission",
    }),
    ...mapState({
      me: (state) => state.auth.me,
    }),
    usuariosSelect() {
      let usuariosSelect = [];
      this.usuarios
        .filter((usuario) => {
          return !this.miembros
            .map((miembro) => miembro.usuario.id)
            .includes(usuario.id);
        })
        .forEach((usuario) => {
          usuariosSelect[usuario.id] = usuario.nombre;
        });
      return usuariosSelect;
    },
    rolesSelect() {
      let rolesSelect = [];
      this.roles
        .filter((rol) => rol.nombre != "Scrum Master")
        .forEach((rol) => {
          rolesSelect[rol.id] = rol.nombre;
        });
      return rolesSelect;
    },
  },
  watch: {
    value() {
      this.show = this.value;
    },
  },
  methods: {
    load() {
      usuarioService.list().then((usuarios) => {
        this.usuarios = usuarios;
      });
      rolProyectoService.list(this.$route.params["id"]).then((roles) => {
        this.roles = roles;
      });
      miembroService.list(this.$route.params["id"]).then((miembros) => {
        this.miembros = miembros;
      });
      this.miembro = { ...this.miembro, proyecto: this.$route.params["id"] };
    },
    save() {
      miembroService.create(this.miembro).then(() => {
        this.load();
        this.miembro = {
          usuario: -1,
          rol: -1,
          proyecto: 0,
          horario: {
            lunes: 8,
            martes: 8,
            miercoles: 8,
            jueves: 8,
            viernes: 8,
            sabado: 0,
            domingo: 0,
          },
        };
        Alert.success("Usuario agregado al proyecto exitosamente");
      });
      this.show = false;
      this.$emit("input", this.show);
    },
  },
};
</script>

<style>
.form-group {
  margin-top: 24px;
}
</style>