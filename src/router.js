import Vue from "vue";
import Router from "vue-router";

import Login from "@/views/Login";
import NoActivado from "@/views/NoActivado";
import PageNotFound from "@/views/PageNotFound";
import Home from "@/views/Home";
import Unauthorized from "@/views/Unauthorized";
import Usuarios from "@/views/Usuarios";
import Autorizacion from "@/views/Autorizacion";
import PlantillaRolProyecto from "@/views/PlantillaRolProyecto";
import Proyecto from "@/views/Proyecto";
import AutorizacionProyecto from "@/views/AutorizacionProyecto";

import guest from "@/middleware/guest";
import auth from "@/middleware/auth";
import activated from "@/middleware/activated";
import unactivated from "@/middleware/unactivated";

Vue.use(Router);

const router = new Router({
  routes: [
    {
      path: "/login",
      name: "Login",
      component: Login,
      meta: {
        middleware: guest,
      },
    },
    {
      path: "/",
      name: "Home",
      component: Home,
      meta: {
        middleware: [auth, activated],
      },
    },
    {
      path: "/usuarios",
      name: "Usuarios",
      component: Usuarios,
      meta: {
        middleware: [auth, activated],
      },
    },
    {
      path: "/autorizacion",
      name: "Autorizacion",
      component: Autorizacion,
      meta: {
        middleware: [auth, activated],
      },
    },
    {
      path: "/proyectos/:id",
      name: "Proyecto",
      component: Proyecto,
      meta: {
        middleware: [auth, activated],
      },
    },
    {
      path: "/proyectos/:id/autorizacion",
      name: "Autorizacion Proyecto",
      component: AutorizacionProyecto,
      meta: {
        middleware: [auth, activated],
      },
    },
    {
      path: "/plantilla-rol-proyecto",
      name: "Plantilla de Roles de Proyecto",
      component: PlantillaRolProyecto,
      meta: {
        middleware: [auth, activated],
      },
    },
    {
      path: "/no-activado",
      name: "No Activado",
      component: NoActivado,
      meta: {
        middleware: [auth, unactivated],
      },
    },
    {
      path: "/no-autorizado",
      name: "No Autorizado",
      component: Unauthorized,
    },
    { path: "*", component: PageNotFound },
  ],
});

function nextFactory(context, middleware, index) {
  const subsequentMiddleware = middleware[index];
  if (!subsequentMiddleware) return context.next;

  return (...parameters) => {
    context.next(...parameters);
    const nextMiddleware = nextFactory(context, middleware, index + 1);
    subsequentMiddleware({ ...context, next: nextMiddleware });
  };
}

router.beforeEach((to, from, next) => {
  if (to.meta.middleware) {
    const middleware = Array.isArray(to.meta.middleware)
      ? to.meta.middleware
      : [to.meta.middleware];
    const context = {
      from,
      next,
      to,
      router,
    };
    const nextMiddleware = nextFactory(context, middleware, 1);
    return middleware[0]({ ...context, next: nextMiddleware });
  }
  return next();
});

export default router;
