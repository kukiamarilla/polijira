import api from './api'

export default {
    list(idProyecto) {
        return api.get(`/proyectos/${idProyecto}/sprints/`).then(response => response.data)
    },
    create(sprint) {
        return api.post(`/sprints/`, sprint).then(response => response.data)
    },
    delete(id) {
        return api.delete(`/sprints/${id}`).then(response => response.data)
    }
}