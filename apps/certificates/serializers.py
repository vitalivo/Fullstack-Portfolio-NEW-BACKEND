from rest_framework import serializers
from .models import Certificate

class CertificateSerializer(serializers.ModelSerializer):
    """Сериализатор для сертификатов"""
    
    certificate_type_display = serializers.CharField(source='get_certificate_type_display', read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    skills_list_en = serializers.ListField(source='get_skills_list_en', read_only=True)
    skills_list_ru = serializers.ListField(source='get_skills_list_ru', read_only=True)
    skills_list_he = serializers.ListField(source='get_skills_list_he', read_only=True)
    
    class Meta:
        model = Certificate
        fields = [
            'id', 'title_en', 'title_ru', 'title_he',
            'issuer', 'credential_id', 'issue_date', 'expiry_date',
            'description_en', 'description_ru', 'description_he',
            'skills_learned_en', 'skills_learned_ru', 'skills_learned_he',
            'skills_list_en', 'skills_list_ru', 'skills_list_he',
            'certificate_image', 'verify_url', 'certificate_file',
            'certificate_type', 'certificate_type_display',
            'score', 'has_distinction', 'is_featured', 'is_expired',
            'order', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'is_expired']

class CertificateListSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для списка сертификатов"""
    
    certificate_type_display = serializers.CharField(source='get_certificate_type_display', read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Certificate
        fields = [
            'id', 'title_en', 'title_ru', 'title_he',
            'issuer', 'issue_date', 'certificate_image',
            'verify_url', 'certificate_file', 'credential_id',
            'certificate_type', 'certificate_type_display',
            'score', 'has_distinction', 'is_featured', 'is_expired'
        ]
