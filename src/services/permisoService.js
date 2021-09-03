import api from "./api"

export default {
    list() {
        return api.get("/permisos/").then(response => response.data)
    }
}