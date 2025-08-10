from django.contrib import admin
from .models import SkillCategory, Skill

@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_ru', 'name_he', 'order')
    search_fields = ('name_en', 'name_ru', 'name_he')
    list_editable = ('order',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'proficiency_level', 'is_featured')
    list_filter = ('category', 'proficiency_level', 'is_featured')
    search_fields = ('name', 'description_en')
    list_editable = ('proficiency_level', 'is_featured')
