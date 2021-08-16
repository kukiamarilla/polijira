import Vue from 'vue'
import LottieVuePlayer from "@lottiefiles/vue-lottie-player";
import * as firebase from "firebase";

import App from '@/App.vue'
import store from '@/store'
import router from '@/router'

import "@/assets/styles/main.css";

Vue.config.productionTip = false

// Vue.use(VueRouter)
Vue.use(LottieVuePlayer);

var firebaseConfig = {
  apiKey: process.env.VUE_APP_FIREBASE_API_KEY,
  authDomain: process.env.VUE_APP_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.VUE_APP_FIREBASE_PROJECT_ID,
  storageBucket: process.env.VUE_APP_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.VUE_APP_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.VUE_APP_FIREBASE_APP_ID
};

firebase.initializeApp(firebaseConfig);

const vue = new Vue({
  router,
  store,
  render: h => h(App)
})

vue.$mount('#app')
