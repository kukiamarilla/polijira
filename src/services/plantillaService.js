import api from "./api";

export default {
  list() {
    return api.get("/plantillas/").then((response) => response.data);
  },
  create(data) {
    return api.post("/plantillas/", data).then((response) => response.data);
  },
  update(id, data) {
    return api
      .put(`/plantillas/${id}/`, data)
      .then((response) => response.data);
  },
  delete(id) {
    return api.delete(`/plantillas/${id}/`).then((response) => response.data);
  },
  agregarPermiso(id, data) {
    return api
      .post(`/plantillas/${id}/permisos/`, data)
      .then((response) => response.data);
  },
  eliminarPermiso(id, data) {
    return api
      .delete(`/plantillas/${id}/permisos/`, { data: data })
      .then((response) => response.data);
  },
};
