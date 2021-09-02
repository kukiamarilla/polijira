import axios from 'axios'
import Cookies from 'js-cookie'
import store from '@/store'

let api = axios.create({
  baseURL: '/api',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': Cookies.get('csrftoken')
  }
})

api.interceptors.response.use((response) => response, (error) => {
  if(error.response)
    store.commit("alert/showAlert", {type: "error", message: error.response.data.message})
  else 
    store.commit("alert/showAlert", {type: "error", message: "No se pudo conectar con el servidor"})
  throw error;
});

export default api;