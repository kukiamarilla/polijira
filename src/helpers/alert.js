import store from "@/store"

export default {
    success(message) {
        store.commit("alert/showAlert", {type: "success", message: message});
    },
    error(message) {
        store.commit("alert/showAlert", {type: "error", message: message});
    }
}