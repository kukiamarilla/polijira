import api from "./api";

export default {
  create(review) {
    return api.post(`/reviews/`, review).then((response) => response.data);
  },
  update(id, review) {
    return api.put(`/reviews/${id}/`, review).then((response) => response.data);
  },
  delete(id) {
    return api.delete(`/reviews/${id}/`).then((response) => response.data);
  },
};
