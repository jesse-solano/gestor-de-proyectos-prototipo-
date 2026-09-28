"""
Formularios de ProjectFlow con validaciones robustas y widgets personalizados.
Cumple con PEP 8 y alineación exacta con los campos mostrados en el PDF.
"""

from typing import Any, Dict
import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Project, CustomUser, Deliverable


class LoginForm(AuthenticationForm):
    """
    Formulario de autenticación personalizado con estilos de píldora
    y seguimiento de intentos fallidos.
    """
    username = UsernameField(
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'class': 'login-input-pill',
            'placeholder': 'Ingrese su usuario',
            'id': 'id_username',
        })
    )
    password = forms.CharField(
        label=_("Contraseña"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'login-input-pill',
            'placeholder': '••••••••',
            'id': 'id_password',
        }),
    )


class UserCreateForm(forms.ModelForm):
    """
    Formulario para creación de usuarios (Página 4 del PDF: Agregar Nuevo Usuario).
    """
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'modal-form-input', 'placeholder': 'Contraseña segura'}),
    )
    password_confirm = forms.CharField(
        label="Repetir Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'modal-form-input', 'placeholder': 'Confirmar contraseña'}),
    )

    class Meta:
        model = CustomUser
        fields = [
            'poo',
            'username',
            'first_name',
            'last_name',
            'email',
            'personal_email',
            'phone',
            'role',
            'password',
        ]
        widgets = {
            'poo': forms.TextInput(attrs={'class': 'modal-form-input', 'placeholder': 'Ej. Gerencia de TI / POO'}),
            'username': forms.TextInput(attrs={'class': 'modal-form-input', 'placeholder': 'Nombre de usuario'}),
            'first_name': forms.TextInput(attrs={'class': 'modal-form-input', 'placeholder': 'Nombre(s)'}),
            'last_name': forms.TextInput(attrs={'class': 'modal-form-input', 'placeholder': 'Apellido(s)'}),
            'email': forms.EmailInput(attrs={'class': 'modal-form-input', 'placeholder': 'correo@empresa.com'}),
            'personal_email': forms.EmailInput(attrs={'class': 'modal-form-input', 'placeholder': 'correo@gmail.com'}),
            'phone': forms.TextInput(attrs={'class': 'modal-form-input', 'placeholder': '+58 416-0000000'}),
            'role': forms.Select(attrs={'class': 'modal-form-input form-select'}),
        }

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('password_confirm')
        if p1 and p2 and p1 != p2:
            raise ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit: bool = True) -> CustomUser:
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """
    Formulario para edición de usuarios (Página 5 del PDF: Editar Usuario).
    """
    class Meta:
        model = CustomUser
        fields = [
            'poo',
            'username',
            'first_name',
            'last_name',
            'email',
            'personal_email',
            'phone',
            'role',
            'is_active',
        ]
        widgets = {
            'poo': forms.TextInput(attrs={'class': 'modal-form-input'}),
            'username': forms.TextInput(attrs={'class': 'modal-form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'modal-form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'modal-form-input'}),
            'email': forms.EmailInput(attrs={'class': 'modal-form-input'}),
            'personal_email': forms.EmailInput(attrs={'class': 'modal-form-input'}),
            'phone': forms.TextInput(attrs={'class': 'modal-form-input'}),
            'role': forms.Select(attrs={'class': 'modal-form-input form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CustomPasswordResetForm(forms.Form):
    """
    Formulario de reseteo de contraseña (Página 6 del PDF: Reset Password).
    Valida requisitos mínimos de seguridad:
    - Mínimo 8 caracteres
    - Al menos una letra mayúscula y una minúscula
    - Al menos un carácter especial
    """
    new_password = forms.CharField(
        label="Nueva Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'modal-form-input', 'placeholder': 'Nueva contraseña segura'}),
    )
    confirm_password = forms.CharField(
        label="Repetir Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'modal-form-input', 'placeholder': 'Confirmar nueva contraseña'}),
    )

    def clean_new_password(self) -> str:
        password = self.cleaned_data.get('new_password')
        if len(password) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Debe contener al menos una letra mayúscula.")
        if not re.search(r'[a-z]', password):
            raise ValidationError("Debe contener al menos una letra minúscula.")
        if not re.search(r'[^A-Za-z0-9]', password):
            raise ValidationError("Debe contener al menos un carácter especial (ej. !@#$%^&*).")
        return password

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        p1 = cleaned_data.get('new_password')
        p2 = cleaned_data.get('confirm_password')
        if p1 and p2 and p1 != p2:
            raise ValidationError("Las contraseñas no coinciden.")
        return cleaned_data


class ProjectForm(forms.ModelForm):
    """
    Formulario completo para crear y editar proyectos (Páginas 8, 9 y 14 del PDF).
    """
    class Meta:
        model = Project
        fields = [
            'code',
            'name',
            'description',
            'objective',
            'owner',
            'assigned_user',
            'start_date',
            'cut_date',
            'end_date',
            'procura',
            'planned_percentage',
            'real_percentage',
            'phase',
            'status',
            'estatus',
        ]
        widgets = {
            'code': forms.TextInput(attrs={'class': 'modal-form-input', 'placeholder': 'Ej. VPIT-2024001'}),
            'name': forms.TextInput(attrs={'class': 'modal-form-input', 'placeholder': 'Nombre del proyecto'}),
            'description': forms.Textarea(attrs={'class': 'modal-form-input', 'rows': 3, 'placeholder': 'Descripción detallada...'}),
            'objective': forms.Textarea(attrs={'class': 'modal-form-input', 'rows': 2, 'placeholder': 'Objetivo estratégico...'}),
            'owner': forms.Select(attrs={'class': 'modal-form-input form-select'}),
            'assigned_user': forms.Select(attrs={'class': 'modal-form-input form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'modal-form-input', 'type': 'date'}),
            'cut_date': forms.DateInput(attrs={'class': 'modal-form-input', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'modal-form-input', 'type': 'date'}),
            'procura': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'planned_percentage': forms.TextInput(attrs={'class': 'modal-form-input', 'placeholder': '100%'}),
            'real_percentage': forms.TextInput(attrs={'class': 'modal-form-input', 'placeholder': '100%'}),
            'phase': forms.Select(attrs={'class': 'modal-form-input form-select'}),
            'status': forms.Select(attrs={'class': 'modal-form-input form-select'}),
            'estatus': forms.Select(attrs={'class': 'modal-form-input form-select'}),
        }


class DeliverableForm(forms.ModelForm):
    """
    Formulario para agregar y editar entregables de un proyecto.
    """
    class Meta:
        model = Deliverable
        fields = ['title', 'description', 'phase', 'assigned_to', 'due_date', 'progress', 'is_completed']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'modal-form-input', 'placeholder': 'Título del entregable'}),
            'description': forms.Textarea(attrs={'class': 'modal-form-input', 'rows': 2}),
            'phase': forms.Select(attrs={'class': 'modal-form-input form-select'}),
            'assigned_to': forms.Select(attrs={'class': 'modal-form-input form-select'}),
            'due_date': forms.DateInput(attrs={'class': 'modal-form-input', 'type': 'date'}),
            'progress': forms.NumberInput(attrs={'class': 'modal-form-input', 'min': 0, 'max': 100}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ReportFilterForm(forms.Form):
    """
    Formulario para filtrado avanzado de reportes.
    """
    q = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar proyecto...'}))
    phase = forms.ChoiceField(choices=[('', 'Todas')] + Project.PHASE_CHOICES, required=False)
    status = forms.ChoiceField(choices=[('', 'Todos')] + Project.STATUS_CHOICES, required=False)
    estatus = forms.ChoiceField(choices=[('', 'Todos')] + Project.ESTATUS_CHOICES, required=False)
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all(), required=False, empty_label="Todos los usuarios")
    month = forms.ChoiceField(choices=[('', 'Todos')] + [(str(i), f"Mes {i}") for i in range(1, 13)], required=False)
    year = forms.ChoiceField(choices=[('', 'Todos')] + [(str(i), str(i)) for i in range(2021, 2027)], required=False)
