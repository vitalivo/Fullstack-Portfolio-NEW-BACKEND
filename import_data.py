import os
import django
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
            ('data_export_contacts.json', 'contacts.Contact')
        ]
        
        self.stdout.write("📦 Importing fixtures data...")
        
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
                        from django.core.management import call_command
                        call_command('loaddata', filename)
                        self.stdout.write(
                            self.style.SUCCESS(f"✅ Loaded {filename}")
                        )
                    
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"❌ Error loading {filename}: {e}")
                    )
            else:
                self.stdout.write(
                    self.style.WARNING(f"⚠️ File {filename} not found")
                )

        self.stdout.write(self.style.SUCCESS("🎉 Fixtures import completed!"))

def import_data():
    """Legacy function for backward compatibility"""
    from django.core.management import call_command
    call_command('import_data')

if __name__ == "__main__":
    import_data()
