from django.contrib import admin
from .models import Certificate

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'issuer', 'issue_date', 'certificate_type', 'is_featured', 'has_distinction', 'order')
    list_filter = ('certificate_type', 'is_featured', 'has_distinction', 'issue_date', 'issuer')
    search_fields = ('title_en', 'title_ru', 'issuer', 'credential_id', 'description_en')
    date_hierarchy = 'issue_date'
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_featured', 'order')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title_en', 'title_ru', 'title_he', 'issuer', 'certificate_type', 'credential_id')
        }),
        ('Даты', {
            'fields': ('issue_date', 'expiry_date')
        }),
        ('Описание (Английский)', {
            'fields': ('description_en', 'skills_learned_en')
        }),
        ('Описание (Русский)', {
            'fields': ('description_ru', 'skills_learned_ru'),
            'classes': ('collapse',)
        }),
        ('Описание (Иврит)', {
            'fields': ('description_he', 'skills_learned_he'),
            'classes': ('collapse',)
        }),
        ('Оценка', {
            'fields': ('score', 'has_distinction')
        }),
        ('Файлы и ссылки', {
            'fields': ('certificate_image', 'certificate_file', 'verify_url')
        }),
        ('Настройки отображения', {
            'fields': ('is_featured', 'order')
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
