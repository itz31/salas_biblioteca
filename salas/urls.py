from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'disponibilidades', views.DisponibilidadViewSet, basename='disponibilidad')
router.register(r'', views.SalasViewSet, basename='sala')

urlpatterns = [
    path('', include(router.urls)),
]
