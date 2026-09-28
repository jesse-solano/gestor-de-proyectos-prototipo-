"""
Rutas de la aplicación admin_user (ProjectFlow).
"""

from django.urls import path
from . import views

urlpatterns = [
    # Autenticación
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('guest-login/', views.guest_login_view, name='guest_login'),
    path('logout/', views.custom_logout_view, name='logout'),

    # Inicio / Bienvenida
    path('home/', views.home, name='home'),

    # Módulo de Usuarios (Página 3, 4, 5, 6, 7)
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:user_id>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:user_id>/reset-password/', views.user_reset_password, name='user_reset_password'),
    path('users/<int:user_id>/details/', views.user_details_json, name='user_details_json'),
    path('users/<int:user_id>/toggle-block/', views.user_toggle_block, name='user_toggle_block'),
    path('users/<int:user_id>/delete/', views.user_delete, name='user_delete'),

    # Módulo de Proyectos (Página 8, 9)
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:project_id>/edit/', views.project_edit, name='project_edit'),
    path('projects/<int:project_id>/delete/', views.project_delete, name='project_delete'),

    # Módulo de Actualización / Estatus (Página 14)
    path('projects/actualizar/', views.project_actualizar, name='project_actualizar'),

    # Módulo de Entregables
    path('projects/<int:project_id>/deliverables/', views.deliverable_manage, name='deliverable_manage'),
    path('deliverables/<int:deliverable_id>/delete/', views.deliverable_delete, name='deliverable_delete'),

    # Módulo de Reportes y Estadísticas (Páginas 10, 11, 12, 15, 16, 17)
    path('reports/', views.report_view, name='report_view'),
    path('reports/export-csv/', views.report_export_csv, name='report_export_csv'),

    # Respaldo y Restauración
    path('backup/', views.backup_data, name='backup_data'),
    path('restore/', views.restore_data, name='restore_data'),
]
