import api from "../services/api";

export default function guest({ router, next }) {
  var session = localStorage.getItem("session");
  if (session != null) {
    session = JSON.parse(session);
    api.defaults.headers.common["Authorization"] = "JWT " + session.token;
    api.get('/usuarios/me/').then(() => {
      router.push({name: "Home"});
    }).catch(err => {
      if(err.response && err.response.data.error == "unauthenticated") {
        localStorage.removeItem("session");
        return next();
      }
      router.push({name: "Home"});
    });
  }
  next();
}
