# Importa el módulo forms de Django para crear formularios
from django import forms
# Importa formularios de autenticación y campos de nombre de usuario de Django
from django.contrib.auth.forms import AuthenticationForm, UsernameField
# Importa la función de traducción para internacionalización
from django.utils.translation import gettext_lazy as _
# Importa los modelos Project y CustomUser definidos en la aplicación
from .models import Project, CustomUser

# Formulario de inicio de sesión personalizado
class LoginForm(AuthenticationForm):
    # Campo de nombre de usuario con un widget de entrada de texto personalizado
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    # Campo de contraseña con un widget de entrada de contraseña personalizado
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    
# Formulario para crear y editar proyectos
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project  # Modelo asociado al formulario
        fields = ['name', 'description', 'phase', 'status', 'estatus', 'assigned_user', 'real_percentage', 'planned_percentage', 'deviation']  # Campos del formulario
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),  # Widget de área de texto para la descripción
            'deviation': forms.TextInput(attrs={'readonly': 'readonly'}),  # Campo de desviación de solo lectura
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        # Desactiva los campos de nombre y usuario asignado
        self.fields['name'].disabled = True
        self.fields['assigned_user'].disabled = True

    # Validación personalizada para el campo de porcentaje real
    def clean_real_percentage(self):
        real_percentage = self.cleaned_data.get('real_percentage')
        if not all(char.isdigit() or char == '%' for char in real_percentage):
            raise forms.ValidationError('Solo se permiten números y el símbolo %.')
        return real_percentage

    # Validación personalizada para el campo de porcentaje planificado
    def clean_planned_percentage(self):
        planned_percentage = self.cleaned_data.get('planned_percentage')
        if not all(char.isdigit() or char == '%' for char in planned_percentage):
            raise forms.ValidationError('Solo se permiten números y el símbolo %.')
        return planned_percentage
        
# Formulario para filtrar reportes
class ReportFilterForm(forms.Form):
    phase = forms.ChoiceField(choices=[('', 'All')] + Project.PHASE_CHOICES, required=False)  # Campo de selección de fase
    status = forms.ChoiceField(choices=[('', 'All')] + Project.STATUS_CHOICES, required=False)  # Campo de selección de estado
    estatus = forms.ChoiceField(choices=[('', 'All')] + Project.ESTATUS_CHOICES, required=False)  # Campo de selección de estatus
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all(), required=False)  # Campo de selección de usuario
    month = forms.ChoiceField(choices=[('', 'All')] + [(str(i), str(i)) for i in range(1, 13)], required=False)  # Campo de selección de mes
    year = forms.ChoiceField(choices=[('', 'All')] + [(str(i), str(i)) for i in range(2020, 2030)], required=False)  # Campo de selección de año
