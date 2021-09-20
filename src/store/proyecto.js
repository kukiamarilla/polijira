import proyectoService from "@/services/proyectoService"

const authStore = {
    namespaced: true,
    state: {
      isLoggedIn: false,
      me: {
        rol: {
            id: 0,
            nombre: "",
            permisos: []
        },
        proyecto: {
            id: 0
        },
      }
    },
    actions: {
        getMe({commit}, proyecto){
            return proyectoService.me(proyecto).then(miembro => {
                commit("me", miembro)
                return miembro
            })
        }
    },
    mutations: {
      login(state) {
        state.isLoggedIn = true
      },
      logout(state) {
        localStorage.removeItem("session")
        state.isLoggedIn = false
      },
      me(state, me) {
        state.me = me
      },
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