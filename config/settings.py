import os
from pathlib import Path
from decouple import config
import ssl # <-- Добавляем импорт модуля ssl

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-me-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost,0.0.0.0').split(',') # Объединил и использую config

# Application definition
DJANGO_APPS = [
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'django_filters',
]
THIRD_PARTY_APPS = [
  'rest_framework',
  'corsheaders',
  # 'modeltranslation',
  # 'ckeditor',
  # 'ckeditor_uploader',
]
LOCAL_APPS = [
  'apps.core.apps.CoreConfig',
  'apps.portfolio.apps.PortfolioConfig',
  'apps.blog.apps.BlogConfig',
  'apps.certificates.apps.CertificatesConfig',
  'apps.skills.apps.SkillsConfig',
  'apps.contacts.apps.ContactsConfig',
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
  'corsheaders.middleware.CorsMiddleware',
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.locale.LocaleMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
  {
      'BACKEND': 'django.template.backends.django.DjangoTemplates',
      'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASES = {
  'default': {
      'ENGINE': 'django.db.backends.postgresql',
      'NAME': config('DB_NAME', default='vitaly_portfolio'),
      'USER': config('DB_USER', default='postgres'),
      'PASSWORD': config('DB_PASSWORD', default='password'),
      'HOST': config('DB_HOST', default='localhost'),
      'PORT': config('DB_PORT', default='5432'),
  }
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators
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

# Internationalization
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Asia/Jerusalem'
USE_I18N = True
USE_TZ = True

# Languages
LANGUAGES = [
  ('en', 'English'),
  ('ru', 'Русский'),
  ('he', 'עברית'),
]
LOCALE_PATHS = [
  BASE_DIR / 'locale',
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
  BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework
REST_FRAMEWORK = {
  'DEFAULT_RENDERER_CLASSES': [
      'rest_framework.renderers.JSONRenderer',
      'rest_framework.renderers.BrowsableAPIRenderer',
  ],
  'DEFAULT_PARSER_CLASSES': [
      'rest_framework.parsers.JSONParser',
      'rest_framework.parsers.FormParser',
      'rest_framework.parsers.MultiPartParser',
  ],
  'DEFAULT_AUTHENTICATION_CLASSES': [
      'rest_framework.authentication.SessionAuthentication',
      'rest_framework.authentication.BasicAuthentication',
  ],
  'DEFAULT_PERMISSION_CLASSES': [
      'rest_framework.permissions.IsAuthenticatedOrReadOnly',
  ],
  'DEFAULT_FILTER_BACKENDS': [
      'django_filters.rest_framework.DjangoFilterBackend',
      'rest_framework.filters.SearchFilter',
      'rest_framework.filters.OrderingFilter',
  ],
  'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
  'PAGE_SIZE': 20,
  'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
  'DEFAULT_VERSION': 'v1',
  'ALLOWED_VERSIONS': ['v1'],
  'VERSION_PARAM': 'version',
}

# CORS настройки для фронтенда
# В settings.py ИСПРАВИТЬ:
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://fullstack-portfolio-new.vercel.app",  # ← ИСПРАВИТЬ ЭТУ СТРОКУ!
]

CORS_ALLOW_CREDENTIALS = True

# Email settings (для обратной связи)
# Возвращаем SMTP Backend, так как отправка идет через smtplib в utils.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)

# Определяем GMAIL_USER и GMAIL_APP_PASSWORD как атрибуты settings
# Это необходимо для доступа из apps/contacts/utils.py
GMAIL_USER = config('GMAIL_USER')
GMAIL_APP_PASSWORD = config('GMAIL_APP_PASSWORD')

# Используем GMAIL_USER для DEFAULT_FROM_EMAIL и CONTACT_FORM_RECIPIENT_EMAIL
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default=GMAIL_USER)
CONTACT_FORM_RECIPIENT_EMAIL = config('CONTACT_FORM_RECIPIENT_EMAIL', default=GMAIL_USER)

# --- ВРЕМЕННОЕ РЕШЕНИЕ ДЛЯ РАЗРАБОТКИ: Отключаем проверку SSL ---
# Этот блок должен быть удален, так как SSL-обход теперь в utils.py
# EMAIL_SSL_CONTEXT = ssl.create_default_context()
# EMAIL_SSL_CONTEXT.check_hostname = False
# EMAIL_SSL_CONTEXT.verify_mode = ssl.CERT_NONE
# --- КОНЕЦ ВРЕМЕННОГО РЕШЕНИЯ ---

# Telegram Bot (для уведомлений)
TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN', default='')
TELEGRAM_CHAT_ID = config('TELEGRAM_CHAT_ID', default='')

# Дополнительные настройки для API
APPEND_SLASH = True

# CKEditor settings
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
  'default': {
      'toolbar': 'full',
      'height': 300,
      'width': '100%',
  },
}

# Настройки админки
ADMIN_SITE_HEADER = 'Портфолио Виталия - Админ панель'
ADMIN_SITE_TITLE = 'Админ панель'
ADMIN_INDEX_TITLE = 'Управление контентом'

# Настройки логирования для отладки почты
LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'formatters': {
      'verbose': {
          'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
          'style': '{',
      },
      'simple': {
          'format': '{levelname} {message}',
          'style': '{',
      },
  },
  'handlers': {
      'console': {
          'class': 'logging.StreamHandler',
          'formatter': 'simple',
      },
      'mail_file': {
          'level': 'DEBUG',
          'class': 'logging.FileHandler',
          'filename': os.path.join(BASE_DIR, 'logs', 'mail_debug.log'),
          'formatter': 'verbose',
      },
  },
  'loggers': {
      'django.server': {
          'handlers': ['console'],
          'level': 'INFO',
          'propagate': False,
      },
      'django.request': {
          'handlers': ['console'],
          'level': 'ERROR',
          'propagate': False,
      },
      'django.db.backends': {
          'handlers': ['console'],
          'level': 'INFO',
          'propagate': False,
      },
      'django.mail': {
          'handlers': ['console', 'mail_file'],
          'level': 'DEBUG', # Установите DEBUG для максимальной детализации
          'propagate': False,
      },
  },
  'root': {
      'handlers': ['console'],
      'level': 'WARNING',
  },
}
