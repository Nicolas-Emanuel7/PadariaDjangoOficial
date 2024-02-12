from django import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from usuario import views

urlpatterns = [
    path('', views.usuario_cadastro, name='login'),
    path('admin/', admin.site.urls),
    path('usuario/', include('usuario.urls')),
    path('gerenciamento/', include('gerenciamento.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
