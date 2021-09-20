import api from "./api";

export default {
    list(proyecto) {
        return api.get(`/proyectos/${proyecto}/miembros/`).then(response => response.data)
    },
    create(data) {
        return api.post("/miembros/", data).then(response => response.data)
    },
    update(id, data) {
        return api.put(`/miembros/${id}/`, data).then(response => response.data)
    },
    delete(id) {
        return api.delete(`/miembros/${id}/`).then(response => response.data)
    },
    modificarHorario(id, horario) {
        return api.put(`/horarios/${id}/`, horario).then(response => response.data)
    },
}