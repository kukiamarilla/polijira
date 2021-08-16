import * as firebase from "firebase";

export default {
  login() {
    var provider = new firebase.auth.GoogleAuthProvider();
    return firebase
      .auth()
      .signInWithPopup(provider)
      .then(user =>
        firebase
          .auth()
          .currentUser.getIdToken()
          .then(token => {
            let session = {
              token: token,
              data: user
            };
            localStorage.setItem("session", JSON.stringify(session));
            return session;
          })
      );
  },
  logout() {
    localStorage.removeItem("session");
  },
  isLoggedIn() {
    return localStorage.getItem("session") != null;
  },
  registrar() {
    var provider = new firebase.auth.GoogleAuthProvider();
    return firebase
      .auth()
      .signInWithPopup(provider)
      .then(user =>
        firebase
          .auth()
          .currentUser.getIdToken()
          .then(token => {
            let session = {
              token: token,
              data: user
            };
            localStorage.setItem("session", JSON.stringify(session));
            return session;
          })
      );
  }
};
