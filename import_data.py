import os
import django
import json
from django.core.management.base import BaseCommand

# Настройка Django для продакшена
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_production')
django.setup()

class Command(BaseCommand):
    help = 'Import initial data (safe for existing data)'

    def handle(self, *args, **options):
        """Импорт данных в продакшн базу с проверкой существующих данных"""
        
        files_to_import = [
            ('data_export_core.json', None),  # Всегда импортируем core данные
            ('data_export_skills.json', 'skills.Skill'),
            ('data_export_portfolio.json', 'portfolio.Project'), 
            ('data_export_certificates.json', 'certificates.Certificate'),
            ('data_export_blog.json', 'blog.BlogPost'),  # Проверяем блог-посты
            ('data_export_contacts.json', 'contacts.Contact')
        ]
        
        for filename, model_check in files_to_import:
            if os.path.exists(filename):
                try:
                    should_import = True
                    if model_check:
                        app_label, model_name = model_check.split('.')
                        from django.apps import apps
                        try:
                            model_class = apps.get_model(app_label, model_name)
                            if model_class.objects.exists():
                                self.stdout.write(
                                    self.style.WARNING(f'⚠️ {model_check} data already exists, skipping {filename}')
                                )
                                should_import = False
                        except Exception as e:
                            self.stdout.write(
                                self.style.WARNING(f'⚠️ Could not check {model_check}: {e}')
                            )
                    
                    if should_import:
                        if filename == 'data_export_blog.json':
                            self.stdout.write(f"📥 Processing {filename} with author_id fix...")
                            self._import_blog_data_with_author_fix(filename)
                        else:
                            self.stdout.write(f"📥 Importing {filename}...")
                            from django.core.management import call_command
                            call_command('loaddata', filename)
                        
                        self.stdout.write(
                            self.style.SUCCESS(f"✅ {filename} imported successfully")
                        )
                    
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"❌ Error importing {filename}: {e}")
                    )
            else:
                self.stdout.write(
                    self.style.WARNING(f"⚠️ File {filename} not found")
                )

        self.stdout.write(self.style.SUCCESS("\n🎉 Import completed!"))

    def _import_blog_data_with_author_fix(self, filename):
        """Импорт блог данных с исправлением author_id на существующего суперпользователя"""
        from django.contrib.auth.models import User
        from blog.models import BlogPost, Category
        
        # Находим существующего суперпользователя
        superuser = User.objects.filter(is_superuser=True).first()
        if not superuser:
            self.stdout.write(
                self.style.ERROR("❌ No superuser found for blog posts")
            )
            return
        
        # Читаем и обрабатываем JSON файл
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Исправляем author_id во всех записях блога
        for item in data:
            if item['model'] == 'blog.blogpost':
                item['fields']['author'] = superuser.id
                self.stdout.write(f"🔧 Fixed author_id to {superuser.id} for post: {item['fields'].get('title_ru', 'Unknown')}")
        
        # Создаем временный файл с исправленными данными
        temp_filename = f"temp_{filename}"
        with open(temp_filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        try:
            # Загружаем исправленные данные
            from django.core.management import call_command
            call_command('loaddata', temp_filename)
        finally:
            # Удаляем временный файл
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

def import_data():
    """Legacy function for backward compatibility"""
    from django.core.management import call_command
    call_command('import_data')

if __name__ == "__main__":
    import_data()
