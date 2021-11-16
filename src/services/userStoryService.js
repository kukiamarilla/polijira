import api from './api'

export default {
    list(idProyecto) {
        return api.get(`/proyectos/${idProyecto}/user_stories/`).then(response => response.data)
    },
    create(userStory) {
        return api.post(`/user-stories/`, userStory).then(response => response.data)
    },
    update(id, userStory) {
        return api.put(`/user-stories/${id}/`, userStory).then(response => response.data)
    },
    delete(id) {
        return api.delete(`/user-stories/${id}/`).then(response => response.data)
    },
    mover(id, estado) {
        return api.post(`/sprint-backlogs/${id}/mover/`, {"estado_kanban": estado}).then(response => response.data)
    },
    actividades(id) {
        return api.get(`/sprint-backlogs/${id}/actividades/`).then(response => response.data)
    },
    registrarActividad(actividad) {
        return api.post(`/actividades/`, actividad).then(response => response.data)
    },
    eliminarActividad(id) {
        return api.delete(`/actividades/${id}/`,).then(response => response.data)
    },
    actualizarActividad(id, actividad) {
        return api.put(`/actividades/${id}/`, actividad).then(response => response.data)
    }
}
