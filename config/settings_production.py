import os
import dj_database_url
from decouple import config
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Импортируем базовые настройки
from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# ALLOWED_HOSTS
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1,*.onrender.com').split(',')

# База данных для продакшена
DATABASE_URL = config('DATABASE_URL', default='')
print(f"🔗 DATABASE_URL: {DATABASE_URL[:50]}..." if DATABASE_URL else "❌ DATABASE_URL not found")

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    print("❌ Using fallback database settings")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': 'password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

# ИСПРАВЛЕНО: Полностью убираем STATICFILES_DIRS для продакшена
STATICFILES_DIRS = []

# Статические файлы для продакшена
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise для статических файлов
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Медиа файлы
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# CORS для Vercel фронтенда
cors_origins = config('CORS_ALLOWED_ORIGINS', default='https://fullstack-portfolio-new.vercel.app,http://localhost:3000')
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in cors_origins.split(',') if origin.strip()]

print(f"🌐 CORS_ALLOWED_ORIGINS: {CORS_ALLOWED_ORIGINS}")

# Безопасность
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Email настройки
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)

GMAIL_USER = config('GMAIL_USER', default='vitalivo@gmail.com')
GMAIL_APP_PASSWORD = config('GMAIL_APP_PASSWORD', default='avsx tsjl brds cmlf')

DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default=GMAIL_USER)
CONTACT_FORM_RECIPIENT_EMAIL = config('CONTACT_FORM_RECIPIENT_EMAIL', default=GMAIL_USER)

# Telegram настройки
TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN', default='8447589158:AAF23a8ZvDBkZYLdfOL4t2p6j8AEsW9_ZKA')
TELEGRAM_CHAT_ID = config('TELEGRAM_CHAT_ID', default='769259836')

# Переменные для суперпользователя
DJANGO_SUPERUSER_USERNAME = config('DJANGO_SUPERUSER_USERNAME', default='admin')
DJANGO_SUPERUSER_EMAIL = config('DJANGO_SUPERUSER_EMAIL', default='vitalivo@gmail.com')
DJANGO_SUPERUSER_PASSWORD = config('DJANGO_SUPERUSER_PASSWORD', default='admin123456')

# Логирование для продакшена
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
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

print("🚀 Production settings loaded successfully!")
