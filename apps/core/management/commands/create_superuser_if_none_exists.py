from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from decouple import config

class Command(BaseCommand):
    help = 'Create a superuser if none exists'

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(
                self.style.SUCCESS('✅ Superuser already exists')
            )
            return

        # Создаем суперпользователя из переменных окружения
        username = config('DJANGO_SUPERUSER_USERNAME', default='admin')
        email = config('DJANGO_SUPERUSER_EMAIL', default='vitalivo@gmail.com')
        password = config('DJANGO_SUPERUSER_PASSWORD', default='admin123456')

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Superuser "{username}" created successfully')
        )
