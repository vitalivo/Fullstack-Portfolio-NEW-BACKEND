from django.contrib import admin
from .models import ContactMessage, ContactInfo

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = (
        'email', 'phone', 'address', 
        'linkedin_url', 'github_url', 'telegram_url',
        'working_hours_en', 'working_hours_ru', 'working_hours_he',
        'is_available_for_work', 'created_at', 'updated_at',
        'availability_note_en', 'availability_note_ru', 'availability_note_he'
        )
    search_fields = (
        'email', 'phone', 'address', 'linkedin_url',
        'github_url', 'telegram_url',
        'working_hours_en', 'working_hours_ru', 'working_hours_he',
        'availability_note_en', 'availability_note_ru', 'availability_note_he'
        )
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Контактная информация', {
            'fields': (
                'email', 'phone', 'address', 'linkedin_url',
                'github_url', 'telegram_url', 'twitter_url',
                'working_hours_en', 'working_hours_ru', 'working_hours_he',
                'availability_note_en', 'availability_note_ru', 'availability_note_he',
                'is_available_for_work'
                )
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'ip_address', 'user_agent')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Информация о контакте', {
            'fields': ('name', 'email', 'phone', 'subject')
        }),
        ('Сообщение', {
            'fields': ('message',)
        }),
        ('Техническая информация', {
            'fields': ('ip_address', 'user_agent', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Если редактируем существующее сообщение
            return self.readonly_fields + ('name', 'email', 'phone', 'subject', 'message')
        return self.readonly_fields

    