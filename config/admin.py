from django.contrib import admin
from django.conf import settings

# Настройка админ панели
admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.index_title = settings.ADMIN_INDEX_TITLE

# Дополнительные настройки админки
admin.site.site_url = '/'  # Ссылка "Посмотреть сайт"
admin.site.enable_nav_sidebar = True  # Боковая панель навигации