from pathlib import Path
from django.conf import settings
from django.core.management.utils import get_random_secret_key
from datetime import timedelta
import os
import sys
import dj_database_url

# region GENERAL
# ------------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = BASE_DIR / "real_estate_api"

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = ['*']

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DATE_FORMAT = "d.m.Y"
DATE_INPUT_FORMATS = ['%d.%m.%Y.']
# endregion

# region APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'whitenoise.runserver_nostatic',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    "crispy_forms",
    'drf_yasg',
    'django_filters',
]

LOCAL_APPS = [
    'real_estate_api.kupci.apps.KupciConfig',
    'real_estate_api.korisnici.apps.KorisniciConfig',
    'real_estate_api.stanovi.apps.StanoviConfig',
    'real_estate_api.ponude.apps.PonudeConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
# endregion

# region AUTHENTICATION
# ------------------------------------------------------------------------------
AUTH_USER_MODEL = 'korisnici.Korisnici'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.RemoteUserBackend',
    'django.contrib.auth.backends.ModelBackend',
)
# endregion

# region MIDDLEWARE
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
]
# endregion

# region URLS
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'

LOGIN_URL = "/admin/"

# endregion

# region TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [APPS_DIR / 'templates'],
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
# endregion

# region SECURITY
# ------------------------------------------------------------------------------
# SESSION_COOKIE_HTTPONLY = True
# CSRF_COOKIE_HTTPONLY = True
# SECURE_BROWSER_XSS_FILTER = True
# X_FRAME_OPTIONS = "DENY"

# USE_X_FORWARDED_HOST = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# Security Headers
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# SECURE_HSTS_SECONDS = 3600

# endregion

# region DATABASES
# ------------------------------------------------------------------------------
if DEBUG is True:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv("POSTGRES_DB", 'recrm_api'),
            'USER': os.getenv("POSTGRES_USER", 'recrm_api'),
            'PASSWORD': os.getenv("POSTGRES_PASSWORD", 'recrm_api'),
            'HOST': os.getenv("POSTGRES_HOST", 'fwwrecrm'),
            'PORT': os.getenv("POSTGRES_PORT", '5432'),
        }
    }
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #         'NAME': 'recrm_api',  # for Local DB-BASE
    #         'USER': 'recrm_api',
    #         'PASSWORD': '8Ib4sCdLNxZp7wG9',
    #         'HOST': 'recrmapi-do-user-3327901-0.b.db.ondigitalocean.com',
    #         'PORT': '25060',
    #     }
    # }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'recrm_api',  # for Local DB-BASE
            'USER': 'recrm_api',
            'PASSWORD': 'fwwrecrm',
            'HOST': 'recrmapi-do-user-3327901-0.b.db.ondigitalocean.com',
            'PORT': '25060',
        }
    }
# endregion

# region PASSWORDS VALIDATORS
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]
# endregion

# region SIMPLE_JWT
# ------------------------------------------------------------------------------
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer', 'JWT'),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}
# endregion

# region INTERNATIONALIZATION
# ------------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = False

USE_TZ = True
# endregion

# region STATIC
# ------------------------------------------------------------------------------
STATIC_ROOT = str(BASE_DIR / "static")  # In production we want to use CDN
STATIC_URL = "/static/"
STATICFILES_DIRS = [str(APPS_DIR / "static")]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
# endregion

# region MEDIA
# ------------------------------------------------------------------------------
MEDIA_ROOT = str(BASE_DIR / "media")
MEDIA_URL = "/media/"

CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = [
    'https://stanovi.biz',
    'https://api.stanovi.biz',
    'https://prodaja-stanova-front-pnyfj.ondigitalocean.app',
    'http://api.dejan.pro',
    'http://localhost:3000',
    'http://127.0.0.1:8000',
    'http://127.0.0.1',
    'http://127.0.0.1:3000',
    'http://164.92.253.160',
    'https://stanovi.dejan.pro',
    'http://stanovi.dejan.pro',
]
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
# endregion

# region REST_FRAMEWORK
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',

    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',

    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # @see https://www.django-rest-framework.org/api-guide/permissions/
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}
# endregion

# region SWAGGER DOCS
# ------------------------------------------------------------------------------
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': True,  # add Django Login and Django Logout buttons, CSRF token to swagger UI page
    'LOGIN_URL': getattr(settings, 'LOGIN_URL', None),  # URL for the login button
    'LOGOUT_URL': getattr(settings, 'LOGOUT_URL', None),  # URL for the logout button

    # Swagger security definitions to include in the schema;
    # see https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#security-definitions-object
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        },
        "api_key": {
            "type": "apiKey",
            "name": "api_key",
            "in": "header"
        },
    },

    # url to an external Swagger validation service; defaults to 'http://online.swagger.io/validator/'
    # set to None to disable the schema validation badge in the UI
    'VALIDATOR_URL': '',

    # swagger-ui configuration settings,
    # see https://github.com/swagger-api/swagger-ui/blob/112bca906553a937ac67adc2e500bdeed96d067b/docs/usage/configuration.md#parameters
    'OPERATIONS_SORTER': None,
    'TAGS_SORTER': None,
    'DOC_EXPANSION': 'none',
    'DEEP_LINKING': False,
    'SHOW_EXTENSIONS': True,
    'DEFAULT_MODEL_RENDERING': 'model',
    'DEFAULT_MODEL_DEPTH': 2,
}
# endregion
