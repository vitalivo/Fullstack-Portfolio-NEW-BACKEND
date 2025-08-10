from django.contrib import admin
from .models import Profile, Experience

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone')
    search_fields = ('first_name', 'last_name', 'email')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('company', 'title_en', 'experience_type', 'start_date', 'end_date', 'is_current')
    list_filter = ('experience_type', 'is_current', 'start_date')
    search_fields = ('company', 'title_en', 'title_ru')
    date_hierarchy = 'start_date'
