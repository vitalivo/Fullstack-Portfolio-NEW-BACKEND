import os
import requests
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage, ContactInfo
from .serializers import ContactMessageSerializer, ContactInfoSerializer

class ContactMessageViewSet(viewsets.ModelViewSet):
    """API для контактных сообщений"""
    
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]  # Разрешаем всем отправлять сообщения
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'priority', 'source']
    search_fields = ['name', 'email', 'subject', 'message']
    ordering_fields = ['created_at', 'priority']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """Только создание доступно всем, остальное - админам"""
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()
    
    def create(self, request, *args, **kwargs):
        """Создание нового сообщения"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save() # Сигнал post_save будет вызван здесь автоматически
        
        # Автоматически помечаем как прочитанное - это теперь в сигнале
        # message.mark_as_read() 
        
        # Отправка уведомлений - это теперь в сигнале
        # self.send_email_notification(message)
        # self.send_telegram_notification(message)
        
        return Response(
            {'message': 'Сообщение успешно отправлено', 'id': message.id},
            status=status.HTTP_201_CREATED
        )
    
    # Эти методы теперь не нужны в ViewSet, так как логика перенесена в utils.py и вызывается сигналом
    # def send_email_notification(self, message):
    #     ...
    # def send_telegram_notification(self, message):
    #     ...

class ContactInfoViewSet(viewsets.ReadOnlyModelViewSet):
    """API для контактной информации"""
    
    queryset = ContactInfo.objects.all()
    serializer_class = ContactInfoSerializer
    permission_classes = [AllowAny]  # Публичная информация
