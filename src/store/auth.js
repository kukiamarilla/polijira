const authStore = {
  namespaced: true,
  state: {
    isLoggedIn: false,
    me: {
      id: 0,
      nombre: "",
      email: "",
      estado: "",
      rol: {
        nombre: "",
        permisos: []
      }
    }
  },
  mutations: {
    login(state) {
      state.isLoggedIn = true
    },
    logout(state) {
      state.isLoggedIn = false
    },
    me(state, me) {
      state.me = me
    }
  }
  
}

export default authStore;