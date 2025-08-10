# import_data.py
import os
import django
import json

# Настройка Django для продакшена
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_production')
django.setup()

def import_data():
    """Импорт данных в продакшн базу"""
    
    # Список файлов для импорта (в правильном порядке)
    files_to_import = [
        'data_export_core.json',
        'data_export_skills.json', 
        'data_export_portfolio.json',
        'data_export_certificates.json',
        'data_export_blog.json',
        'data_export_contacts.json'
    ]
    
    for filename in files_to_import:
        if os.path.exists(filename):
            try:
                print(f"Импортируем {filename}...")
                
                from django.core.management import call_command
                call_command('loaddata', filename)
                
                print(f"✅ {filename} импортирован успешно")
                
            except Exception as e:
                print(f"❌ Ошибка при импорте {filename}: {e}")
        else:
            print(f"⚠️ Файл {filename} не найден")

if __name__ == "__main__":
    import_data()
    print("\n🎉 Импорт завершен!")