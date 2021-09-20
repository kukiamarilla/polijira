import api from "./api"

export default {
    list() {
        return api.get("/permisos-proyecto/").then(response => response.data)
    }
}