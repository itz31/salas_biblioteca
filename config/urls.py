from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    # API separada por app
    path('api/usuarios/', include('usuario.urls')),
    path('api/salas/', include('salas.urls')),
    path('api/reservas/', include('reservas.urls')),
    # Páginas frontend servidas por Django
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('mapa/', TemplateView.as_view(template_name='mapa.html'), name='mapa'),
    path('usuario/', TemplateView.as_view(template_name='usuario.html'), name='usuario'),
    path('detalle-sala/', TemplateView.as_view(template_name='detalleSalas.html'), name='detalle-sala'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
