import api from './api'

export default {
  me() {
    return api.get("/usuarios/me/").then(response => response.data)
  },
  list() {
    return api.get("/usuarios/").then(response => response.data)
  },
  activar(id) {
    return api.post(`/usuarios/${id}/activar/`).then(response => response.data)
  },
  desactivar(id) {
    return api.post(`/usuarios/${id}/desactivar/`).then(response => response.data)
  },
  asignarRol(id, data) {
    return api.post(`/usuarios/${id}/asignar_rol/`, data).then(response => response.data)
  }
}