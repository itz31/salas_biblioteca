from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'historial', views.HistorialViewSet, basename='historial')
router.register(r'', views.ReservasViewSet, basename='reserva')

urlpatterns = [
    path('', include(router.urls)),
]
