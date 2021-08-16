import api from "../services/api";

export default function auth({ router, next }) {
  var session = localStorage.getItem("session");
  if (session == null) {
    return router.push({ name: "Login" });
  }
  session = JSON.parse(session);
  api.defaults.headers.common["Authorization"] = "JWT " + session.token;
  next();
}
