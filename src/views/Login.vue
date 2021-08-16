<template>
  <div class="login">
    <MenuSemiCirculoDerecho
      frase="Accedé Ahora"
      botonTexto="Iniciar Sesión"
      color="var(--primary)"
    />
  </div>
</template>

<script>
import MenuSemiCirculoDerecho from "@/components/MenuSemiCirculoDerecho";
export default {
  components: {
    MenuSemiCirculoDerecho,
  },
};
</script>

<style scoped>
.login {
  height: 100vh;
  min-height: 550px;
  position: relative;
  width: 100%;
}
</style>
