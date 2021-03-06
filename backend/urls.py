"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
"""

from django.contrib import admin
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.urls import path, include
from rest_framework import routers
from backend.api.views import \
    UsuarioViewSet, \
    PermisoViewSet, \
    RolViewSet, \
    ProyectoViewSet, \
    PermisoProyectoViewSet, \
    PlantillaRolProyectoViewSet, \
    RolProyectoViewSet, \
    MiembroViewSet, \
    HorarioViewSet, \
    UserStoryViewSet, \
    SprintViewSet, \
    SprintPlanningViewSet, \
    SprintBacklogViewSet, \
    ActividadViewSet, \
    ReviewViewSet
from backend.api.views.MiembroSprintViewSet import MiembroSprintViewSet

index_view = never_cache(TemplateView.as_view(template_name='index.html'))

router = routers.DefaultRouter()
router.register("usuarios", UsuarioViewSet, basename="usuarios")
router.register("permisos", PermisoViewSet, basename="permisos")
router.register("roles", RolViewSet, basename="roles")
router.register("proyectos", ProyectoViewSet, basename="proyectos")
router.register("plantillas", PlantillaRolProyectoViewSet, basename="plantillas")
router.register("roles-proyecto", RolProyectoViewSet, basename="roles-proyecto")
router.register("permisos-proyecto", PermisoProyectoViewSet, basename="permisos-proyecto")
router.register("miembros", MiembroViewSet, basename="miembros")
router.register("horarios", HorarioViewSet, basename="horarios")
router.register("user-stories", UserStoryViewSet, basename="user-stories")
router.register("sprints", SprintViewSet, basename="sprints")
router.register("sprint-planning", SprintPlanningViewSet, basename="sprint-planning")
router.register("reviews", ReviewViewSet, basename="reviews")
router.register("sprint-backlogs", SprintBacklogViewSet, basename="sprint-backlogs")
router.register("actividades", ActividadViewSet, basename="actividades")
router.register("miembros-sprint", MiembroSprintViewSet, basename="miembros-sprint")

urlpatterns = [

    # http://localhost:8000/
    path('', index_view, name='index'),

    # http://localhost:8000/api/<router-viewsets>
    path('api/', include(router.urls)),

    # http://localhost:8000/api/admin/
    path('api/admin/', admin.site.urls),
]
