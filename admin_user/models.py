# Importa AbstractUser para crear un modelo de usuario personalizado
from django.contrib.auth.models import AbstractUser
# Importa models para definir modelos de base de datos
from django.db import models

# Define tus modelos aquí.

# Modelo de usuario personalizado que hereda de AbstractUser
class CustomUser(AbstractUser):
    pass


# Modelo para el proyecto
class Project(models.Model):
    # Campos existentes
    name = models.CharField(max_length=100)  # Nombre del proyecto
    description = models.TextField()  # Descripción del proyecto
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación del proyecto
    updated_at = models.DateTimeField(auto_now=True)  # Fecha de última actualización del proyecto
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='owned_projects')  # Propietario del proyecto
    assigned_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_projects', null=True, blank=True)  # Usuario asignado al proyecto

    procura = models.BooleanField(default=False)  # Campo booleano para el estado de procura
    real_percentage = models.CharField(max_length=10)  # Porcentaje real del progreso del proyecto (almacenado como cadena con '%')
    planned_percentage = models.CharField(max_length=10)  # Nuevo campo para el porcentaje planificado del progreso del proyecto
    deviation = models.CharField(max_length=10, blank=True, default='0%')  # Campo para la desviación del progreso (calculado)

    # Definición de fases del proyecto
    FACTIBILIZATION = 'Factibilizacion'
    PLANNING = 'Planificacion'
    EXECUTION = 'Ejecucion'
    PHASE_CHOICES = [
        (FACTIBILIZATION, 'Factibilizacion'),
        (PLANNING, 'Planificacion'),
        (EXECUTION, 'Ejecucion'),
    ]
    phase = models.CharField(max_length=15, choices=PHASE_CHOICES, default=FACTIBILIZATION)  # Fase actual del proyecto
    
    # Definición de estados del proyecto
    ACTIVE = 'Activo'
    RESCHEDULED = 'Reprogramado'
    REPLANNED = 'Replanificado'
    PAUSED = 'Pausado'
    CLOSING = 'En cierre'
    COMPLETED = 'Culminado'
    CANCELLED = 'Cancelado'
    STATUS_CHOICES = [
        (ACTIVE, 'Activo'),
        (RESCHEDULED, 'Reprogramado'),
        (REPLANNED, 'Replanificado'),
        (PAUSED, 'Pausado'),
        (CLOSING, 'En cierre'),
        (COMPLETED, 'Culminado'),
        (CANCELLED, 'Cancelado'),
    ]
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=ACTIVE)  # Estado actual del proyecto
    
    # Definición de estatus del proyecto
    NOT_STARTED = 'Por iniciar'
    PEC = 'P.E.C'
    AHEAD = 'Adelantado'
    ON_TIME = 'A tiempo'
    ALERT = 'En alerta'
    RISK = 'En riesgo'
    SUSPENDED = 'Suspendido'
    CLOSED = 'Cerrado'
    CANCELLED_STATUS = 'Cancelado'
    ESTATUS_CHOICES = [
        (NOT_STARTED, 'Por iniciar'),
        (PEC, 'P.E.C'),
        (AHEAD, 'Adelantado'),
        (ON_TIME, 'A tiempo'),
        (ALERT, 'En alerta'),
        (RISK, 'En riesgo'),
        (SUSPENDED, 'Suspendido'),
        (CLOSED, 'Cerrado'),
        (CANCELLED_STATUS, 'Cancelado'),
    ]
    estatus = models.CharField(max_length=15, choices=ESTATUS_CHOICES, default=NOT_STARTED)  # Estatus actual del proyecto

    # Método para representar el proyecto como una cadena (el nombre del proyecto)
    def __str__(self):
        return self.name
    
    # Método para guardar el proyecto
    def save(self, *args, **kwargs):
        # Calcular la desviación antes de guardar
        real = int(self.real_percentage.strip('%'))  # Convierte el porcentaje real a entero
        planned = int(self.planned_percentage.strip('%'))  # Convierte el porcentaje planificado a entero
        self.deviation = f"{real - planned}%"  # Calcula la desviación y la guarda como cadena con '%'
        super(Project, self).save(*args, **kwargs)  # Llama al método save() de la clase base
