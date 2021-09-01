import api from './api'

export default {
  me() {
    return api.get("/usuarios/me/").then(response => response.data)
  }
}