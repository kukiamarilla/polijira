import api from './api'

export default {
    list() {
        return api.get("/roles/").then(response => response.data)
    }
}