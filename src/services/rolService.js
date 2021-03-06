import api from './api'

export default {
    list() {
        return api.get("/roles/").then(response => response.data)
    },
    create(data) {
        return api.post("/roles/", data).then(response => response.data)
    },
    update(id, data) {
        return api.put(`/roles/${id}/`, data).then(response => response.data)
    },
    delete(id) {
        return api.delete(`/roles/${id}/`).then(response => response.data)
    },
    agregarPermiso(id, data) {
        return api.post(`/roles/${id}/permisos/`, data).then(response => response.data)
    },
    eliminarPermiso(id, data) {
        return api.delete(`/roles/${id}/permisos/`, {data: data}).then(response => response.data)
    }
}