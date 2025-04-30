# Importa el módulo admin de Django para registrar modelos en el sitio de administración
from django.contrib import admin
# Importa UserAdmin para personalizar la administración de usuarios
from django.contrib.auth.admin import UserAdmin
# Importa los modelos CustomUser y Project definidos en la aplicación
from .models import CustomUser, Project

# Clase de administración personalizada para el modelo CustomUser
class CustomUserAdmin(UserAdmin):
    pass

# Registra el modelo CustomUser con la clase de administración CustomUserAdmin en el sitio de administración
admin.site.register(CustomUser, CustomUserAdmin)
# Registra el modelo Project en el sitio de administración
admin.site.register(Project)