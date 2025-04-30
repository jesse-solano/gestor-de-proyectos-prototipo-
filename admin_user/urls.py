from django.urls import path # Importa la función path para definir rutas de URL
from .views import CustomLoginView, admin_dashboard # Importa vistas específicas de la aplicación
from .views import create_project 
from .views import user_project_list, edit_project, report_view
from django.contrib.auth import views as auth_views # Importa las vistas de autenticación de Django

# Definición de las rutas de URL para la aplicación
urlpatterns = [
    # Ruta para el inicio de sesión personalizado
    path('login/', CustomLoginView.as_view(), name='login'),
    
    # Ruta para el panel de administración
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    
    # Ruta para la creación de proyectos
    path('projects/create/', create_project, name='create_project'),
    
    # Ruta para la lista de proyectos del usuario
    path('projects/', user_project_list, name='user_project_list'),
    
    # Ruta para la edición de un proyecto específico (usando el ID del proyecto)
    path('projects/edit/<int:project_id>/', edit_project, name='edit_project'),
    
    # Ruta para la vista de reportes
    path('reports/', report_view, name='report_view'),
    
    # Ruta para el cierre de sesión
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
]
