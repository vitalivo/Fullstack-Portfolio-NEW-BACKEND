from django.core.management.base import BaseCommand
from django.core.management import call_command
from pathlib import Path
import os

class Command(BaseCommand):
    help = 'Import all fixtures data'

    def handle(self, *args, **options):
        self.stdout.write('📦 Importing fixtures data...')
        
        # Путь к fixtures
        fixtures_dir = Path(__file__).resolve().parent.parent.parent.parent.parent / 'fixtures'
        
        # Порядок импорта (важен из-за зависимостей)
        fixtures = [
            'core_data.json',
            'skills_data.json',
            'portfolio_data.json',
            'certificates_data.json',
            'contacts_data.json',
            'blog_data.json',
        ]
        
        for fixture in fixtures:
            fixture_path = fixtures_dir / fixture
            
            if fixture_path.exists():
                try:
                    call_command('loaddata', str(fixture_path))
                    self.stdout.write(
                        self.style.SUCCESS(f'✅ Loaded {fixture}')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'❌ Error loading {fixture}: {str(e)}')
                    )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠️ {fixture} not found')
                )
        
        self.stdout.write(
            self.style.SUCCESS('🎉 Fixtures import completed!')
        )
