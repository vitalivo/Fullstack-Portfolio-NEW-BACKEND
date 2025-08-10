from rest_framework import serializers
from .models import SkillCategory, Skill

class SkillCategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий навыков"""
    
    class Meta:
        model = SkillCategory
        fields = ['id', 'name_en', 'name_ru', 'name_he', 'slug', 'icon', 'color', 'order']

class SkillSerializer(serializers.ModelSerializer):
    """Сериализатор для навыков"""
    
    category = SkillCategorySerializer(read_only=True)
    skill_type_display = serializers.CharField(source='get_skill_type_display', read_only=True)
    proficiency_text = serializers.CharField(source='get_proficiency_text', read_only=True)
    is_recent = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Skill
        fields = [
            'id', 'name', 'category', 'skill_type', 'skill_type_display',
            'proficiency_level', 'proficiency_text', 'proficiency_percentage',
            'description_en', 'description_ru', 'description_he',
            'years_of_experience', 'last_used', 'is_recent',
            'icon', 'color', 'logo', 'is_featured', 'order',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'is_recent']

class SkillsByCategorySerializer(serializers.ModelSerializer):
    """Навыки сгруппированные по категориям"""
    
    skills = SkillSerializer(many=True, read_only=True)
    
    class Meta:
        model = SkillCategory
        fields = ['id', 'name_en', 'name_ru', 'name_he', 'slug', 'icon', 'color', 'order', 'skills']
