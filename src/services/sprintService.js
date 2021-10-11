import api from './api'

export default {
    list(idProyecto) {
        return api.get(`/proyectos/${idProyecto}/sprints/`).then(response => response.data)
    },
    retrieve(id) {
        return api.get(`/sprints/${id}/`).then(response => response.data)
    },
    create(sprint) {
        return api.post(`/sprints/`, sprint).then(response => response.data)
    },
    delete(id) {
        return api.delete(`/sprints/${id}`).then(response => response.data)
    },
    iniciarSprintPlanning(id) {
        return api.post(`/sprint-planning/${id}/iniciar/`).then(response => response.data)
    },
    miembros(id) {
        return api.get(`/sprint-planning/${id}/miembros/`).then(response => response.data)
    },
    agregarMiembro(id, miembro) {
        return api.post(`/sprint-planning/${id}/miembros/`, miembro).then(response => response.data)
    },
    eliminarMiembro(id, miembro) {
        return api.delete(`/sprint-planning/${id}/miembros/`, {data: miembro}).then(response => response.data)
    }
}