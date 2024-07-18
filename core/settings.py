from pathlib import Path
import datetime as dt
import os
import environ


env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])


# Application definition

DEFAULT_DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
]

LOCAL_APPS = ["SistemaApp", "UsuarioApp", "FabricaApp"]


THIRD_APPS = [
    "tailwind",
    "theme",
    "allauth",
    "allauth.account",
    "allauth.mfa",
    "crispy_forms",
    "crispy_tailwind",
    "preventconcurrentlogins",
    "axes",
]

INSTALLED_APPS = DEFAULT_DJANGO_APPS + LOCAL_APPS + THIRD_APPS

TAILWIND_APP_NAME = "theme"

INTERNAL_IPS = env.list("INTERNAL_IPS", default=[])

NPM_BIN_PATH = os.environ.get("NPM_BIN_PATH")

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"

CRISPY_TEMPLATE_PACK = "tailwind"


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "preventconcurrentlogins.middleware.PreventConcurrentLoginsMiddleware",
    "axes.middleware.AxesMiddleware",
    "SistemaApp.middleware.UpdateLastActivityMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

WSGI_APPLICATION = "core.wsgi.application"

MFA_ADAPTER = "allauth.mfa.adapter.DefaultMFAAdapter"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": env.db(),
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "es-us"

TIME_ZONE = "America/Santiago"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = "static/"

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# else: EMAIL_BACKEND = [Configuración de correo]


ACCOUNT_ALLOW_REGISTRATION = True

ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False
LOGIN_REDIRECT_URL = "Home"


ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None

ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3

ACCOUNT_LOGOUT_ON_GET = True

SESSION_COOKIE_AGE = 1200  # 20 minutes in seconds

LOGIN_URL = "account_login"

# -----------------------------------------------

MFA_RECOVERY_CODE_COUNT = 10
# El número de códigos de recuperación.

MFA_TOTP_PERIOD = 30
# El período durante el cual un código TOTP será válido, en segundos.

MFA_TOTP_DIGITS = 6
# The number of digits for TOTP codes.

# -------------------------------------------------

delta = dt.timedelta(minutes=5)

AXES_FAILURE_LIMIT = 3
AXES_COOLOFF_TIME = delta
AXES_RESET_ON_SUCCESS = True
AXES_ENABLE_ACCESS_FAILURE_LOG = True
AXES_LOCK_OUT_AT_FAILURE = True
