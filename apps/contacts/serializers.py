from rest_framework import serializers
from .models import ContactMessage, ContactInfo

class ContactMessageSerializer(serializers.ModelSerializer):
    """Сериализатор для контактных сообщений"""
    
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    
    class Meta:
        model = ContactMessage
        fields = [
            'id', 'name', 'email', 'phone', 'company', 'subject', 'message',
            'status', 'status_display', 'priority', 'priority_display',
            'source', 'user_agent', 'ip_address',
            'reply_message', 'replied_at', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'status', 'priority', 'user_agent', 'ip_address',
            'reply_message', 'replied_at', 'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        # Автоматически добавляем IP и User-Agent из запроса
        request = self.context.get('request')
        if request:
            validated_data['ip_address'] = self.get_client_ip(request)
            validated_data['user_agent'] = request.META.get('HTTP_USER_AGENT', '')
        return super().create(validated_data)
    
    def get_client_ip(self, request):
        """Получение IP адреса клиента"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class ContactInfoSerializer(serializers.ModelSerializer):
    """Сериализатор для контактной информации"""
    
    class Meta:
        model = ContactInfo
        fields = [
            'id', 'email', 'phone', 'address',
            'linkedin_url', 'github_url', 'telegram_url', 'twitter_url',
            'working_hours_en', 'working_hours_ru', 'working_hours_he',
            'is_available_for_work',
            'availability_note_en', 'availability_note_ru', 'availability_note_he',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
