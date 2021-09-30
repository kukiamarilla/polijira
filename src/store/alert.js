const INITIAL_STATE = {
  show: false,
  message: "",
  type: "",
};

const alert = {
  namespaced: true,
  state: { alert: INITIAL_STATE },
  mutations: {
    /**
     * @param payload is an object with two attributes:
     * -message: an string that the alert will show.
     * -type: has two values, 'success' and 'error',
     *        decide what icon will be shown.
     */
    showAlert(state, payload) {
      state.alert = { ...payload, show: true };
    },
    hideAlert(state) {
      state.alert = { ...INITIAL_STATE };
    },
  },
};

export default alert;
