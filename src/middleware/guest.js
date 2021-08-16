import api from "../services/api";

export default function guest({ router, next }) {
  var session = localStorage.getItem("session");
  if (session != null) {
    session = JSON.parse(session);
    api.defaults.headers.common["Authorization"] = "JWT " + session.token;
    return router.push({ name: "No Activado" });
  }
  next();
}
