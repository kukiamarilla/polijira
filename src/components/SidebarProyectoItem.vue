<template>
  <div :class="{ item: true, active }" @click="$router.push(to)">
    <div class="normal-item">
      <div class="reference">
        <router-link :to="to" style="text-decoration: none">
          <div class="d-flex">
            <Icon :icono="icono" color="#fff" size="18px" />
            <h6>{{ texto }}</h6>
          </div>
        </router-link>
      </div>
    </div>
    <div class="active-item">
      <div class="reference">
        <div class="top-bg"></div>
        <div class="top-ol"></div>
        <div class="bottom-bg"></div>
        <div class="bottom-ol"></div>
        <router-link :to="to" style="text-decoration: none">
          <div class="d-flex">
            <Icon :icono="icono" color="var(--primary-dark)" size="18px" />
            <h6>{{ texto }}</h6>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import Icon from "@/components/Icon";
export default {
  components: { Icon },
  props: ["icono", "texto", "to", "active"],
};
</script>

<style lang="scss" scoped>
.item {
  position: relative;
  height: 80px;
  cursor: pointer;
  &.active .active-item {
    clip-path: inset(-16px 0px -16px 0px);
  }
  &:hover .active-item {
    clip-path: inset(-16px 0px -16px 0px);
  }
  .normal-item {
    width: calc(100% - 16px);
    position: absolute;
    top: 0;
    padding: 16px 0;
    margin-left: 16px;
    margin-top: 16px;
    .reference {
      text-decoration: none;
      .d-flex {
        display: flex;
        flex-direction: row;
        margin-left: 40px;
        h6 {
          color: #fff;
          padding-left: 16px;
        }
      }
    }
  }
  .active-item {
    width: calc(100% - 16px);
    position: absolute;
    top: 0;
    background-color: #fff;
    padding: 16px 0;
    margin-left: 16px;
    margin-top: 16px;
    border-top-left-radius: 26px;
    border-bottom-left-radius: 26px;
    transition: clip-path 0.4s ease-out;
    clip-path: inset(-16px 0px -16px 100%);
    .reference {
      text-decoration: none;
      position: relative;
      .top-bg {
        background-color: #fff;
        width: 100%;
        position: absolute;
        height: 16px;
        top: -32px;
      }
      .top-ol {
        background-color: var(--primary-dark);
        width: 100%;
        position: absolute;
        height: 16px;
        top: -32px;
        border-bottom-right-radius: 16px;
      }
      .bottom-bg {
        background-color: #fff;
        width: 100%;
        position: absolute;
        height: 16px;
        bottom: -32px;
      }
      .bottom-ol {
        background-color: var(--primary-dark);
        width: 100%;
        position: absolute;
        height: 16px;
        bottom: -32px;
        border-top-right-radius: 16px;
      }
      .d-flex {
        display: flex;
        flex-direction: row;
        margin-left: 40px;
        h6 {
          color: var(--primary-dark);
          padding-left: 16px;
        }
      }
    }
  }
}
</style>