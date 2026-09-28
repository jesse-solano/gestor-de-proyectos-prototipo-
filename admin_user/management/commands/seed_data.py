import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from admin_user.models import CustomUser, Project, Deliverable, MonthlyTrend


class Command(BaseCommand):
    help = 'Puebla la base de datos con los datos de referencia profesionales de ProjectFlow basados en el PDF'

    def handle(self, *args, **kwargs):
        self.stdout.write("Iniciando sembrado de datos de demostración ProjectFlow...")

        # 1. Crear usuarios clave
        users_data = [
            {
                'username': 'admin',
                'first_name': 'Ali',
                'last_name': 'Angulo',
                'email': 'ali.angulo@projectflow.com',
                'personal_email': 'ali.angulo@gmail.com',
                'phone': '+58 416-5550101',
                'poo': 'Gerencia de TI y Sistemas',
                'role': CustomUser.ROLE_ADMIN,
                'avatar_color': '#EF4444',
                'is_staff': True,
                'is_superuser': True,
            },
            {
                'username': 'vohieusinh',
                'first_name': 'Vo',
                'last_name': 'Hieu Sinh',
                'email': 'sinh@gmail.com',
                'personal_email': 'sinh.personal@gmail.com',
                'phone': '+58 416-5550102',
                'poo': 'Infraestructura Tecnológica',
                'role': CustomUser.ROLE_ADMIN,
                'avatar_color': '#F87171',
                'is_staff': True,
                'is_superuser': False,
            },
            {
                'username': 'kuroi',
                'first_name': 'Nguyen',
                'last_name': 'Van Roi',
                'email': 'kuroi@gmail.com',
                'personal_email': 'kuroi.dev@gmail.com',
                'phone': '+58 416-5550103',
                'poo': 'Desarrollo de Soluciones',
                'role': CustomUser.ROLE_ADMIN,
                'avatar_color': '#DC2626',
                'is_staff': True,
                'is_superuser': False,
            },
            {
                'username': 'chinn',
                'first_name': 'Vo',
                'last_name': 'Van Chinh',
                'email': 'chinn@gmail.com',
                'personal_email': 'chinn.priv@gmail.com',
                'phone': '+58 416-5550104',
                'poo': 'Coordinación de Interconexión',
                'role': CustomUser.ROLE_COORDINATOR,
                'avatar_color': '#38BDF8',
                'is_staff': False,
                'is_superuser': False,
            },
            {
                'username': 'ninh',
                'first_name': 'Pham',
                'last_name': 'TT Ninh',
                'email': 'ninh@gmail.com',
                'personal_email': 'ninh.personal@gmail.com',
                'phone': '+58 416-5550105',
                'poo': 'Coordinación de Operaciones Web',
                'role': CustomUser.ROLE_COORDINATOR,
                'avatar_color': '#0EA5E9',
                'is_staff': False,
                'is_superuser': False,
            },
            {
                'username': 'thu',
                'first_name': 'Cao',
                'last_name': 'Thi Minh Thu',
                'email': 'thu@gmail.com',
                'personal_email': 'thu.pm@gmail.com',
                'phone': '+58 416-5550106',
                'poo': 'Oficina de Gestión de Proyectos (PMO)',
                'role': CustomUser.ROLE_PMO,
                'avatar_color': '#64748B',
                'is_staff': False,
                'is_superuser': False,
            },
            {
                'username': 'ngoc',
                'first_name': 'Ng',
                'last_name': 'Do Bao Ngoc',
                'email': 'ngoc@gmail.com',
                'personal_email': 'ngoc.mail@gmail.com',
                'phone': '+58 416-5550107',
                'poo': 'Especialista PMO y Calidad',
                'role': CustomUser.ROLE_PMO,
                'avatar_color': '#94A3B8',
                'is_staff': False,
                'is_superuser': False,
            },
            {
                'username': 'bnghi',
                'first_name': 'P N',
                'last_name': 'Bang Nghi',
                'email': 'bnghi@gmail.com',
                'personal_email': 'bnghi.work@gmail.com',
                'phone': '+58 416-5550108',
                'poo': 'Planificación Estratégica PMO',
                'role': CustomUser.ROLE_PMO,
                'avatar_color': '#475569',
                'is_staff': False,
                'is_superuser': False,
            },
            {
                'username': 'vnmk',
                'first_name': 'Vu',
                'last_name': 'N M Khuyen',
                'email': 'vnmk@mail.com',
                'personal_email': 'khuyen.pmo@mail.com',
                'phone': '+58 416-5550109',
                'poo': 'Analista de Métricas PMO',
                'role': CustomUser.ROLE_PMO,
                'avatar_color': '#6B7280',
                'is_staff': False,
                'is_superuser': False,
            },
            {
                'username': 'invitado',
                'first_name': 'Usuario',
                'last_name': 'Invitado',
                'email': 'invitado@projectflow.dev',
                'personal_email': 'guest@projectflow.dev',
                'phone': '+58 400-0000000',
                'poo': 'Visitante Público',
                'role': CustomUser.ROLE_GUEST,
                'avatar_color': '#10B981',
                'is_staff': False,
                'is_superuser': False,
            },
        ]

        created_users = {}
        for u in users_data:
            user, created = CustomUser.objects.get_or_create(
                username=u['username'],
                defaults={
                    'first_name': u['first_name'],
                    'last_name': u['last_name'],
                    'email': u['email'],
                    'personal_email': u['personal_email'],
                    'phone': u['phone'],
                    'poo': u['poo'],
                    'role': u['role'],
                    'avatar_color': u['avatar_color'],
                    'is_staff': u['is_staff'],
                    'is_superuser': u['is_superuser'],
                    'last_login': timezone.now() - datetime.timedelta(days=1),
                }
            )
            # Contraseña por defecto para pruebas: admin123 para admin, user123 para otros
            pwd = 'admin123' if u['username'] == 'admin' else 'user123'
            user.set_password(pwd)
            user.role = u['role']
            user.poo = u['poo']
            user.personal_email = u['personal_email']
            user.phone = u['phone']
            user.avatar_color = u['avatar_color']
            user.save()
            created_users[u['username']] = user

        admin_user = created_users['admin']
        chinn_user = created_users['chinn']
        ninh_user = created_users['ninh']
        thu_pmo = created_users['thu']

        # 2. Proyectos principales vistos en el PDF
        primary_projects = [
            {
                'code': 'VPIT-20210535',
                'name': 'Sistema de Interconexión Operadores Locales - Fase I',
                'description': 'Modernización de enlace y protocolos de interconexión con operadores de telecomunicaciones nacionales.',
                'objective': 'Garantizar el enrutamiento bidireccional y monitoreo de tráfico en tiempo real.',
                'start_date': datetime.date(2021, 10, 5),
                'procura': True,
                'planned_percentage': '100%',
                'real_percentage': '100%',
                'phase': Project.EXECUTION,
                'status': Project.COMPLETED,
                'estatus': 'Cerrado',
                'owner': admin_user,
                'assigned_user': chinn_user,
            },
            {
                'code': 'VPIT-20230336',
                'name': 'Repositorio Xius "Pospago"',
                'description': 'Consolidación de base de datos transaccional para clientes corporativos y planes pospago.',
                'objective': 'Optimizar tiempos de facturación y consulta de estados de cuenta.',
                'start_date': datetime.date(2023, 3, 3),
                'procura': True,
                'planned_percentage': '100%',
                'real_percentage': '100%',
                'phase': Project.EXECUTION,
                'status': Project.COMPLETED,
                'estatus': 'Cerrado',
                'owner': admin_user,
                'assigned_user': chinn_user,
            },
            {
                'code': 'VPIT-20210215',
                'name': 'Larga Distancia Internacional',
                'description': 'Ampliación de capacidad para troncales de señalización y gateways internacionales.',
                'objective': 'Expandir cobertura y resiliencia en llamadas internacionales salientes.',
                'start_date': datetime.date(2021, 10, 21),
                'procura': True,
                'planned_percentage': '99%',
                'real_percentage': '98%',
                'phase': Project.EXECUTION,
                'status': Project.CLOSING,
                'estatus': 'A tiempo',
                'owner': admin_user,
                'assigned_user': ninh_user,
            },
            {
                'code': 'VPIT-20240361',
                'name': 'Sistema de Autogestión a través de la Web - Fase II',
                'description': 'Plataforma responsive de autogestión de usuarios y servicios en línea.',
                'objective': 'Reducir el volumen de solicitudes presenciales mediante canal digital omnicanal.',
                'start_date': datetime.date(2024, 3, 6),
                'procura': True,
                'planned_percentage': '99%',
                'real_percentage': '97%',
                'phase': Project.EXECUTION,
                'status': Project.CLOSING,
                'estatus': 'A tiempo',
                'owner': admin_user,
                'assigned_user': ninh_user,
            },
            {
                'code': 'VPIT-202306101',
                'name': 'Comedor Fase III Sede Amoca',
                'description': 'Adecuación de infraestructura técnica y cableado estructurado para sede corporativa.',
                'objective': 'Completar redes de voz, datos y puntos de acceso WiFi para el personal.',
                'start_date': datetime.date(2023, 6, 10),
                'procura': True,
                'planned_percentage': '98%',
                'real_percentage': '98%',
                'phase': Project.EXECUTION,
                'status': Project.CLOSING,
                'estatus': 'A tiempo',
                'owner': admin_user,
                'assigned_user': chinn_user,
            },
            {
                'code': 'VPIT-202309210',
                'name': 'Implementación de SIM-X',
                'description': 'Despliegue tecnológico de aprovisionamiento de tarjetas SIM virtuales y físicas de alta velocidad.',
                'objective': 'Habilitar activación digital instantánea de líneas móviles.',
                'start_date': datetime.date(2023, 9, 21),
                'procura': False,
                'planned_percentage': '81%',
                'real_percentage': '81%',
                'phase': Project.EXECUTION,
                'status': Project.ACTIVE,
                'estatus': 'A tiempo',
                'owner': admin_user,
                'assigned_user': ninh_user,
            },
        ]

        # Borrar proyectos previos si se desea resetear ordenadamente
        Project.objects.all().delete()

        for p_data in primary_projects:
            p = Project.objects.create(**p_data)
            # Agregar entregables de muestra
            Deliverable.objects.create(
                project=p,
                title="Estudio de Factibilidad Técnica",
                phase=Project.FACTIBILIZATION,
                assigned_to=p.assigned_user,
                progress=100,
                is_completed=True,
                due_date=p.start_date
            )
            Deliverable.objects.create(
                project=p,
                title="Documentación de Arquitectura y Diseño",
                phase=Project.PLANNING,
                assigned_to=p.assigned_user,
                progress=100,
                is_completed=True,
                due_date=p.start_date
            )
            Deliverable.objects.create(
                project=p,
                title="Despliegue y Pruebas Piloto",
                phase=Project.EXECUTION,
                assigned_to=p.assigned_user,
                progress=p.real_pct_number,
                is_completed=(p.real_pct_number == 100),
                due_date=p.start_date
            )

        # 3. Completar hasta 57 proyectos para coincidir exactamente con el desglose del PDF:
        # Fases objetivo: Factibilización = 16, Planificación = 3, Ejecución = 38 (Total: 57)
        # Estados objetivo: Activo=20, Re-planificado=2, Reprogramado=3, Pausado=3, Cancelado=3, En cierre=1, Culminado=17, PAP OK=1 (Total: 57)
        # Estatus objetivo: Plan en Construcción=6, Por iniciar=1, Adelantado=0, A tiempo=19, En alerta=5, En riesgo=3, Suspendido=3, Sin plan=0, Cerrado=17, Cancelado=3, Sin indicador=0 (Total: 57)

        # Ya tenemos 6 proyectos de Ejecución (2 Culminado/Cerrado, 3 En cierre/A tiempo, 1 Activo/A tiempo).
        # Agreguemos los 51 proyectos restantes con combinaciones precisas:
        target_distribution = [
            # 16 Factibilización:
            # - Plan en Construcción (6)
            *[(Project.FACTIBILIZATION, Project.ACTIVE, 'Plan en Construcción', 15, 10, False) for _ in range(6)],
            # - Por iniciar (1)
            (Project.FACTIBILIZATION, Project.ACTIVE, 'Por iniciar', 0, 0, False),
            # - En alerta (3)
            *[(Project.FACTIBILIZATION, Project.ACTIVE, 'En alerta', 35, 20, False) for _ in range(3)],
            # - En riesgo (2)
            *[(Project.FACTIBILIZATION, Project.REPLANNED, 'En riesgo', 40, 25, False) for _ in range(2)],
            # - Suspendido (2)
            *[(Project.FACTIBILIZATION, Project.PAUSED, 'Suspendido', 20, 20, False) for _ in range(2)],
            # - Cancelado (2)
            *[(Project.FACTIBILIZATION, Project.CANCELLED, 'Cancelado', 10, 5, False) for _ in range(2)],

            # 3 Planificación:
            # - A tiempo (2)
            *[(Project.PLANNING, Project.ACTIVE, 'A tiempo', 50, 50, False) for _ in range(2)],
            # - En alerta (1)
            (Project.PLANNING, Project.RESCHEDULED, 'En alerta', 60, 45, False),

            # 32 Ejecución adicionales (para llegar a 38):
            # - Culminados / Cerrados (15 adicionales para totalizar 17 Culminados y 17 Cerrados)
            *[(Project.EXECUTION, Project.COMPLETED, 'Cerrado', 100, 100, True) for _ in range(15)],
            # - PAP OK (1)
            (Project.EXECUTION, Project.PAP_OK, 'A tiempo', 95, 95, True),
            # - Activos / A tiempo (10)
            *[(Project.EXECUTION, Project.ACTIVE, 'A tiempo', 80, 80, True) for _ in range(10)],
            # - Reprogramados / En alerta (1)
            (Project.EXECUTION, Project.RESCHEDULED, 'En alerta', 75, 60, False),
            # - Reprogramados / En riesgo (1)
            (Project.EXECUTION, Project.RESCHEDULED, 'En riesgo', 80, 60, False),
            # - Pausados / Suspendido (1)
            (Project.EXECUTION, Project.PAUSED, 'Suspendido', 65, 65, False),
            # - Cancelados / Cancelado (1)
            (Project.EXECUTION, Project.CANCELLED, 'Cancelado', 40, 20, False),
            # - A tiempo activos restantes (3)
            *[(Project.EXECUTION, Project.ACTIVE, 'A tiempo', 90, 88, True) for _ in range(3)],
        ]

        project_names_pool = [
            "Actualización Plataforma Core GSM", "Migración de Enlaces Satelitales Sede Guayana",
            "Monitoreo NOC Fibra Óptica Troncal Centro", "Integración Pasarela de Pagos Móvil",
            "Automatización de Aprovisionamiento HLR/HSS", "Despliegue Celdas Microondas Rurales",
            "Portal Corporativo de Autoservicio B2B", "Renovación Parque Servidores Blade",
            "Cluster de Virtualización VMWare - Sede Norte", "Centralización de Logs SIEM y Ciberseguridad",
            "Modernización Sistema IVR de Atención al Cliente", "Migración Base de Datos Oracle a PostgreSQL",
            "Reingeniería de Enlaces Microondas Zona Andina", "Implementación Red SD-WAN Oficinas Comerciales",
            "Plataforma de Facturación Mayorista de Tráfico", "Plan de Contingencia y Recuperación ante Desastres (DRP)",
            "Optimización de Cobertura 4G LTE Sector Amoca", "Adecuación Energética UPS Subestaciones",
            "Sistema de Monitoreo Ambiental en Nodos de Red", "Gestión Integral de Flotas y Logística",
            "Actualización Licencias Firewall Perimetral", "Digitalización de Contratos Corporativos",
            "Sistema de Detección de Fraude en Voz IP", "Plataforma de Notificaciones Masivas SMS",
            "Adecuación Climatización Centro de Datos Principal", "Interconexión Troncales SIP Internacionales",
            "Auditoría de Vulnerabilidades y Pentesting Anual", "Automatización de Conciliación Bancaria",
            "Migración Sistema de Gestión de Tickets HelpDesk", "Optimización de Conectividad Roaming Internacional",
            "Despliegue de Fibra Óptica Hasta la Antena (FTTA)", "Renovación Equipamiento Cisco Capa de Distribución",
            "Ampliación Ancho de Banda Enlaces Submarinos", "Sistema de Control de Acceso Biométrico DataCenter",
            "Plataforma de Inteligencia de Negocios y KPI", "Gestión Centralizada de Direcciones IP (IPAM)",
            "Actualización de Servidores DNS y DHCP", "Automatización de Respaldos de Configuraciones de Red",
            "Plataforma de Capacitación y Gestión de Talento", "Monitoreo de Calidad de Servicio QoS en Tiempo Real",
            "Mesa de Ayuda para Soporte Técnico 24/7", "Integración API Servicios Terceros Fintech",
            "Sustitución de Baterías de Respaldo Nodos Críticos", "Rediseño de Portal Interno de Colaboradores",
            "Despliegue Protocolo IPv6 en Red Troncal", "Sistema de Inventario de Activos de Telecomunicaciones",
            "Modernización de Centrales Telefónicas IP", "Auditoría de Seguridad según Norma ISO 27001",
            "Integración de Mensajería Push para Clientes", "Módulo de Facturación Electrónica Fiscal",
            "Ampliación Capacidad Servidores DNS Cache"
        ]

        user_pool = [chinn_user, ninh_user, thu_pmo, admin_user]
        base_date = datetime.date(2023, 1, 15)

        for i, (fase, estado, estatus, plan_pct, real_pct, proc) in enumerate(target_distribution):
            name = project_names_pool[i % len(project_names_pool)]
            assigned = user_pool[i % len(user_pool)]
            code_num = 20230000 + i + 10
            proj_date = base_date + datetime.timedelta(days=(i * 12) % 365)
            
            p = Project.objects.create(
                code=f"VPIT-{code_num}",
                name=f"{name} (Lote {i+1})",
                description=f"Iniciativa técnica estratégica orientada a la fase de {fase}.",
                objective="Cumplir los hitos del cronograma anual y elevar la disponibilidad de servicios.",
                start_date=proj_date,
                cut_date=proj_date + datetime.timedelta(days=90),
                end_date=proj_date + datetime.timedelta(days=180),
                procura=proc,
                planned_percentage=f"{plan_pct}%",
                real_percentage=f"{real_pct}%",
                phase=fase,
                status=estado,
                estatus=estatus,
                owner=admin_user,
                assigned_user=assigned
            )
            Deliverable.objects.create(
                project=p,
                title="Hito Operativo Principal",
                phase=fase,
                assigned_to=assigned,
                progress=real_pct,
                is_completed=(real_pct == 100),
                due_date=proj_date + datetime.timedelta(days=60)
            )

        # 4. Tendencias mensuales (Enero a Noviembre) exactamente como el gráfico del PDF (Page 12 y 17)
        MonthlyTrend.objects.all().delete()
        monthly_mockup_data = [
            {'month_name': 'Enero', 'month_number': 1, 'in_progress': 17, 'paused': 2, 'closing': 5, 'completed': 0, 'cancelled': 0, 'total': 24},
            {'month_name': 'Febrero', 'month_number': 2, 'in_progress': 14, 'paused': 6, 'closing': 4, 'completed': 0, 'cancelled': 0, 'total': 24},
            {'month_name': 'Marzo', 'month_number': 3, 'in_progress': 12, 'paused': 7, 'closing': 5, 'completed': 1, 'cancelled': 0, 'total': 25},
            {'month_name': 'Abril', 'month_number': 4, 'in_progress': 14, 'paused': 7, 'closing': 4, 'completed': 1, 'cancelled': 0, 'total': 26},
            {'month_name': 'Mayo', 'month_number': 5, 'in_progress': 15, 'paused': 6, 'closing': 4, 'completed': 2, 'cancelled': 0, 'total': 27},
            {'month_name': 'Junio', 'month_number': 6, 'in_progress': 14, 'paused': 7, 'closing': 4, 'completed': 2, 'cancelled': 0, 'total': 27},
            {'month_name': 'Julio', 'month_number': 7, 'in_progress': 15, 'paused': 4, 'closing': 8, 'completed': 3, 'cancelled': 0, 'total': 30},
            {'month_name': 'Agosto', 'month_number': 8, 'in_progress': 14, 'paused': 4, 'closing': 9, 'completed': 3, 'cancelled': 0, 'total': 30},
            {'month_name': 'Septiembre', 'month_number': 9, 'in_progress': 15, 'paused': 4, 'closing': 9, 'completed': 3, 'cancelled': 0, 'total': 31},
            {'month_name': 'Octubre', 'month_number': 10, 'in_progress': 15, 'paused': 4, 'closing': 8, 'completed': 6, 'cancelled': 0, 'total': 33},
            {'month_name': 'Noviembre', 'month_number': 11, 'in_progress': 15, 'paused': 3, 'closing': 3, 'completed': 12, 'cancelled': 2, 'total': 35},
        ]

        for m in monthly_mockup_data:
            MonthlyTrend.objects.create(year=2024, **m)

        self.stdout.write(self.style.SUCCESS(
            f"¡Datos sembrados exitosamente! Proyectos: {Project.objects.count()}, Usuarios: {CustomUser.objects.count()}, Tendencias: {MonthlyTrend.objects.count()}"
        ))
