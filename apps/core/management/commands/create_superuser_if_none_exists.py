from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from decouple import config

class Command(BaseCommand):
    help = 'Force create superuser (delete existing and create new)'

    def handle(self, *args, **options):
        username = config('DJANGO_SUPERUSER_USERNAME', default='admin')
        email = config('DJANGO_SUPERUSER_EMAIL', default='vitalivo@gmail.com')
        password = config('DJANGO_SUPERUSER_PASSWORD', default='admin123456')
        
        try:
            # ПРИНУДИТЕЛЬНО удаляем всех суперпользователей
            deleted_count = User.objects.filter(is_superuser=True).count()
            User.objects.filter(is_superuser=True).delete()
            
            if deleted_count > 0:
                self.stdout.write(f'🗑️ Deleted {deleted_count} existing superuser(s)')
            
            # Создаём нового суперпользователя
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            user.id = 1
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ FORCE CREATED superuser: {username}')
            )
            self.stdout.write(f'📧 Email: {email}')
            self.stdout.write(f'🔑 Password: {password}')
            self.stdout.write(f'🌐 Admin URL: /admin/')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error creating admin: {str(e)}')
            )
