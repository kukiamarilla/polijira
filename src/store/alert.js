const INITIAL_STATE = {
  show: false,
  message: "",
  type: "",
};

const alert = {
  namespaced: true,
  state: { alert: INITIAL_STATE },
  mutations: {
    showAlert(state, payload) {
      state.alert = { show: true, ...payload };
    },
    hideAlert(state) {
      state.alert = { ...INITIAL_STATE };
    },
  },
};

export default alert;
