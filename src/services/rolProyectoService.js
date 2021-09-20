import api from './api'

export default {
    list(proyecto) {
        return api.get(`/proyectos/${proyecto}/roles/`).then(response => response.data)
    },
    create(data) {
        return api.post("/roles-proyecto/", data).then(response => response.data)
    },
    update(id, data) {
        return api.put(`/roles-proyecto/${id}/`, data).then(response => response.data)
    },
    delete(id) {
        return api.delete(`/roles-proyecto/${id}/`).then(response => response.data)
    },
    agregarPermiso(id, data) {
        return api.post(`/roles-proyecto/${id}/permisos/`, data).then(response => response.data)
    },
    eliminarPermiso(id, data) {
        return api.delete(`/roles-proyecto/${id}/permisos/`, {data: data}).then(response => response.data)
    }
}