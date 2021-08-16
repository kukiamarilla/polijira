<template>
  <div class="login">
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
  methods: {
    login() {
      authService
        .login()
        .then(() => {
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
</style>
