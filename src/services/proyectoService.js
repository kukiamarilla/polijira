import api from "./api";

export default {
  list() {
    return api.get("/proyectos/").then((response) => response.data);
  },
  create(data) {
    return api.post("/proyectos/", data).then((response) => response.data);
  },
  update(id, data) {
    return api
      .put(`/proyectos/${id}/`, data)
      .then((response) => response.data);
  },
  delete(id) {
    return api.delete(`/proyectos/${id}/`).then((response) => response.data);
  },
};
