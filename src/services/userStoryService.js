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
    }
}
