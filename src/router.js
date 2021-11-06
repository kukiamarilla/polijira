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
import Miembros from "@/views/Miembros";
import UserStories from "@/views/UserStories";
import ProductBacklog from "@/views/ProductBacklog";
import Sprints from "@/views/Sprints";
import SprintPlanning1 from "@/views/SprintPlanning1";
import SprintPlanning2 from "@/views/SprintPlanning2";
import SprintPlanning3 from "@/views/SprintPlanning3";
import EstimacionesPendientes from "@/views/EstimacionesPendientes";

import guest from "@/middleware/guest";
import auth from "@/middleware/auth";
import activated from "@/middleware/activated";
import unactivated from "@/middleware/unactivated";
import proyecto from "@/middleware/proyecto";

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
      path: "/plantilla-rol-proyecto",
      name: "Plantilla de Roles de Proyecto",
      component: PlantillaRolProyecto,
      meta: {
        middleware: [auth, activated],
      },
    },
    {
      path: "/proyectos/:id",
      name: "Proyecto",
      component: Proyecto,
      meta: {
        middleware: [auth, activated, proyecto],
      },
    },
    {
      path: "/proyectos/:id/autorizacion",
      name: "Autorizacion Proyecto",
      component: AutorizacionProyecto,
      meta: {
        middleware: [auth, activated, proyecto],
      },
    },
    {
      path: "/proyectos/:id/miembros",
      name: "Miembros Proyecto",
      component: Miembros,
      meta: {
        middleware: [auth, activated, proyecto],
      },
    },
    {
      path: "/proyectos/:id/user-stories",
      name: "User Stories",
      component: UserStories,
      meta: {
        middleware: [auth, activated, proyecto],
      },
    },
    {
      path: "/proyectos/:id/backlog",
      name: "Product Backlog",
      component: ProductBacklog,
      meta: {
        middleware: [auth, activated, proyecto],
      },
    },
    {
      path: "/proyectos/:id/sprints",
      name: "Sprints",
      component: Sprints,
      meta: {
        middleware: [auth, activated, proyecto],
      },
    },
    {
      path: "/proyectos/:id/sprint-planning/:idSprint/paso-1",
      name: "Sprint Planning Paso 1",
      component: SprintPlanning1,
      meta: {
        middleware: [auth, activated, proyecto],
      },
    },
    {
      path: "/proyectos/:id/sprint-planning/:idSprint/paso-2",
      name: "Sprint Planning Paso 2",
      component: SprintPlanning2,
      meta: {
        middleware: [auth, activated, proyecto],
      },
    },
    {
      path: "/proyectos/:id/sprint-planning/:idSprint/paso-3",
      name: "Sprint Planning Paso 3",
      component: SprintPlanning3,
      meta: {
        middleware: [auth, activated, proyecto],
      },
    },
    {
      path: "/proyectos/:id/estimaciones-pendientes",
      name: "Estimaciones Pendientes",
      component: EstimacionesPendientes,
      meta: {
        middleware: [auth, activated, proyecto],
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
