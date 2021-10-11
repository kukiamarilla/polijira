import api from './api'

export default {
    list(idProyecto) {
        return api.get(`/proyectos/${idProyecto}/user_stories/`).then(response => response.data)
    },
    create(userStory) {
        return api.post(`/user-stories/`, userStory).then(response => response.data)
    }
}
