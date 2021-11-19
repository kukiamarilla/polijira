<template>
  <div :class="{ select: true, disabled: disabled }" v-click-outside="hide">
    <span class="text" @click="show" v-if="value != -1">
      {{ selected.text }}
      <span :class="{ alert: selectedTooHeavy }">
        {{ selected.currWeight }}/{{ selected.totalWeight }}
      </span>
      &nbsp;
      <span class="caret" v-if="!disabled"></span>
    </span>
    <span class="text" @click="show" v-else>
      Seleccione un valor &nbsp; <span class="caret" v-if="!disabled"></span>
    </span>
    <div class="options" v-if="active">
      <div
        :class="{ option: true, active: value == idx }"
        v-for="(option, idx) in options"
        :key="idx"
        @click="select(idx)"
      >
        <span class="highlight">
          {{ option.text }}
          <span :class="{ alert: isTooHeavy(idx) }">
            {{ option.currWeight }}/{{ option.totalWeight }}
          </span>
        </span>
        <div class="icon" v-if="value == idx">
          <Icon icono="check" size="12px" color="var(--primary)" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Icon from "@/components/Icon";
import ClickOutside from "vue-click-outside";

export default {
  components: { Icon },
  props: ["options", "value", "disabled"],
  computed: {
    selected() {
      return this.options[this.value];
    },
    selectedTooHeavy() {
      const remainingWeight =
        this.selected.totalWeight - this.selected.currWeight;

      return remainingWeight < 0;
    },
  },
  data() {
    return {
      active: false,
    };
  },
  methods: {
    hide() {
      if (this.active) this.active = false;
    },
    show() {
      if (!this.disabled) this.active = true;
    },
    select(idx) {
      this.active = false;
      this.$emit("input", idx);
    },
    isTooHeavy(idx) {
      const option = this.options[idx];
      const remainingWeight = option.totalWeight - option.currWeight;

      return remainingWeight < 0;
    },
  },
  directives: {
    ClickOutside,
  },
};
</script>

<style scoped lang="scss">
.select {
  position: relative;
  &:not(.disabled) {
    span.text {
      cursor: pointer;
    }
  }
  .options {
    padding: 16px;
    position: absolute;
    top: 0;
    left: 0;
    display: flex;
    flex-direction: column;
    background-color: #fff;
    box-shadow: 4px 0 15px rgba(0, 0, 0, 0.25);
    border-radius: 10px;
    z-index: 1;
    .option {
      cursor: pointer;
      padding: 8px 0;
      display: flex;
      flex-direction: row;
      justify-content: space-between;
      &:hover,
      &.active {
        color: var(--primary);
      }
      span {
        padding-right: 16px;
      }
      .icon {
        padding-top: 2px;
      }
    }
  }
}

span.caret {
  width: 6px;
  height: 6px;
  display: inline-block;
  transform: rotate(45deg) translateY(-3px);
  border-bottom: 3px var(--gray-4) solid;
  border-right: 3px var(--gray-4) solid;
  border-top: 3px transparent solid;
  border-left: 3px transparent solid;
}

.alert {
  color: var(--danger);
}
</style>
