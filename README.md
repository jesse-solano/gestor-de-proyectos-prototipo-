# ProjectFlow - Gestor de Proyectos Corporativo (Enterprise PMO)

[![Django](https://img.shields.io/badge/Django-5.0%2B-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Ready-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Chart.js](https://img.shields.io/badge/Chart.js-4.x-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)](https://www.chartjs.org/)

**ProjectFlow** es una plataforma integral de gestión y seguimiento de proyectos corporativos (*Enterprise PMO*) diseñada para centralizar la factibilización, planificación, ejecución y reporte de métricas en tiempo real. 

Este proyecto fue desarrollado bajo arquitectura **Django MVT**, con soporte nativo para **PostgreSQL** y maquetado con base en especificaciones de diseño UI/UX de alta fidelidad.

---

## 🌟 Características Principales

### 1. Módulo de Autenticación y Seguridad
- Inicio de sesión con protección CSRF y seguimiento visual de **intentos fallidos de autenticación**.
- Botón de **Acceso Rápido como Invitado** (`Ingresar como Invitado`) para demostraciones públicas sin riesgo de modificación de datos.
- Variables de entorno aisladas mediante `python-dotenv` y gestión de secretos con `.env`.

### 2. Control de Acceso Basado en Roles (RBAC)
- **Administrador:** Gestión total de usuarios, roles, proyectos, copias de seguridad JSON y restauración del sistema.
- **Coordinador:** Asignación de recursos, gestión de entregables por fases y actualización de avance en lote.
- **PMO / Auditor:** Análisis estratégico, visualización de tableros consolidados y descarga de informes CSV.
- **Invitado:** Modo demostración con acceso de lectura a métricas y proyectos.

### 3. Gestión y Seguimiento de Proyectos
- Listado con ordenamiento dinámico por ID, Nombre y Fecha de Inicio.
- Búsqueda en tiempo real y paginación configurable (5, 10, 25 filas).
- Menú contextual de acciones por proyecto:
  - *Agregar / Modificar / Eliminar Entregables*.
  - *Asignación y desasignación de responsables*.
  - *Ficha modal de detalles ejecutivos*.
- Exportación de **Copia de Seguridad** en JSON y **Restauración** con un solo clic.

### 4. Módulo de Actualización Operativa
- Tabla de seguimiento rápido con switches de **Procura** (*Sí / No*).
- Cálculo automático de desviación (`% Desviación = % Real - % Plan`).
- Selectores en línea para transición de Fases (*Factibilización, Planificación, Ejecución*), Estados y Estatus operativos.

### 5. Dashboards y Reportes Analíticos
- **Temporizador regresivo dinámico:** *Tiempo restante para el corte* (cuenta regresiva en vivo).
- Filtros interactivos tipo cápsula por **Líderes, Fases, Estados, Estatus, PMO, Mes y Año**.
- Tablas estadísticas consolidadas con totales automáticos.
- Gráficos interactivos construidos con **Chart.js**:
  - Gráfico de barras por fase.
  - Gráfico circular / donut de distribución.
  - Diagrama mensual multivariable: *Comportamiento Enero - Noviembre* (En curso, Pausado, En cierre, Culminados, Cancelados y Curva total).
- Exportación instantánea de informe a formato CSV.

---

## 🚀 Puesta en Marcha Rápida (Desarrollo Local)

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/gestor-de-proyectos.git
cd gestor-de-proyectos
```

### 2. Crear y activar el entorno virtual
Con `uv` (recomendado por velocidad):
```bash
uv venv .venv --python 3.12
.venv\Scripts\activate      # En Windows
# source .venv/bin/activate  # En Linux/macOS
```

O con Python estándar:
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Copia la plantilla de ejemplo y ajusta los valores:
```bash
cp .env.example .env
```
> *Por defecto, `.env` está configurado para utilizar SQLite en desarrollo local inmediato sin requerir configuración previa de bases de datos externas.*

Para conectar con **PostgreSQL**, configura en tu `.env`:
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=projectflow_db
DB_USER=postgres
DB_PASSWORD=tu_contraseña
DB_HOST=127.0.0.1
DB_PORT=5432
```

### 5. Aplicar migraciones
```bash
python manage.py migrate
```

### 6. Poblar datos de demostración
Ejecuta el comando de sembrado para cargar los 58 proyectos, usuarios y tendencias mensuales idénticos a la presentación:
```bash
python manage.py seed_data
```

### 7. Iniciar el servidor
```bash
python manage.py runserver
```

Abre tu navegador en [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

## 🔑 Credenciales de Acceso Demo

| Rol | Usuario | Contraseña | Nombre Completo | Acceso Directo |
| :--- | :--- | :--- | :--- | :--- |
| **Administrador** | `admin` | `admin123` | Ali Angulo | Control total, gestión de usuarios y proyectos |
| **Coordinador** | `chinn` | `user123` | Vo Van Chinh | Actualización de proyectos y entregables |
| **PMO** | `thu` | `user123` | Nguyen Thi Thu | Supervisión, tableros y descarga de informes |
| **Invitado** | *N/A* | *N/A* | — | Botón `"Ingresar como Invitado"` en pantalla de login |


---

## 📂 Estructura del Proyecto

```plaintext
Gestor_de_Proyectos/
├── .env.example                  # Plantilla de variables de entorno
├── .gitignore                    # Exclusiones de control de versiones
├── AGENTS.md                     # Reglas de codificación para asistentes de IA
├── README.md                     # Documentación principal del repositorio
├── requirements.txt              # Dependencias de producción
├── manage.py                     # Entrypoint de Django
├── pasantias_proyecto/           # Módulo de configuración global
│   ├── settings.py               # Configuración desacoplada con python-dotenv
│   ├── urls.py                   # Enrutamiento general
│   └── wsgi.py                   # Despliegue WSGI
├── admin_user/                   # Aplicación principal (ProjectFlow)
│   ├── admin.py                  # Personalización del Admin de Django
│   ├── forms.py                  # Formularios con validación estricta
│   ├── models.py                 # CustomUser, Project, Deliverable, MonthlyTrend
│   ├── views.py                  # Controladores optimizados (ORM select_related)
│   ├── urls.py                   # Rutas de la aplicación
│   ├── management/commands/      # Comando seed_data para población demo
│   └── templates/admin_user/     # Plantillas HTML con diseño fiel al PDF
│       ├── base.html             # Shell maestro con Bootstrap 5
│       ├── sidebar.html          # Barra lateral con indicador verde neón
│       ├── login.html            # Login con contador de intentos
│       ├── home.html             # Bienvenida y tarjetas de métricas
│       ├── user_list.html        # Gestión de usuarios con modales
│       ├── project_list.html     # Tabla de proyectos, respaldo y restauración
│       ├── project_actualizar.html # Tabla de avance, procura y estatus
│       └── report.html           # Reportes, conteos y gráficos Chart.js
├── docs/                         # Documentación de arquitectura
│   └── architecture-and-best-practices.md
└── static/                       # Recursos estáticos
    ├── css/projectflow.css       # Estilos corporativos maestros
    └── images/                   # Logotipos vectoriales SVG
```

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
