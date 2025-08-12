from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction, connection
from decouple import config

class Command(BaseCommand):
    help = 'Create superuser safely (preserve existing data)'

    def handle(self, *args, **options):
        username = config('DJANGO_SUPERUSER_USERNAME', default='admin')
        email = config('DJANGO_SUPERUSER_EMAIL', default='vitalivo@gmail.com')
        password = config('DJANGO_SUPERUSER_PASSWORD', default='admin123456')
        
        try:
            with transaction.atomic():
                existing_superuser = User.objects.filter(is_superuser=True).first()
                
                if existing_superuser:
                    self.stdout.write(
                        self.style.WARNING(f'⚠️ Superuser already exists: {existing_superuser.username} (id={existing_superuser.id})')
                    )
                    # Update existing superuser if needed
                    if existing_superuser.username != username or existing_superuser.email != email:
                        existing_superuser.username = username
                        existing_superuser.email = email
                        existing_superuser.set_password(password)
                        existing_superuser.save()
                        self.stdout.write(
                            self.style.SUCCESS(f'✅ Updated existing superuser: {username}')
                        )
                    return
                
                user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Created new superuser: {username} with id={user.id}')
                )
                self.stdout.write(f'📧 Email: {email}')
                self.stdout.write(f'🔑 Password: {password}')
                self.stdout.write(f'🌐 Admin URL: /admin/')
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error creating admin: {str(e)}')
            )
            # Дополнительная диагностика
            existing_users = User.objects.all()
            self.stdout.write(f'⚠️ Current users in database: {existing_users.count()}')
            for u in existing_users:
                self.stdout.write(f'   - ID: {u.id}, Username: {u.username}, Email: {u.email}')
            raise e
