from django.contrib import admin
from .models import ContactMessage

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
