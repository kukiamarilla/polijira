import api from "./api";

export default {
  list(idProyecto) {
    return api
      .get(`/proyectos/${idProyecto}/sprints/`)
      .then((response) => response.data);
  },
  retrieve(id) {
    return api.get(`/sprints/${id}/`).then((response) => response.data);
  },
  create(sprint) {
    return api.post(`/sprints/`, sprint).then((response) => response.data);
  },
  delete(id) {
    return api.delete(`/sprints/${id}`).then((response) => response.data);
  },
  iniciarSprintPlanning(id) {
    return api
      .post(`/sprint-planning/${id}/iniciar/`)
      .then((response) => response.data);
  },
  finalizarSprintPlanning(id) {
    return api
      .post(`/sprint-planning/${id}/finalizar/`)
      .then((response) => response.data);
  },
  miembros(id) {
    return api
      .get(`/sprint-planning/${id}/miembros/`)
      .then((response) => response.data);
  },
  agregarMiembro(id, miembro) {
    return api
      .post(`/sprint-planning/${id}/miembros/`, miembro)
      .then((response) => response.data);
  },
  eliminarMiembro(id, miembro) {
    return api
      .delete(`/sprint-planning/${id}/miembros/`, { data: miembro })
      .then((response) => response.data);
  },
  sprintBacklog(id) {
    return api
      .get(`/sprints/${id}/sprint_backlogs/`)
      .then((response) => response.data);
  },
  agregarUserStory(id, payload) {
    return api
      .post(`/sprint-planning/${id}/planificar_user_story/`, payload)
      .then((response) => response.data);
  },
  eliminarUserStory(id, payload) {
    return api
      .post(`/sprint-planning/${id}/devolver_user_story/`, payload)
      .then((response) => response.data);
  },
  responderEstimacion(id, payload) {
    return api
      .post(`/sprint-backlogs/${id}/responder_estimacion/`, payload)
      .then((response) => response.data);
  },
  activar(id) {
      return api.post(`/sprints/${id}/activar/`).then(response => response.data)
  }
};
