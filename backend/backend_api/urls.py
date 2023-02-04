from backend_api.views import MovieViewSet
from rest_framework.routers import DefaultRouter
from backend_api import views
from backend_api.views import *
from rest_framework import routers
from django.urls import path, include


router = DefaultRouter()
router = routers.DefaultRouter()

router.register(r'usuarios', UsuarioViewSet)
router.register(r'partidas', PartidaViewSet)
router.register(r'participaciones', ParticipaViewSet)
router.register(r'dibujos', DibujoViewSet)
router.register(r'comentarios', ComentarioViewSet)
router.register(r'valoraciones', ValoraViewSet)

urlpatterns = [
    path("v1/", include(router.urls)),
]