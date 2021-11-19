<template>
  <div>
    <Navbar />
    <div class="mitad-izquierda">
      <div>
        <h2>
          Gestiona todos tus proyectos.<br />
          Mas fácil. Mas rápido.
        </h2>

        <lottie-vue-player
          src="https://assets2.lottiefiles.com/packages/lf20_0tue65cn.json"
          :theme="options.theme"
          :player-size="options.playerSize"
          :player-controls="false"
          style="width: 100%; height: auto"
        />
      </div>
    </div>

    <MenuSemiCirculoDerecho
      frase="Accedé Ahora"
      botonTexto="Iniciar Sesión"
      color="var(--primary)"
      @login="login"
    />
  </div>
</template>

<script>
import MenuSemiCirculoDerecho from "@/components/MenuSemiCirculoDerecho";
import authService from "@/services/authService";
import Navbar from "@/components/Navbar";

export default {
  components: {
    MenuSemiCirculoDerecho,
    Navbar,
  },
  data() {
    return {
      options: {
        minimizable: false,
        playerSize: "standard",
        backgroundColor: "#fff",
        backgroundStyle: "color",
        theme: {
          controlsView: "standard",
          active: "light",
          light: {
            color: "#3D4852",
            backgroundColor: "#fff",
            opacity: "0.7",
          },
          dark: {
            color: "#fff",
            backgroundColor: "#202020",
            opacity: "0.7",
          },
        },
      },
    };
  },
  methods: {
    login() {
      authService
        .login()
        .then(() => {
          this.$store.commit("auth/login");
          this.$router.push({ name: "No Activado" });
        })
        .catch(function (error) {
          // Handle Errors here.
          var errorCode = error.code;
          alert(errorCode);

          var errorMessage = error.message;
          alert(errorMessage);
        });
    },
  },
};
</script>

<style scoped>
.mitad-izquierda {
  padding-left: 100px;
  padding-top: 50px;
  width: 40vw;
}
</style>
