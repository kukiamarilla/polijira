import api from "./api";

export default {
    eliminar(id) {
        return api.delete(`/miembros-sprint/${id}/`).then(response => response.data);
    },
    reemplazar(id, miembro) {
        return api.post(`/miembros-sprint/${id}/reemplazar/`, miembro).then(response => response.data);
    },
}