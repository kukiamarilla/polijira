<template>
  <div>
    <Modal v-model="show" @input="$emit('input', show)">
      <h2>Modificar Miembro</h2>
      <div class="form-group">
        <label for="horario" class="highlight">Horario (en horas)</label>
        <br /><br />
        <div
          class="d-flex"
          style="justify-content: space-between; width: 90%; margin-left: 5%"
        >
          <Counter
            label="Lunes"
            v-model="miembroUpdate.horario.lunes"
            style="width: 40px"
            :min="0"
            :max="24"
          />
          <Counter
            label="Martes"
            v-model="miembroUpdate.horario.martes"
            style="width: 40px"
            :min="0"
            :max="24"
          />
          <Counter
            label="Miércoles"
            v-model="miembroUpdate.horario.miercoles"
            style="width: 40px"
            :min="0"
            :max="24"
          />
          <Counter
            label="Jueves"
            v-model="miembroUpdate.horario.jueves"
            style="width: 40px"
            :min="0"
            :max="24"
          />
          <Counter
            label="Viernes"
            v-model="miembroUpdate.horario.viernes"
            style="width: 40px"
            :min="0"
            :max="24"
          />
          <Counter
            label="Sábado"
            v-model="miembroUpdate.horario.sabado"
            style="width: 40px"
            :min="0"
            :max="24"
          />
          <Counter
            label="Domingo"
            v-model="miembroUpdate.horario.domingo"
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
    Counter,
    Boton,
  },
  props: ["value", "miembro"],
  data() {
    return {
      show: false,
      usuarios: [],
      roles: [],
      miembros: [],
      miembroUpdate: {
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
      this.miembroUpdate = { ...this.miembro };
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
    },
    save() {
      miembroService
        .modificarHorario(
          this.miembroUpdate.horario.id,
          this.miembroUpdate.horario
        )
        .then(() => {
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
          Alert.success("Horario modificado exitosamente");
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