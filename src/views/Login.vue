<template>
  <div class="login">
    <div class="mitad-izquierda">
      <ImagenConTitulo
        titulo="Gestiona todos tus proyectos. Mas fácil. Mas rápido."
      />
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
import ImagenConTitulo from "@/components/ImagenConTitulo";
import MenuSemiCirculoDerecho from "@/components/MenuSemiCirculoDerecho";
export default {
  components: {
    ImagenConTitulo,
    MenuSemiCirculoDerecho,
  },
  methods: {
    login() {},
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
  align-items: flex-end;
  display: flex;
  flex-direction: column;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 50%;
}
</style>
