"""
Modelos de Base de Datos para ProjectFlow (Gestor de Proyectos).
Cumple con PEP 8, anotaciones de tipos, campos de auditoría y optimización de índices.
"""

from typing import Any
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Modelo de usuario personalizado que extiende AbstractUser con
    roles específicos de gestión de proyectos, datos corporativos y auditoría.
    """
    ROLE_ADMIN = 'Administrador'
    ROLE_COORDINATOR = 'Coordinador'
    ROLE_PMO = 'PMO'
    ROLE_GUEST = 'Invitado'

    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Administrador'),
        (ROLE_COORDINATOR, 'Coordinador'),
        (ROLE_PMO, 'PMO'),
        (ROLE_GUEST, 'Invitado'),
    ]

    role = models.CharField(
        max_length=25,
        choices=ROLE_CHOICES,
        default=ROLE_COORDINATOR,
        verbose_name="Rol"
    )
    poo = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        verbose_name="POO / Cargo"
    )
    personal_email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Correo Electrónico Personal"
    )
    phone = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        verbose_name="Número de Teléfono"
    )
    avatar_color = models.CharField(
        max_length=20,
        default='#FF5733',
        verbose_name="Color de Avatar"
    )
    failed_login_attempts = models.PositiveIntegerField(
        default=0,
        verbose_name="Intentos Fallidos de Inicio de Sesión"
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['first_name', 'last_name', 'username']

    def __str__(self) -> str:
        full_name = self.get_full_name()
        return full_name if full_name else self.username

    @property
    def full_name_or_username(self) -> str:
        full_name = self.get_full_name().strip()
        return full_name if full_name else self.username

    @property
    def initials(self) -> str:
        name = self.full_name_or_username
        parts = name.split()
        if len(parts) >= 2:
            return f"{parts[0][0]}{parts[1][0]}".upper()
        return name[:2].upper() if name else "US"

    @property
    def is_admin_role(self) -> bool:
        return self.is_superuser or self.role == self.ROLE_ADMIN

    @property
    def is_pmo_role(self) -> bool:
        return self.role == self.ROLE_PMO or self.is_admin_role

    @property
    def role_badge_class(self) -> str:
        badge_map = {
            self.ROLE_ADMIN: 'badge-admin',
            self.ROLE_COORDINATOR: 'badge-coordinador',
            self.ROLE_PMO: 'badge-pmo',
            self.ROLE_GUEST: 'badge-guest',
        }
        return badge_map.get(self.role, 'badge-pmo')


class Project(models.Model):
    """
    Modelo representativo de un Proyecto en ProjectFlow.
    Incluye identificador oficial, desglose de avance (%Plan, %Real, %Desviación),
    procura, fases, estados y estatus operativos.
    """

    # Definición de Fases
    FACTIBILIZATION = 'Factibilizacion'
    PLANNING = 'Planificacion'
    EXECUTION = 'Ejecucion'
    PHASE_CHOICES = [
        (FACTIBILIZATION, 'Factibilización'),
        (PLANNING, 'Planificación'),
        (EXECUTION, 'Ejecución'),
    ]

    # Definición de Estados
    ACTIVE = 'Activo'
    REPLANNED = 'Re-planificado'
    RESCHEDULED = 'Reprogramado'
    PAUSED = 'Pausado'
    CANCELLED = 'Cancelado'
    CLOSING = 'En cierre'
    COMPLETED = 'Culminado'
    PAP_OK = 'PAP OK'
    STATUS_CHOICES = [
        (ACTIVE, 'Activo'),
        (REPLANNED, 'Re-planificado'),
        (RESCHEDULED, 'Reprogramado'),
        (PAUSED, 'Pausado'),
        (CANCELLED, 'Cancelado'),
        (CLOSING, 'En cierre'),
        (COMPLETED, 'Culminado'),
        (PAP_OK, 'PAP OK'),
    ]

    # Definición de Estatus
    PLAN_IN_CONSTRUCTION = 'Plan en Construcción'
    NOT_STARTED = 'Por iniciar'
    AHEAD = 'Adelantado'
    ON_TIME = 'A tiempo'
    ALERT = 'En alerta'
    RISK = 'En riesgo'
    SUSPENDED = 'Suspendido'
    NO_PLAN = 'Sin plan'
    NO_INDICATOR = 'Sin indicador'
    CLOSED = 'Cerrado'
    CANCELLED_STATUS = 'Cancelado'
    ESTATUS_CHOICES = [
        (PLAN_IN_CONSTRUCTION, 'Plan en Construcción'),
        (NOT_STARTED, 'Por iniciar'),
        (AHEAD, 'Adelantado'),
        (ON_TIME, 'A tiempo'),
        (ALERT, 'En alerta'),
        (RISK, 'En riesgo'),
        (SUSPENDED, 'Suspendido'),
        (NO_PLAN, 'Sin plan'),
        (NO_INDICATOR, 'Sin indicador'),
        (CLOSED, 'Cerrado'),
        (CANCELLED_STATUS, 'Cancelado'),
    ]

    # Identificación y descripción
    code = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        db_index=True,
        verbose_name="ID / Código de Proyecto"
    )
    name = models.CharField(
        max_length=200,
        verbose_name="Nombre del Proyecto"
    )
    description = models.TextField(
        blank=True,
        default="",
        verbose_name="Descripción del Proyecto"
    )
    objective = models.TextField(
        blank=True,
        default="",
        verbose_name="Objetivo del Proyecto"
    )

    # Participantes y Auditoría
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='owned_projects',
        verbose_name="Líder / Propietario"
    )
    assigned_user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name='assigned_projects',
        null=True,
        blank=True,
        verbose_name="Usuario Asignado"
    )

    # Fechas
    start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de Inicio"
    )
    cut_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de Corte"
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de Culminación"
    )

    # Operatividad y Avance
    procura = models.BooleanField(
        default=False,
        verbose_name="Procura"
    )
    real_percentage = models.CharField(
        max_length=10,
        default="0%",
        verbose_name="% Real"
    )
    planned_percentage = models.CharField(
        max_length=10,
        default="0%",
        verbose_name="% Plan"
    )
    deviation = models.CharField(
        max_length=10,
        blank=True,
        default="0%",
        verbose_name="% Desviación"
    )

    # Clasificaciones
    phase = models.CharField(
        max_length=25,
        choices=PHASE_CHOICES,
        default=FACTIBILIZATION,
        db_index=True,
        verbose_name="Fase"
    )
    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        default=ACTIVE,
        db_index=True,
        verbose_name="Estado"
    )
    estatus = models.CharField(
        max_length=30,
        choices=ESTATUS_CHOICES,
        default=NOT_STARTED,
        db_index=True,
        verbose_name="Estatus"
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        ordering = ['-created_at']

    def __str__(self) -> str:
        display_code = f"[{self.code}] " if self.code else ""
        return f"{display_code}{self.name}"

    @property
    def display_id(self) -> str:
        return self.code if self.code else f"PRJ-{self.id:04d}"

    @property
    def real_pct_number(self) -> int:
        val = str(self.real_percentage).replace('%', '').strip()
        try:
            return int(val)
        except ValueError:
            return 0

    @property
    def planned_pct_number(self) -> int:
        val = str(self.planned_percentage).replace('%', '').strip()
        try:
            return int(val)
        except ValueError:
            return 0

    def save(self, *args: Any, **kwargs: Any) -> None:
        # Normalizar porcentajes y calcular desviación automáticamente
        def clean_val(v: Any) -> int:
            if not v:
                return 0
            clean_str = str(v).replace('%', '').strip()
            try:
                return int(clean_str)
            except ValueError:
                return 0

        real_num = clean_val(self.real_percentage)
        plan_num = clean_val(self.planned_percentage)
        dev_num = real_num - plan_num

        self.real_percentage = f"{real_num}%"
        self.planned_percentage = f"{plan_num}%"
        self.deviation = f"{dev_num}%"

        if not self.code:
            self.code = f"VPIT-2024{self.id or 1000 + (Project.objects.count() if Project.objects.exists() else 1):04d}"

        super().save(*args, **kwargs)


class Deliverable(models.Model):
    """
    Entregable asociado a un Proyecto, permitiendo granularidad
    en Factibilización, Planificación y Ejecución.
    """
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='deliverables',
        verbose_name="Proyecto"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Título del Entregable"
    )
    description = models.TextField(
        blank=True,
        default="",
        verbose_name="Descripción"
    )
    phase = models.CharField(
        max_length=25,
        choices=Project.PHASE_CHOICES,
        default=Project.FACTIBILIZATION,
        verbose_name="Fase"
    )
    assigned_to = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_deliverables',
        verbose_name="Responsable"
    )
    due_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha Límite"
    )
    progress = models.PositiveIntegerField(
        default=0,
        verbose_name="% Avance"
    )
    is_completed = models.BooleanField(
        default=False,
        verbose_name="Completado"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Entregable"
        verbose_name_plural = "Entregables"
        ordering = ['due_date', 'id']

    def __str__(self) -> str:
        return f"{self.title} ({self.project.name})"


class MonthlyTrend(models.Model):
    """
    Instantánea de comportamiento mensual para métricas históricas
    (Enero - Noviembre / Diciembre).
    """
    month_name = models.CharField(max_length=20)
    month_number = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField(default=2024)
    in_progress = models.PositiveIntegerField(default=0, verbose_name="En Curso")
    paused = models.PositiveIntegerField(default=0, verbose_name="Pausado")
    closing = models.PositiveIntegerField(default=0, verbose_name="En Cierre (PAP OK)")
    completed = models.PositiveIntegerField(default=0, verbose_name="Culminados")
    cancelled = models.PositiveIntegerField(default=0, verbose_name="Cancelado")
    total = models.PositiveIntegerField(default=0, verbose_name="Total")

    class Meta:
        verbose_name = "Tendencia Mensual"
        verbose_name_plural = "Tendencias Mensuales"
        ordering = ['year', 'month_number']

    def __str__(self) -> str:
        return f"{self.month_name} {self.year} (Total: {self.total})"
