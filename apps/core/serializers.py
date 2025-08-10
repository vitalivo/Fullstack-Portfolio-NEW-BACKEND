from rest_framework import serializers
from .models import Profile, Experience

class ProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля"""
    
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    age = serializers.IntegerField(source='get_age', read_only=True)
    
    class Meta:
        model = Profile
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'birth_date', 'age',
            'location', 'email', 'phone', 'linkedin_url', 'github_url',
            'current_title_en', 'current_title_ru', 'current_title_he',
            'bio_en', 'bio_ru', 'bio_he',
            'years_management', 'years_it', 'team_size_managed',
            'photo', 'resume_en', 'resume_ru', 'resume_he',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'full_name', 'age']

class ExperienceSerializer(serializers.ModelSerializer):
    """Сериализатор для опыта работы"""
    
    experience_type_display = serializers.CharField(source='get_experience_type_display', read_only=True)
    
    class Meta:
        model = Experience
        fields = [
            'id', 'company', 'location',
            'title_en', 'title_ru', 'title_he',
            'description_en', 'description_ru', 'description_he',
            'experience_type', 'experience_type_display',
            'start_date', 'end_date', 'is_current',
            'order', 'created_at'
        ]
        read_only_fields = ['created_at']

class ProfileWithExperienceSerializer(ProfileSerializer):
    """Профиль с опытом работы"""
    
    experiences = ExperienceSerializer(many=True, read_only=True)
    
    class Meta(ProfileSerializer.Meta):
        fields = ProfileSerializer.Meta.fields + ['experiences']
