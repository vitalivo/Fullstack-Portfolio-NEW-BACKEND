"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from rest_framework.documentation import include_docs_urls

urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),
    
    # API v1
    path('api/v1/core/', include('apps.core.urls')),
    path('api/v1/portfolio/', include('apps.portfolio.urls')),
    path('api/v1/skills/', include('apps.skills.urls')),
    path('api/v1/certificates/', include('apps.certificates.urls')),
    path('api/v1/blog/', include('apps.blog.urls')),
    path('api/v1/contacts/', include('apps.contacts.urls')),
    
    # API документация
    # path('api/docs/', include_docs_urls(title='Vitaly Portfolio API')),
    
    # DRF Browsable API (для разработки)
    path('api-auth/', include('rest_framework.urls')),
]

# Статические файлы для разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

