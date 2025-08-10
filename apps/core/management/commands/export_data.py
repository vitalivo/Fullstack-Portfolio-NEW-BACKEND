from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = 'Export all data to JSON files for deployment'

    def handle(self, *args, **options):
        self.stdout.write('📦 Exporting data for deployment...')
        
        # Экспортируем данные по приложениям
        apps_to_export = [
            ('core', ['core.Profile', 'core.Experience']),
            ('skills', ['skills.SkillCategory', 'skills.Skill']),
            ('portfolio', ['portfolio.Technology', 'portfolio.ProjectCategory', 'portfolio.Project']),
            ('certificates', ['certificates.Certificate']),
            ('contacts', ['contacts.ContactInfo']),
            ('blog', ['blog.BlogCategory', 'blog.BlogTag', 'blog.BlogPost']),
        ]
        
        for app_name, models in apps_to_export:
            filename = f'fixtures/{app_name}_data.json'
            
            # Создаем папку fixtures если её нет
            os.makedirs('fixtures', exist_ok=True)
            
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    call_command('dumpdata', *models, format='json', indent=2, stdout=f)
                
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Exported {app_name} data to {filename}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error exporting {app_name}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('🎉 Data export completed! Files saved in fixtures/ folder')
        )
