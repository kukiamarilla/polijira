import api from './api'

export default {
    list() {
        return api.get("/roles/").then(response => response.data)
    },
    create(data) {
        return api.post("/roles/", data).then(response => response.data)
    }
}