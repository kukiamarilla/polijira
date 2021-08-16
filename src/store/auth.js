const authStore = {
    namespaced: true,
    state: {
        isLoggedIn: false
    },
    mutations: {
        login(state) {
            state.isLoggedIn = true
        },
        logout(state) {
            state.isLoggedIn = false
        },
    }
    
}

export default authStore;