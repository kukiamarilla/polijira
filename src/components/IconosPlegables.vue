<template>
  <div :class="tema" :style="{ height: altura }">
    <button class="btn-icon" v-on:click="handleClick">
      <Icon icono="options" color="var(--gray-4)" hover="var(--gray-4)" />
    </button>

    <button class="btn-icon" @click="$emit('clickWatch')">
      <Icon icono="watch" color="var(--gray-4)" hover="var(--info)" />
    </button>

    <button class="btn-icon" @click="$emit('clickDelete')">
      <Icon icono="delete" color="var(--gray-4)" hover="var(--danger)" />
    </button>
  </div>
</template>

<script>
import Icon from "@/components/Icon";

export default {
  data() {
    return {
      active: false,
      iconos: [1, 2],
    };
  },
  computed: {
    tema() {
      return this.active ? "plegable active" : "plegable";
    },
    altura() {
      const height = this.active
        ? (this.iconos.length + 1) * (24 + 8 + 8) + 4 * 2
        : 48;
      return `${height}px`;
    },
  },
  components: {
    Icon,
  },
  methods: {
    handleClick() {
      this.active = !this.active;
    },
  },
};
</script>

<style lang="scss" scoped>
.plegable {
  display: flex;
  border-radius: 24px;
  background-color: white;
  flex-direction: column;
  overflow: hidden;
  transition-property: height, background-color, color;
  transition-timing-function: ease;
  transition-duration: 0.2s;
  z-index: 1;

  .btn-icon {
    background-color: transparent;
    border: none;
    color: var(--gray-4);
    cursor: pointer;
    padding: 8px 12px;

    &:first-child {
      padding-top: 12px;
    }

    &:last-child {
      padding-bottom: 12px;
    }
  }
}

.plegable.active {
  background-color: black;

  .btn-icon {
    color: white;

    &:hover {
      color: var(--info);
    }
  }
}
</style>
