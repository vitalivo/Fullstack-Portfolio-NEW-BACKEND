"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from decouple import config

# Определяем какие настройки использовать на основе DEBUG
if config('DEBUG', default=True, cast=bool):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_production')

application = get_wsgi_application()
