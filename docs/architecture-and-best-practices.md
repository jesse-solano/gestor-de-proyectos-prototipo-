# Arquitectura del Sistema y Guía de Buenas Prácticas - ProjectFlow

**ProjectFlow** es una solución corporativa de gestión y seguimiento de proyectos (*Enterprise PMO*) desarrollada con el framework web **Django** y preparada para bases de datos relacionales de alto rendimiento como **PostgreSQL**.

Este documento detalla los patrones de diseño, directrices de seguridad, optimización de base de datos y principios de experiencia de usuario implementados para exhibición en repositorios profesionales de GitHub.

---

## 1. Patrones de Diseño Implementados

### 1.1 Patrón MVT (Model - View - Template)
La arquitectura sigue la separación de responsabilidades canónica de Django:
- **Modelos (`models.py`):** Define el esquema relacional (`CustomUser`, `Project`, `Deliverable`, `MonthlyTrend`), encapsulando la integridad de datos, métodos de cálculo automático de desviación (`%Real - %Plan`) y campos de auditoría.
- **Vistas (`views.py`):** Controladores desacoplados que procesan peticiones HTTP, validan permisos mediante decoradores RBAC, ejecutan agregaciones en base de datos y preparan el contexto para renderizado o serialización JSON/CSV.
- **Plantillas (`templates/`):** Estructura visual basada en herencia modular (`base.html` -> `sidebar.html` -> vistas hijas), garantizando consistencia estética con cero duplicación de marcado.

### 1.2 Separación de Lógica de Negocio y Formularios
- Los formularios de entrada (`forms.py`) encapsulan validaciones complejas:
  - Formatos y límites porcentuales.
  - Reglas estrictas de contraseñas (mínimo 8 caracteres, mayúsculas, minúsculas y caracteres especiales).
  - Sanitización de entradas para prevenir inyecciones.
- Las tareas administrativas o de población de datos se encapsulan en comandos reutilizables (`seed_data.py`), permitiendo restauración instantánea y despliegue continuo sin depender de scripts manuales frágiles.

---

## 2. Manejo de Seguridad y Control de Acceso (RBAC)

### 2.1 Gestión de Secretos y Variables de Entorno
- La configuración sensible del sistema se aísla mediante `python-dotenv`:
  - `SECRET_KEY`: Gestionada por entorno.
  - `DEBUG`: Inactivable de forma trivial en producción (`DEBUG=False`).
  - Credenciales de Base de Datos: Adaptables dinámicamente entre PostgreSQL para producción y SQLite como respaldo de desarrollo local.
- Se incluye `.env.example` versionado para facilitar el onboarding de nuevos desarrolladores sin filtrar secretos reales.

### 2.2 Control de Acceso Basado en Roles (RBAC)
El sistema clasifica a los usuarios en 4 perfiles diferenciados:
1. **Administrador (`ROLE_ADMIN`):**
   - Acceso total a creación, edición, reseteo de contraseñas y bloqueo de cuentas de usuarios.
   - Creación, borrado y asignación de proyectos.
   - Generación de copias de seguridad y restauración del sistema.
2. **Coordinador (`ROLE_COORDINATOR`):**
   - Gestión de proyectos asignados y creación de entregables.
   - Acceso a la tabla de actualización rápida de avances (%Plan, %Real, Procura).
3. **PMO (`ROLE_PMO`):**
   - Supervisión analítica, acceso a tableros ejecutivos, conteos por fases y descarga de informes consolidados.
4. **Invitado (`ROLE_GUEST`):**
   - Perfil de solo lectura con acceso seguro para demostraciones en vivo sin riesgo de alteración o borrado de datos.

### 2.3 Protección contra Ataques Comunes
- **CSRF (Cross-Site Request Forgery):** Protección activa mediante tokens `{% csrf_token %}` en cada formulario POST.
- **XSS (Cross-Site Scripting):** Escape automático de variables en templates de Django y serialización segura con `escapejs`.
- **Ataques de Fuerza Bruta:** Registro y visualización del contador de intentos fallidos de autenticación (reflejado en el modal de error de inicio de sesión según el mockup).

---

## 3. Estrategias de Optimización de Base de Datos y ORM

### 3.1 Prevención de Consultas N+1
Para evitar sobrecargar la base de datos con consultas recurrentes dentro de bucles en templates:
- **`select_related('owner', 'assigned_user')`:** Empleado en `project_list` y `project_actualizar` para traer en un solo `JOIN` SQL los datos de usuario relacionados (`ForeignKey`).
- **`prefetch_related('deliverables')`:** Utilizado para precargar los entregables de múltiples proyectos mediante una única consulta adicional optimizada.

### 3.2 Indexación y Agregación a Nivel de Motor
- Índices explícitos (`db_index=True`) en campos de filtrado y ordenamiento frecuente:
  - `Project.code` (búsquedas por identificador único).
  - `Project.phase`, `Project.status`, `Project.estatus` (filtros analíticos de dashboard).
  - `Project.created_at` (ordenamiento cronológico).
- Uso de funciones agregadas nativas (`Count('id')`, `Sum`, `TruncMonth`) delegando el procesamiento al motor de base de datos en lugar de iterar colecciones en Python.

---

## 4. Principios de Interfaz Limpia y Adaptación UI/UX

### 4.1 Fidelidad a los Mockups de Referencia
El diseño replica rigurosamente los 17 esquemas del archivo de presentación:
- **Pantalla de Inicio de Sesión (Páginas 1 y 2):** Card central blanco sobre lienzo coral corporativo (`#FA5C3C`), inputs tipo píldora (`border-radius: 9999px`), botón de acceso rápido para visitantes y caja modal de error con contador numérico de intentos.
- **Gestión de Usuarios (Página 3 a 7):** Tabla con avatares cromáticos, etiquetas de rol con color institucional (Rojo Admin, Celeste Coordinador, Gris PMO), menú contextual `...` con modales para adición, edición, reseteo de claves y ficha de detalles.
- **Gestión y Seguimiento de Proyectos (Páginas 8 y 14):** Tablas con ordenamiento dinámico, selectores inline de procura, sincronización visual de fases y botones de respaldo y restauración.
- **Dashboard y Reportes (Páginas 10, 11, 12, 15, 16, 17):** 
  - Contador regresivo en tiempo real (`Tiempo restante para el corte`).
  - Bloques de filtros con botones en cápsula azul.
  - Tablas de resumen estadístico por Fase, Estado y Estatus con totales calculados.
  - Gráficos integrados con **Chart.js**: barras por fase, gráfico donut y diagrama compuesto de barras y líneas (*Comportamiento Enero - Noviembre*).

### 4.2 Marca Blanca Neutra
Se sustituyeron íntegramente las referencias previas por la identidad **ProjectFlow**, acompañada de logotipo vectorial SVG escalable y paleta de diseño moderna adecuada para cualquier portafolio profesional de desarrollo freelance.
