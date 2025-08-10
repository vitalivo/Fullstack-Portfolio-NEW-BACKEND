# export_data.py
import os
import django
import json
from django.core import serializers

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def export_data():
    """Экспорт данных с правильной кодировкой UTF-8"""
    
    # Список приложений для экспорта
    apps_to_export = [
        'core',
        'skills', 
        'portfolio',
        'certificates',
        'blog',
        'contacts'
    ]
    
    for app in apps_to_export:
        try:
            print(f"Экспортируем {app}...")
            
            # Выполняем команду dumpdata
            from django.core.management import call_command
            from io import StringIO
            
            output = StringIO()
            call_command('dumpdata', app, indent=2, stdout=output)
            data = output.getvalue()
            
            # Сохраняем в файл с UTF-8
            filename = f"data_export_{app}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(data)
            
            print(f"✅ {app} экспортирован в {filename}")
            
        except Exception as e:
            print(f"❌ Ошибка при экспорте {app}: {e}")

if __name__ == "__main__":
    export_data()
    print("\n🎉 Экспорт завершен!")