"""
Vistas de ProjectFlow - Gestor de Proyectos.
Cumple con PEP 8, anotaciones de tipos, optimización ORM (select_related / prefetch_related),
control de acceso RBAC y exportación de reportes.
"""

from typing import Any, Dict
import csv
import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count, Q, Sum
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import View

from .forms import (
    CustomPasswordResetForm,
    DeliverableForm,
    LoginForm,
    ProjectForm,
    ReportFilterForm,
    UserCreateForm,
    UserUpdateForm,
)
from .models import CustomUser, Deliverable, MonthlyTrend, Project


# ==============================================================================
# DECORADORES Y UTILIDADES RBAC
# ==============================================================================

def is_guest(request: HttpRequest) -> bool:
    """Retorna True si el usuario autenticado tiene rol Invitado."""
    return (
        request.user.is_authenticated
        and not request.user.is_superuser
        and request.user.role == CustomUser.ROLE_GUEST
    )


GUEST_BLOCK_MSG = (
    "⚠️ Acción no permitida en modo demostración. "
    "Inicia sesión con una cuenta con permisos para realizar cambios."
)


def role_required(*allowed_roles):
    """
    Decorador para restringir el acceso a vistas según el rol del usuario.
    Los superusuarios siempre tienen permiso.
    """
    def decorator(view_func):
        def _wrapped_view(request: HttpRequest, *args: Any, **kwargs: Any):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.is_superuser or request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            messages.error(
                request,
                f"Acceso restringido: Se requiere rol {', '.join(allowed_roles)} para esta acción."
            )
            return redirect('home')
        return _wrapped_view
    return decorator


# ==============================================================================
# AUTENTICACIÓN
# ==============================================================================

class CustomLoginView(View):
    """
    Vista de inicio de sesión con contador de intentos fallidos
    y maquetado idéntico a las Páginas 1 y 2 del PDF.
    """
    def get(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect('home')
        form = LoginForm()
        attempts = request.session.get('login_attempts', 0)
        show_error = request.session.pop('login_error', False)
        return render(request, 'admin_user/login.html', {
            'form': form,
            'attempts': attempts,
            'show_error': show_error,
        })

    def post(self, request: HttpRequest) -> HttpResponse:
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            request.session['login_attempts'] = 0
            messages.success(request, f"Bienvenido/a, {user.full_name_or_username}")
            if user.role == CustomUser.ROLE_ADMIN or user.is_superuser:
                return redirect('user_list')
            elif user.role == CustomUser.ROLE_COORDINATOR:
                return redirect('project_actualizar')
            return redirect('home')
        else:
            attempts = request.session.get('login_attempts', 0) + 1
            request.session['login_attempts'] = attempts
            request.session['login_error'] = True
            return render(request, 'admin_user/login.html', {
                'form': form,
                'attempts': attempts,
                'show_error': True,
            })


def guest_login_view(request: HttpRequest) -> HttpResponse:
    """
    Permite acceso instantáneo con perfil 'Invitado' (Páginas 1 y 2: Botón 'Ingresar como Invitado').
    """
    guest_user, _ = CustomUser.objects.get_or_create(
        username='invitado',
        defaults={
            'first_name': 'Usuario',
            'last_name': 'Invitado',
            'email': 'invitado@projectflow.dev',
            'role': CustomUser.ROLE_GUEST,
            'poo': 'Visitante Público',
            'avatar_color': '#10B981',
        }
    )
    login(request, guest_user)
    messages.info(request, "Has ingresado en Modo Invitado (Lectura y visualización de reportes).")
    return redirect('report_view')


def custom_logout_view(request: HttpRequest) -> HttpResponse:
    """Cierra la sesión del usuario de forma segura."""
    logout(request)
    messages.success(request, "Sesión cerrada correctamente.")
    return redirect('login')


# ==============================================================================
# PANTALLA PRINCIPAL / BIENVENIDA
# ==============================================================================

@login_required
def home(request: HttpRequest) -> HttpResponse:
    """
    Página de Inicio (Página 13 del PDF: Bienvenido usuario).
    """
    total_projects = Project.objects.count()
    completed_projects = Project.objects.filter(status=Project.COMPLETED).count()
    active_projects = Project.objects.filter(status=Project.ACTIVE).count()
    
    # Proyectos recientes con select_related para evitar N+1
    recent_projects = (
        Project.objects.select_related('owner', 'assigned_user')
        .order_by('-created_at')[:6]
    )

    return render(request, 'admin_user/home.html', {
        'total_projects': total_projects,
        'completed_projects': completed_projects,
        'active_projects': active_projects,
        'recent_projects': recent_projects,
    })


# ==============================================================================
# MÓDULO DE USUARIOS (Páginas 3, 4, 5, 6, 7 del PDF)
# ==============================================================================

@login_required
@role_required(CustomUser.ROLE_ADMIN)
def user_list(request: HttpRequest) -> HttpResponse:
    """
    Tabla de administración de usuarios (Página 3 del PDF).
    Incluye búsqueda por nombre/correo, filtro por rol, ordenamiento y paginación.
    """
    users_qs = CustomUser.objects.all().order_by('-date_joined')

    # Filtro de búsqueda
    search_query = request.GET.get('q', '').strip()
    if search_query:
        users_qs = users_qs.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(poo__icontains=search_query)
        )

    # Filtro por rol
    role_filter = request.GET.get('role', '').strip()
    if role_filter and role_filter != 'All':
        users_qs = users_qs.filter(role=role_filter)

    # Paginación
    per_page = int(request.GET.get('rows', 10))
    paginator = Paginator(users_qs, per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Formularios para modales
    user_form = UserCreateForm()

    return render(request, 'admin_user/user_list.html', {
        'page_obj': page_obj,
        'total_users': users_qs.count(),
        'search_query': search_query,
        'role_filter': role_filter,
        'per_page': per_page,
        'user_form': user_form,
    })


@login_required
@role_required(CustomUser.ROLE_ADMIN)
def user_create(request: HttpRequest) -> HttpResponse:
    """Creación de usuario (Página 4 del PDF: Agregar Nuevo Usuario)."""
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            messages.success(request, f"Usuario '{new_user.username}' creado con éxito.")
            return redirect('user_list')
        else:
            messages.error(request, "Error al crear usuario. Verifica los campos requeridos.")
    else:
        form = UserCreateForm()
    return render(request, 'admin_user/user_form.html', {'form': form, 'is_create': True})


@login_required
@role_required(CustomUser.ROLE_ADMIN)
def user_edit(request: HttpRequest, user_id: int) -> HttpResponse:
    """Edición de usuario (Página 5 del PDF: Editar Usuario)."""
    user_obj = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f"Usuario '{user_obj.username}' actualizado.")
            return redirect('user_list')
    else:
        form = UserUpdateForm(instance=user_obj)
    return render(request, 'admin_user/user_form.html', {
        'form': form,
        'user_obj': user_obj,
        'is_create': False,
    })


@login_required
@role_required(CustomUser.ROLE_ADMIN)
def user_reset_password(request: HttpRequest, user_id: int) -> HttpResponse:
    """Reset de contraseña seguro (Página 6 del PDF: Reset Password)."""
    user_obj = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            new_pwd = form.cleaned_data['new_password']
            user_obj.set_password(new_pwd)
            user_obj.save()
            messages.success(request, f"Contraseña actualizada para {user_obj.username}.")
            return redirect('user_list')
    else:
        form = CustomPasswordResetForm()
    return render(request, 'admin_user/user_reset_password.html', {
        'form': form,
        'user_obj': user_obj,
    })


@login_required
@role_required(CustomUser.ROLE_ADMIN)
def user_details_json(request: HttpRequest, user_id: int) -> JsonResponse:
    """Endpoint AJAX para modal de Detalles de Usuario (Página 7 del PDF)."""
    u = get_object_or_404(CustomUser, id=user_id)
    return JsonResponse({
        'id': u.id,
        'username': u.username,
        'full_name': u.get_full_name() or u.username,
        'poo': u.poo or 'N/A',
        'email': u.email or 'N/A',
        'personal_email': u.personal_email or 'N/A',
        'phone': u.phone or 'N/A',
        'role': u.role,
        'is_active': u.is_active,
        'last_login': u.last_login.strftime('%d/%m/%Y %H:%M') if u.last_login else 'Nunca',
    })


@login_required
@role_required(CustomUser.ROLE_ADMIN)
def user_toggle_block(request: HttpRequest, user_id: int) -> HttpResponse:
    """Bloquear / Desbloquear usuario (Botón 'Block' de Página 3)."""
    user_obj = get_object_or_404(CustomUser, id=user_id)
    if user_obj == request.user:
        messages.error(request, "No puedes bloquear tu propia cuenta de usuario.")
    else:
        user_obj.is_active = not user_obj.is_active
        user_obj.save()
        status_txt = "activado" if user_obj.is_active else "bloqueado"
        messages.warning(request, f"El usuario {user_obj.username} ha sido {status_txt}.")
    return redirect('user_list')


@login_required
@role_required(CustomUser.ROLE_ADMIN)
def user_delete(request: HttpRequest, user_id: int) -> HttpResponse:
    """Eliminar usuario."""
    user_obj = get_object_or_404(CustomUser, id=user_id)
    if user_obj == request.user:
        messages.error(request, "No puedes eliminar tu propia cuenta.")
    else:
        user_obj.delete()
        messages.success(request, f"Usuario {user_obj.username} eliminado.")
    return redirect('user_list')


# ==============================================================================
# MÓDULO DE GESTIÓN DE PROYECTOS (Páginas 8, 9 del PDF)
# ==============================================================================

@login_required
def project_list(request: HttpRequest) -> HttpResponse:
    """
    Vista principal de Proyectos (Página 8 del PDF: Gestión de Proyectos).
    Incluye tabla ordenable, búsqueda, paginación y menú de acciones.
    Optimizado con select_related y prefetch_related para evitar N+1.
    """
    projects_qs = (
        Project.objects.select_related('owner', 'assigned_user')
        .prefetch_related('deliverables')
        .all()
    )

    # Búsqueda
    q = request.GET.get('q', '').strip()
    if q:
        projects_qs = projects_qs.filter(
            Q(code__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q)
        )

    # Ordenamiento
    order = request.GET.get('order', '-created_at')
    valid_orders = ['id', '-id', 'name', '-name', 'start_date', '-start_date', 'real_percentage']
    if order in valid_orders:
        projects_qs = projects_qs.order_by(order)

    # Filtro por fase o estado
    phase = request.GET.get('phase', '')
    if phase:
        projects_qs = projects_qs.filter(phase=phase)

    status = request.GET.get('status', '')
    if status:
        projects_qs = projects_qs.filter(status=status)

    per_page = int(request.GET.get('rows', 10))
    paginator = Paginator(projects_qs, per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    users = CustomUser.objects.filter(is_active=True)

    return render(request, 'admin_user/project_list.html', {
        'page_obj': page_obj,
        'total_projects': projects_qs.count(),
        'q': q,
        'order': order,
        'phase': phase,
        'status': status,
        'per_page': per_page,
        'users': users,
        'phase_choices': Project.PHASE_CHOICES,
        'status_choices': Project.STATUS_CHOICES,
    })


@login_required
@role_required(CustomUser.ROLE_ADMIN, CustomUser.ROLE_COORDINATOR)
def project_create(request: HttpRequest) -> HttpResponse:
    """Crear Proyecto (Página 9 del PDF: Agregar Nuevo Proyecto)."""
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            proj = form.save(commit=False)
            proj.owner = request.user
            proj.save()
            messages.success(request, f"Proyecto '{proj.name}' creado correctamente.")
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'admin_user/project_form.html', {'form': form, 'is_create': True})


@login_required
@role_required(CustomUser.ROLE_ADMIN, CustomUser.ROLE_COORDINATOR)
def project_edit(request: HttpRequest, project_id: int) -> HttpResponse:
    """Editar proyecto existente."""
    proj = get_object_or_404(
        Project.objects.select_related('owner', 'assigned_user'),
        id=project_id
    )
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=proj)
        if form.is_valid():
            form.save()
            messages.success(request, f"Proyecto '{proj.name}' actualizado.")
            return redirect('project_list')
    else:
        form = ProjectForm(instance=proj)
    return render(request, 'admin_user/project_form.html', {
        'form': form,
        'project': proj,
        'is_create': False,
    })


@login_required
@role_required(CustomUser.ROLE_ADMIN)
def project_delete(request: HttpRequest, project_id: int) -> HttpResponse:
    """Eliminar proyecto."""
    proj = get_object_or_404(Project, id=project_id)
    proj.delete()
    messages.success(request, f"Proyecto eliminado.")
    return redirect('project_list')


# ==============================================================================
# MÓDULO DE ACTUALIZACIÓN / ESTATUS (Página 14 del PDF)
# ==============================================================================

@login_required
def project_actualizar(request: HttpRequest) -> HttpResponse:
    """
    Vista de Actualización de Proyectos (Página 14 del PDF).
    Tabla de seguimiento con switches de Procura, %Plan, %Real, %Desviación,
    y selectores de Fase, Estado y Estatus.
    Los usuarios con rol Invitado tienen acceso de solo lectura.
    """
    if request.method == 'POST':
        # Bloqueo de modo invitado
        if is_guest(request):
            messages.warning(request, GUEST_BLOCK_MSG)
            return redirect('project_actualizar')
        # Guardado en lote / actualización rápida
        project_id = request.POST.get('project_id')
        if project_id:
            proj = get_object_or_404(Project, id=project_id)
            proj.procura = request.POST.get('procura') == 'on' or request.POST.get('procura') == 'true'
            proj.planned_percentage = request.POST.get('planned_percentage', proj.planned_percentage)
            proj.real_percentage = request.POST.get('real_percentage', proj.real_percentage)
            proj.phase = request.POST.get('phase', proj.phase)
            proj.status = request.POST.get('status', proj.status)
            proj.estatus = request.POST.get('estatus', proj.estatus)
            proj.save()
            messages.success(request, f"Proyecto {proj.code} actualizado.")
            return redirect('project_actualizar')

    projects_qs = (
        Project.objects.select_related('owner', 'assigned_user')
        .order_by('-start_date')
    )

    # Filtros y ordenamiento
    phase = request.GET.get('phase')
    if phase:
        projects_qs = projects_qs.filter(phase=phase)
    
    order = request.GET.get('order', '-start_date')
    if order in ['start_date', '-start_date', 'real_percentage', '-real_percentage']:
        projects_qs = projects_qs.order_by(order)

    return render(request, 'admin_user/project_actualizar.html', {
        'projects': projects_qs,
        'phase_choices': Project.PHASE_CHOICES,
        'status_choices': Project.STATUS_CHOICES,
        'estatus_choices': Project.ESTATUS_CHOICES,
        'current_phase': phase,
    })


# ==============================================================================
# MÓDULO DE ENTREGABLES (Menú de acciones Página 8)
# ==============================================================================

@login_required
def deliverable_manage(request: HttpRequest, project_id: int) -> HttpResponse:
    """Gestionar entregables de un proyecto. Invitados tienen solo lectura."""
    project = get_object_or_404(
        Project.objects.prefetch_related('deliverables__assigned_to'),
        id=project_id
    )
    if request.method == 'POST':
        # Bloqueo de modo invitado
        if is_guest(request):
            messages.warning(request, GUEST_BLOCK_MSG)
            return redirect('deliverable_manage', project_id=project.id)
        form = DeliverableForm(request.POST)
        if form.is_valid():
            deliv = form.save(commit=False)
            deliv.project = project
            deliv.save()
            messages.success(request, f"Entregable '{deliv.title}' agregado al proyecto.")
            return redirect('deliverable_manage', project_id=project.id)
    else:
        form = DeliverableForm()

    return render(request, 'admin_user/deliverable_manage.html', {
        'project': project,
        'deliverables': project.deliverables.all(),
        'form': form,
        'is_readonly': is_guest(request),
    })


@login_required
def deliverable_delete(request: HttpRequest, deliverable_id: int) -> HttpResponse:
    """Eliminar un entregable. Bloqueado para usuarios Invitado."""
    if is_guest(request):
        messages.warning(request, GUEST_BLOCK_MSG)
        return redirect('project_list')
    deliv = get_object_or_404(Deliverable, id=deliverable_id)
    project_id = deliv.project_id
    deliv.delete()
    messages.success(request, "Entregable eliminado.")
    return redirect('deliverable_manage', project_id=project_id)


# ==============================================================================
# MÓDULO DE REPORTES Y DASHBOARDS (Páginas 10, 11, 12, 15, 16, 17 del PDF)
# ==============================================================================

@login_required
def report_view(request: HttpRequest) -> HttpResponse:
    """
    Vista integral de Reportes y Estadísticas.
    Incluye:
    - Contador regresivo hacia fecha de corte (89:00:00)
    - Filtros por Líderes, Fases, Estados, Estatus, PMO, Mes y Año
    - Resumen estadístico por Fase, Estado y Estatus con totales (Página 11)
    - Gráficos interactivos Chart.js (Barras, Donut, Comportamiento Enero-Noviembre)
    - Tipos de reportes (Semanal, Quincenal, Mensual, Trimestral, Semestral, Anual)
    """
    projects_qs = Project.objects.select_related('owner', 'assigned_user').all()

    # Filtros
    filter_form = ReportFilterForm(request.GET or None)
    selected_phase = request.GET.get('phase', '')
    selected_status = request.GET.get('status', '')
    selected_estatus = request.GET.get('estatus', '')
    selected_leader = request.GET.get('leader', '')
    selected_pmo = request.GET.get('pmo', '')
    selected_month = request.GET.get('month', '')
    selected_year = request.GET.get('year', '')
    search_q = request.GET.get('q', '').strip()

    if search_q:
        projects_qs = projects_qs.filter(
            Q(code__icontains=search_q) | Q(name__icontains=search_q)
        )
    if selected_phase:
        projects_qs = projects_qs.filter(phase=selected_phase)
    if selected_status:
        projects_qs = projects_qs.filter(status=selected_status)
    if selected_estatus:
        projects_qs = projects_qs.filter(estatus=selected_estatus)
    if selected_leader:
        projects_qs = projects_qs.filter(owner__username=selected_leader)
    if selected_pmo:
        projects_qs = projects_qs.filter(assigned_user__username=selected_pmo)
    if selected_month and selected_month.isdigit():
        projects_qs = projects_qs.filter(created_at__month=int(selected_month))
    if selected_year and selected_year.isdigit():
        projects_qs = projects_qs.filter(created_at__year=int(selected_year))

    # Agregaciones ORM optimizadas
    phase_counts = list(projects_qs.values('phase').annotate(count=Count('id')).order_by('phase'))
    status_counts = list(projects_qs.values('status').annotate(count=Count('id')).order_by('status'))
    estatus_counts = list(projects_qs.values('estatus').annotate(count=Count('id')).order_by('estatus'))

    total_projects = projects_qs.count()

    # Datos mensuales para gráfico "Comportamiento Enero - Noviembre"
    monthly_trends = MonthlyTrend.objects.all().order_by('month_number')
    months_labels = [m.month_name for m in monthly_trends]
    trend_in_progress = [m.in_progress for m in monthly_trends]
    trend_paused = [m.paused for m in monthly_trends]
    trend_closing = [m.closing for m in monthly_trends]
    trend_completed = [m.completed for m in monthly_trends]
    trend_cancelled = [m.cancelled for m in monthly_trends]
    trend_total = [m.total for m in monthly_trends]

    # Datos para gráficos de Fase
    phase_labels = ['Factibilizacion', 'Planificacion', 'Ejecucion']
    phase_counts_dict = {p['phase']: p['count'] for p in phase_counts}
    phase_chart_data = [phase_counts_dict.get(pl, 0) for pl in phase_labels]

    # Líderes y PMO disponibles para los chips
    leaders = CustomUser.objects.filter(role__in=[CustomUser.ROLE_ADMIN, CustomUser.ROLE_COORDINATOR])[:3]
    pmos = CustomUser.objects.filter(role=CustomUser.ROLE_PMO)[:2]

    context = {
        'projects': projects_qs[:30],
        'total_count': total_projects,
        'filter_form': filter_form,
        'phase_counts': phase_counts,
        'status_counts': status_counts,
        'estatus_counts': estatus_counts,
        # Gráficos
        'months_labels_json': json.dumps(months_labels),
        'trend_in_progress_json': json.dumps(trend_in_progress),
        'trend_paused_json': json.dumps(trend_paused),
        'trend_closing_json': json.dumps(trend_closing),
        'trend_completed_json': json.dumps(trend_completed),
        'trend_cancelled_json': json.dumps(trend_cancelled),
        'trend_total_json': json.dumps(trend_total),
        'phase_labels_json': json.dumps(phase_labels),
        'phase_chart_data_json': json.dumps(phase_chart_data),
        # Filtros seleccionados
        'selected_phase': selected_phase,
        'selected_status': selected_status,
        'selected_estatus': selected_estatus,
        'selected_leader': selected_leader,
        'selected_pmo': selected_pmo,
        'selected_month': selected_month,
        'selected_year': selected_year,
        'leaders': leaders,
        'pmos': pmos,
    }

    return render(request, 'admin_user/report.html', context)


@login_required
def report_export_csv(request: HttpRequest) -> HttpResponse:
    """Descarga de informe en formato CSV (Página 10: Botón 'Descarga de informe')."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ProjectFlow_Reporte_Consolidado.csv"'
    writer = csv.writer(response)
    writer.writerow([
        'ID Proyecto', 'Nombre', 'Líder', 'Usuario Asignado', 'Fase',
        'Estado', 'Estatus', '% Plan', '% Real', '% Desviación', 'Procura', 'Fecha Inicio'
    ])

    projects = Project.objects.select_related('owner', 'assigned_user').all()
    for p in projects:
        writer.writerow([
            p.display_id,
            p.name,
            p.owner.full_name_or_username,
            p.assigned_user.full_name_or_username if p.assigned_user else 'Sin asignar',
            p.phase,
            p.status,
            p.estatus,
            p.planned_percentage,
            p.real_percentage,
            p.deviation,
            'Si' if p.procura else 'No',
            p.start_date.strftime('%d/%m/%Y') if p.start_date else 'N/A'
        ])

    return response


# ==============================================================================
# RESPALDOS Y RESTAURACIÓN (Página 8: Botones Copia de Seguridad y Restaurar)
# ==============================================================================

@login_required
@role_required(CustomUser.ROLE_ADMIN)
def backup_data(request: HttpRequest) -> HttpResponse:
    """Genera respaldo en formato JSON de todos los proyectos y entregables."""
    projects_data = []
    for p in Project.objects.prefetch_related('deliverables').all():
        deliverables_list = [
            {'title': d.title, 'phase': d.phase, 'progress': d.progress, 'is_completed': d.is_completed}
            for d in p.deliverables.all()
        ]
        projects_data.append({
            'code': p.code,
            'name': p.name,
            'description': p.description,
            'objective': p.objective,
            'phase': p.phase,
            'status': p.status,
            'estatus': p.estatus,
            'procura': p.procura,
            'planned_percentage': p.planned_percentage,
            'real_percentage': p.real_percentage,
            'deliverables': deliverables_list,
        })

    response = HttpResponse(
        json.dumps(projects_data, indent=2, ensure_ascii=False),
        content_type='application/json'
    )
    response['Content-Disposition'] = 'attachment; filename="ProjectFlow_Backup.json"'
    return response


@login_required
@role_required(CustomUser.ROLE_ADMIN)
def restore_data(request: HttpRequest) -> HttpResponse:
    """Restaura los datos originales del sistema."""
    from django.core.management import call_command
    try:
        call_command('seed_data')
        messages.success(request, "Datos de prueba restaurados exitosamente según el PDF.")
    except Exception as e:
        messages.error(request, f"Error al restaurar: {str(e)}")
    return redirect('project_list')
