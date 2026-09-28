"""
Django settings for ProjectFlow (formerly pasantias_proyecto).
Configurado con buenas prácticas profesionales para exhibición en GitHub.
Soporta PostgreSQL para producción y SQLite como fallback de desarrollo.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Carga variables de entorno desde .env
load_dotenv()

# Construye las rutas dentro del proyecto: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SEGURIDAD: Clave secreta leída de variable de entorno con fallback seguro para desarrollo local
SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'django-insecure-projectflow-dev-secret-key-2026-safe-local'
)

# SEGURIDAD: DEBUG configurable por entorno
DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 't')

# Hosts permitidos
ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,0.0.0.0').split(',')
    if host.strip()
]

# Definición de Aplicaciones Instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Aplicaciones locales
    'admin_user',
    # Terceros
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pasantias_proyecto.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'admin_user', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pasantias_proyecto.wsgi.application'

# ==============================================================================
# CONFIGURACIÓN FLEXIBLE DE BASE DE DATOS (Estándar GitHub)
# ==============================================================================
# Conexión flexible: Si DB_ENGINE está configurado para PostgreSQL en el .env,
# se conectará a PostgreSQL. De lo contrario, o si no se definen variables,
# aplicará automáticamente un fallback seguro a SQLite local (db.sqlite3).
DB_ENGINE_ENV = os.getenv('DB_ENGINE', '').strip().lower()

if 'postgresql' in DB_ENGINE_ENV:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'projectflow_db'),
            'USER': os.getenv('DB_USER', 'postgres'),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST': os.getenv('DB_HOST', '127.0.0.1'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }
else:
    # Fallback automático garantizado a SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Modelo de Usuario Personalizado
AUTH_USER_MODEL = 'admin_user.CustomUser'

# Validadores de Contraseña
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Configuración Regional e Internacionalización
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Caracas'
USE_I18N = True
USE_TZ = True

# Archivos Estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Archivos Multimedia
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Rutas de Autenticación
LOGIN_URL = '/admin_user/login/'
LOGIN_REDIRECT_URL = '/admin_user/projects/'
LOGOUT_REDIRECT_URL = '/admin_user/login/'
