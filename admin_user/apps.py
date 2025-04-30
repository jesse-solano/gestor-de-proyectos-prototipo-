# Importa AppConfig para configurar la aplicación
from django.apps import AppConfig

# Configuración de la aplicación 'admin_user'
class AdminUserConfig(AppConfig):
    # Campo de clave primaria predeterminado para los modelos de esta aplicación
    default_auto_field = 'django.db.models.BigAutoField'
    # Nombre de la aplicación
    name = 'admin_user'
