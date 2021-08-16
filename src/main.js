import Vue from 'vue'
import LottieVuePlayer from "@lottiefiles/vue-lottie-player";

import App from '@/App.vue'
import store from '@/store'
import router from '@/router'

import "@/assets/styles/main.css";

Vue.config.productionTip = false

// Vue.use(VueRouter)
Vue.use(LottieVuePlayer);

const vue = new Vue({
  router,
  store,
  render: h => h(App)
})

vue.$mount('#app')
