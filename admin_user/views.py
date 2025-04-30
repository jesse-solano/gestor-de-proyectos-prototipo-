# Importa las funciones de autenticación de Django
from django.contrib.auth import login, logout
# Importa el decorador que requiere que el usuario esté autenticado
from django.contrib.auth.decorators import login_required
# Importa la vista de inicio de sesión de Django
from django.contrib.auth.views import LoginView
# Importa el formulario de inicio de sesión personalizado
from .forms import LoginForm
# Importa las funciones de renderizado, redirección y obtención de objetos o 404
from django.shortcuts import render, redirect, get_object_or_404
# Importa la función reverse para obtener URLs a partir de sus nombres
from django.urls import reverse
# Importa decoradores para verificar permisos de usuario y autenticación
from django.contrib.auth.decorators import user_passes_test, login_required
# Importa el modelo User de Django para manejar usuarios
from django.contrib.auth.models import User
# Importa el formulario de creación de proyectos
from .forms import ProjectForm
# Importa los modelos Project y CustomUser definidos en la aplicación
from .models import Project, CustomUser
# Importa el formulario de filtro de reportes
from .forms import ReportFilterForm
# Importa funciones de agregación de Django
from django.db.models import Count, Sum
# Importa configuraciones de tamaño de página y generación de PDF de ReportLab
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
# Importa la clase HttpResponse para devolver respuestas HTTP
from django.http import HttpResponse
# Importa la función TruncMonth para truncar fechas por mes
from django.db.models.functions import TruncMonth 

# Vista personalizada para el inicio de sesión de usuarios
class CustomLoginView(LoginView):
    template_name = 'admin_user/login.html'  # Plantilla HTML para el formulario de inicio de sesión
    authentication_form = LoginForm  # Formulario personalizado para el inicio de sesión

    # Redirige al usuario a la URL correspondiente según su rol después de un inicio de sesión exitoso
    def get_success_url(self):
        user = self.request.user  # Obtiene el usuario actual
        if user.is_superuser:  # Si el usuario es un superusuario (administrador)
            return reverse('admin_dashboard')  # Redirige al panel de administración
        else:  # Si el usuario es un usuario normal
            return reverse('home')  # Redirige a la página de inicio
    
@login_required  # Requiere que el usuario esté autenticado para acceder a esta vista
def home(request):
    # Renderiza la plantilla HTML 'home' para la página de inicio
    return render(request, 'admin_user/home.html')

# Función para verificar si el usuario es administrador
def is_admin(user):
    return user.is_superuser  # Retorna True si el usuario es un superusuario, de lo contrario retorna False

@login_required  # Requiere que el usuario esté autenticado para acceder a esta vista
@user_passes_test(is_admin)  # Requiere que el usuario pase la prueba de ser administrador
def admin_dashboard(request):
    users = User.objects.all()  # Obtiene todos los usuarios
    # Renderiza la plantilla HTML 'admin_dashboard' con la lista de usuarios
    return render(request, 'admin_user/admin_dashboard.html', {'users': users})

@login_required  # Requiere que el usuario esté autenticado para acceder a esta vista
@user_passes_test(is_admin)  # Requiere que el usuario pase la prueba de ser administrador
def create_project(request):
    if request.method == 'POST':  # Si el formulario se ha enviado mediante POST
        form = ProjectForm(request.POST)  # Crea un formulario con los datos enviados
        if form.is_valid():  # Si el formulario es válido
            project = form.save(commit=False)  # Crea un objeto Project pero no lo guarda en la base de datos aún
            project.owner = request.user  # Asigna el usuario actual como propietario del proyecto
            project.save()  # Guarda el proyecto en la base de datos
            return redirect('project_list')  # Redirige a la lista de proyectos
    else:  # Si se accede a la vista mediante GET
        form = ProjectForm()  # Crea un formulario vacío
    # Renderiza la plantilla HTML 'create_project' con el formulario
    return render(request, 'admin_user/create_project.html', {'form': form})

@login_required  # Requiere que el usuario esté autenticado para acceder a esta vista
def user_project_list(request):
    projects = Project.objects.filter(assigned_user=request.user)  # Filtra los proyectos asignados al usuario actual
    # Renderiza la plantilla HTML 'user_project_list' con la lista de proyectos del usuario
    return render(request, 'admin_user/user_project_list.html', {'projects': projects})

@login_required  # Requiere que el usuario esté autenticado para acceder a esta vista
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)  # Obtiene el proyecto por su ID o retorna un error 404 si no se encuentra
    if request.method == 'POST':  # Si el formulario se ha enviado mediante POST
        form = ProjectForm(request.POST, instance=project)  # Crea un formulario con los datos enviados y el proyecto existente
        if form.is_valid():  # Si el formulario es válido
            form.save()  # Guarda los cambios en el proyecto
            return redirect('user_project_list')  # Redirige a la lista de proyectos del usuario
    else:  # Si se accede a la vista mediante GET
        form = ProjectForm(instance=project)  # Crea un formulario con los datos del proyecto existente
    # Renderiza la plantilla HTML 'edit_project' con el formulario y el proyecto
    return render(request, 'admin_user/edit_project.html', {'form': form, 'project': project})

@login_required  # Requiere que el usuario esté autenticado para acceder a esta vista
def report_view(request):
    projects = Project.objects.all()  # Obtiene todos los proyectos
    filter_form = ReportFilterForm(request.GET or None)  # Crea un formulario de filtro para los reportes

    if filter_form.is_valid():  # Si el formulario de filtro es válido
        # Aplica los filtros seleccionados a los proyectos
        if filter_form.cleaned_data.get('phase'):
            projects = projects.filter(phase=filter_form.cleaned_data.get('phase'))
        if filter_form.cleaned_data.get('status'):
            projects = projects.filter(status=filter_form.cleaned_data.get('status'))
        if filter_form.cleaned_data.get('estatus'):
            projects = projects.filter(estatus=filter_form.cleaned_data.get('estatus'))
        if filter_form.cleaned_data.get('user'):
            projects = projects.filter(assigned_user=filter_form.cleaned_data.get('user'))
        if filter_form.cleaned_data.get('month') and filter_form.cleaned_data.get('year'):
            projects = projects.filter(
                created_at__month=filter_form.cleaned_data.get('month'),
                created_at__year=filter_form.cleaned_data.get('year')
            )

    # Contadores de fases, estados y estatus
    phase_counts = projects.values('phase').annotate(count=Count('id'))
    status_counts = projects.values('status').annotate(count=Count('id'))
    estatus_counts = projects.values('estatus').annotate(count=Count('id'))
    phase_month_counts = projects.annotate(month=TruncMonth('created_at')).values('month', 'phase').annotate(count=Count('id')).order_by('month')

    # Totales para fases, estados y estatus
    total_phase = sum(phase['count'] for phase in phase_counts)
    total_status = sum(status['count'] for status in status_counts)
    total_estatus = sum(estatus['count'] for estatus in estatus_counts)

    # Contexto para la plantilla HTML
    context = {
        'projects': projects,
        'filter_form': filter_form,
        'phase_counts': list(phase_counts),
        'status_counts': list(status_counts),
        'estatus_counts': list(estatus_counts),
        'phase_month_counts': list(phase_month_counts),
        'total_phase': total_phase,
        'total_status': total_status,
        'total_estatus': total_estatus,
    }
    # Renderiza la plantilla HTML 'report' con el contexto
    return render(request, 'admin_user/report.html', context)
