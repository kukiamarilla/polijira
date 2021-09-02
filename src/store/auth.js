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
  },
  getters: {
    hasPermission: (state) => (permission) => {
      return state.me.rol.permisos.map(permiso => permiso.codigo).includes(permission)
    },
    hasPermissions: (state, getters) => (permissions) => {
      return permissions.every(getters.hasPermission)
    },
    hasAnyPermission: (state, getters) => (permissions) => {
      return permissions.some(getters.hasPermission)
    }
  }
}

export default authStore;