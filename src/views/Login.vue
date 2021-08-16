<template>
  <div class="login">
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

export default {
  components: {
    MenuSemiCirculoDerecho,
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
          console.log(errorCode);
          alert(errorCode);

          var errorMessage = error.message;
          console.log(errorMessage);
          alert(errorMessage);
        });
    },
  },
};
</script>

<style scoped>
.login {
  height: 100vh;
  min-height: 550px;
  width: 100%;
}

.mitad-izquierda {
  width: 40vw;
  margin-left: 100px;
  margin-top: 50px;
}
</style>
