# AGENTS.md - Directrices de Desarrollo y Estándares de IA

Este documento establece las directrices de arquitectura, codificación, estilo y seguridad obligatorias para cualquier asistente de IA o desarrollador que contribuya a este repositorio (**ProjectFlow - Gestor de Proyectos**).

---

## 1. Principios Generales del Proyecto

- **Nombre del Producto / Marca:** "ProjectFlow" (marca blanca neutral, sin menciones a entidades corporativas privadas anteriores).
- **Stack Tecnológico:**
  - Backend: Python 3.12+ / Django 5+
  - Base de Datos: PostgreSQL (con soporte SQLite en modo local/desarrollo)
  - Frontend: Django Templates (MVT) + HTML5 semántico + CSS modular + Vanilla JS + Bootstrap 5 + Chart.js
  - Gestión de Dependencias: `uv` / `pip` y `python-dotenv` para configuración por entorno.

---

## 2. Reglas de Código en Python y Django

### 2.1 Cumplimiento de PEP 8 y Tipado
- Todo el código Python debe cumplir con el estándar **PEP 8** (longitud de línea razonable, nombres descriptivos `snake_case` para funciones y variables, `PascalCase` para clases y modelos).
- Añadir **anotaciones de tipos (Type Hinting)** en firmas de funciones, métodos y propiedades clave en vistas, formularios y servicios.
- Redactar docstrings explicativos en español formal describiendo el propósito, argumentos y retorno de cada función o clase.

### 2.2 Optimización del ORM y Prevención de Consultas N+1
- **Prohibido realizar consultas N+1:** Siempre que se acceda a relaciones foráneas en bucles de plantillas o vistas, utilizar explícitamente:
  - `select_related('foreign_key_field')` para relaciones `ForeignKey` y `OneToOne`.
  - `prefetch_related('many_to_many_or_reverse_fk')` para relaciones inversas y `ManyToManyField` (ej. entregables o historial).
- Utilizar `only()` o `defer()` cuando los objetos contengan campos de texto o blobs pesados que no sean necesarios en la vista.
- Emplear agregaciones ORM (`Count`, `Sum`, `Avg`, `TruncMonth`) a nivel de base de datos en lugar de procesar listas o conteos en memoria con Python.

---

## 3. Convenciones de Interfaz de Usuario y Frontend (UI/UX)

### 3.1 Fidelidad al Diseño de Referencia (Prototipos y Mockups)
- **Paleta Cromática Corporativa:**
  - Color Primario / Marca: Coral / Naranja Corporativo (`#FF5733` / `#FA5C3C` / `#E64A19`)
  - Acentos de Estado:
    - Verde Éxito / Activo: `#2ECC71` / `#22C55E`
    - Azul Corporativo / Acciones: `#0D6EFD` / `#3B82F6`
    - Amarillo Advertencia / Alerta: `#F59E0B` / `#FFC107`
    - Rojo Peligro / Bloqueo: `#DC2626` / `#EF4444`
    - Gris Neutro / PMO: `#6B7280` / `#9CA3AF`
  - Fondos: Blanco pulcro (`#FFFFFF`), Gris tenue (`#F8F9FA` / `#F1F5F9`) y Superficie lateral limpia.
- **Estructura Visual de Pantallas:**
  - **Barra Lateral Izquierda Fija:** Logo superior "ProjectFlow", selector de navegación con botón activo resaltado en marco distintivo, y botón inferior "Cerrar sesión".
  - **Área de Trabajo Central:** Tarjeta blanca redondeada con sombra suave (`border-radius: 16px`, elevación elegante).
  - **Botones y Acciones:** Botón "+ New User" o "Agregar +" en azul, botón "Block" o "Eliminar" en rojo, acciones secundarias en gris/outline.
  - **Controles de Tabla:** Barra de búsqueda integrada, selectores de rol y paginador inferior `< 1 2 3 4 ... 10 >` con selector de filas por página.

### 3.2 Separación de Responsabilidades CSS y JS
- Mantener los estilos centralizados en `static/css/projectflow.css` o archivos modulares bien estructurados, evitando estilos en línea innecesarios.
- El código JavaScript interactivo (como renderizado de gráficos Chart.js, conteo regresivo de corte de reporte, modales y validación de formularios) debe ser modular, defensivo y desacoplado de la estructura HTML.

---

## 4. Directrices Estrictas de Seguridad y Buenas Prácticas

### 4.1 Gestión de Secretos y Variables de Entorno
- **Nunca registrar credenciales en el control de versiones:** `SECRET_KEY`, `DEBUG`, credenciales de base de datos (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`) deben leerse exclusivamente de variables de entorno mediante `python-dotenv`.
- Mantener siempre actualizado `.env.example` con variables dummy seguras y descripciones claras.

### 4.2 Control de Acceso Basado en Roles (RBAC)
- Todas las vistas privadas deben requerir autenticación (`@login_required` o `LoginRequiredMixin`).
- Implementar validaciones de roles estrictas:
  - **Administrador:** Acceso total a gestión de usuarios, roles, creación/eliminación de proyectos y respaldos.
  - **Coordinador:** Gestión operativa de proyectos asignados, actualización de avances (%Plan, %Real, Procura) y visualización de reportes.
  - **PMO / Auditor:** Acceso a métricas globales, tableros de reportes y supervisión ejecutiva.
  - **Invitado (Guest):** Acceso de solo lectura a tableros y proyectos públicos de muestra.

### 4.3 Auditoría e Integridad de Datos
- Cada modelo principal debe incorporar campos de auditoría: `created_at` (`auto_now_add=True`) y `updated_at` (`auto_now=True`).
- Validación estricta de entradas numéricas y porcentajes (0 a 100%) con cálculo automático de desviación (`%Real - %Plan`).
