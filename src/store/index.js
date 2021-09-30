import Vue from "vue";
import Vuex from "vuex";

import auth from "@/store/auth";
import alert from "@/store/alert";
import proyecto from "@/store/proyecto";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    auth,
    alert,
    proyecto
  },
});
