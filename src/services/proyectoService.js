import api from "./api";

export default {
  list() {
    return api.get("/proyectos/").then((response) => response.data);
  },
  retrieve(id) {
    return api.get(`/proyectos/${id}/`).then((response) => response.data);
  },
  create(data) {
    return api.post("/proyectos/", data).then((response) => response.data);
  },
  update(id, data) {
    return api.put(`/proyectos/${id}/`, data).then((response) => response.data);
  },
  delete(id) {
    return api.delete(`/proyectos/${id}/`).then((response) => response.data);
  },
  activar(id) {
    return api
      .post(`/proyectos/${id}/activar/`)
      .then((response) => response.data);
  },
  me(id) {
    return api.get(`/proyectos/${id}/me/`).then((response) => response.data);
  },
  backlog(id) {
    return api
      .get(`/proyectos/${id}/product_backlogs/`)
      .then((response) => response.data);
  },
  estimacionesPendientes(id) {
    return api
      .get(`/proyectos/${id}/estimaciones_pendientes/`)
      .then((response) => response.data);
  },
  finalizar(id) {
    return api.post(`/proyectos/${id}/finalizar/`).then(response => response.data)
  },
  cancelar(id) {
    return api.post(`/proyectos/${id}/cancelar/`).then(response => response.data)
  }
};
