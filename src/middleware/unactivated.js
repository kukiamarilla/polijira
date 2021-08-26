import api from "../services/api";

export default function activated({ router, next }) {
  api.get('/usuarios/me/').then(() => {
      router.push({name: "Home"});
}).catch(err => {
    if(err.response && err.response.data.error == "unactivated") {
        next()
    }
  });
}
