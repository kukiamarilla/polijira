import api from './api'

export default {
    list(idProyecto) {
        return api.get(`/proyectos/${idProyecto}/user_stories`).then(response => response.data)
    }
}
