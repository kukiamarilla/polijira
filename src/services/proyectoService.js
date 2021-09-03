import api from "./api";

export default {
  list() {
    return api.get("/proyectos").then((response) => response.data);
  },
  create(data) {
    return api.post("/proyectos", data).then((response) => response.data);
  },
  modify(data) {
    return api
      .put(`/proyectos/${data.id}`, data)
      .then((response) => response.data);
  },
  delete(id) {
    return api.put(`/proyectos/${id}`).then((response) => response.data);
  },
};
