"""
Configuración de URLs principales para ProjectFlow.
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # Redirigir la raíz directamente al gestor de proyectos
    path('', RedirectView.as_view(pattern_name='project_list', permanent=False)),
    
    # Administración Django
    path('admin/', admin.site.urls),
    
    # Aplicación principal
    path('admin_user/', include('admin_user.urls')),
]