<template>
  <div>
    <label class="highlight">{{ title }}</label>

    <DatePicker
      class="datepicker"
      v-model="text"
      format="DD/MM/YYYY"
      type="date"
      placeholder="Seleccionar fecha"
      @input="$emit('input', text)"
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
  props: ["title", "value"],
  data() {
    return {
      text: this.value,
    };
  },
  watch: {
    value() {
      this.text = this.value;
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
