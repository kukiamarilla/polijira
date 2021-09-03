import api from "../services/api";
import usuarioService from "@/services/usuarioService";
import store from "@/store";

export default function auth({ router, next }) {
  var session = localStorage.getItem("session");
  if (session == null) {
    return router.push({ name: "Login" });
  }
  session = JSON.parse(session);
  api.defaults.headers.common["Authorization"] = "JWT " + session.token;
  usuarioService.me().then(response => {
    store.commit('auth/me', response)
    next();
  }).catch(err => {
    if(err.response && err.response.data.error == "unauthenticated") {
      localStorage.removeItem("session");
      router.push({name: "Login"});
    }
    next()
  });
}
