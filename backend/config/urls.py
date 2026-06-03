"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from config.views import detalle_sala_page, index, login_page, mapa_page, usuario_page
from reservas.views import crear_reserva, historial_html, reservas_all_html, reservas_html
from salas.views import salas_api, sala_detalle_api
from usuarios.views import api_login, api_register

urlpatterns = [
    path('', index, name='index'),
    path('login.html', login_page, name='login_page'),
    path('mapa.html', mapa_page, name='mapa_page'),
    path('detalleSalas.html', detalle_sala_page, name='detalle_sala_page'),
    path('usuario.html', usuario_page, name='usuario_page'),
    path('api/login', api_login, name='api_login'),
    path('api/register', api_register, name='api_register'),
    path('salas', salas_api, name='salas_api'),
    path('salas/<str:param>', sala_detalle_api, name='sala_detalle_api'),
    path('reservas/all', reservas_all_html, name='reservas_all_html'),
    path('reservas/<str:param>', reservas_html, name='reservas_html'),
    path('reservas', crear_reserva, name='crear_reserva'),
    path('historial/<str:param>', historial_html, name='historial_html'),
    path('admin/', admin.site.urls),
]
