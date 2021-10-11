<template>
  <div>
    <label class="highlight">{{ title }}</label>

    <DatePicker
      class="datepicker"
      v-model="text"
      format="DD/MM/YYYY"
      type="date"
      placeholder="Seleccionar fecha"
      @input="$emit('input', (new Date(text)).toISOString().substr(0,10))"
      :disabled="disabled"
    ></DatePicker>
  </div>
</template>

<script>
import DatePicker from "vue2-datepicker";
import "vue2-datepicker/index.css";
import "vue2-datepicker/locale/es";

export default {
  components: {
    DatePicker,
  },
  props: ["title", "value", "disabled"],
  data() {
    return {
      text: new Date(this.value),
    };
  },
  watch: {
    value() {
      this.text = new Date(this.value);
    },
  },
};
</script>

<style lang="scss" scoped>
.datepicker {
  border-radius: 5px;
  margin: 16px 0 32px 0;
  width: 100%;
}
</style>
