<template>
  <div style="width: calc(100% - 380px)">
    <div class="box shadow">
      <h2 class="title">Product Backlog</h2>
      <div class="backlog">
        <h2 class="empty-message">
          Aun no hay User Stories en el Product Backlog.
          <a href="#">Agregar uno</a>
        </h2>
      </div>
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style lang="scss" scoped>
.box {
  background-color: white;
  border-radius: 20px;
  min-height: 300px;
  margin: 0 40px;
  padding: 40px;
}
.backlog {
  height: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.empty-message {
  width: 600px;
  text-align: center;
  color: var(--gray-4);
  a {
    text-decoration: none;
    color: var(--primary-light);
    &:hover {
      color: var(--primary);
    }
  }
}
</style>