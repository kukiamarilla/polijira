import api from "../services/api";

export default function activated({ router, next }) {
  api.get('/usuarios/me/').then(() => {
      next()
  }).catch(err => {
    if (err.response && err.response.data.error == "unactivated") {
      router.push({name: "No Activado"});
    }
  });
}
