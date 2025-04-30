"""
URL configuration for pasantias_proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

# Importa el módulo de administración de Django
from django.contrib import admin
# Importa las funciones path e include para definir rutas de URL y incluir otras configuraciones de URL
from django.urls import path, include
# Importa vistas genéricas de Django
from django.views.generic import RedirectView
# Importa las vistas del módulo admin_user
from admin_user import views as admin_user_views
# Importa la vista home del módulo admin_user
from admin_user.views import home

# Definición de las rutas de URL para el proyecto
urlpatterns = [
    # Ruta para la página de inicio, usando la vista home del módulo admin_user
    path('', admin_user_views.home, name='home'),
    
    # Ruta para el sitio de administración
    path('admin/', admin.site.urls),
    
    # Incluir las rutas de URL del módulo admin_user
    path('admin_user/', include('admin_user.urls')),
    
    # Ruta adicional para la página de inicio, usando la vista home del módulo admin_user
    path('', home, name='home'),
]