#!/usr/bin/env python
"""
Скрипт для создания fixtures с начальными данными
"""
import os
import django
import json
from pathlib import Path

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core import serializers
from apps.core.models import Profile, Experience
from apps.skills.models import SkillCategory, Skill
from apps.portfolio.models import Technology, ProjectCategory, Project
from apps.certificates.models import Certificate
from apps.contacts.models import ContactInfo
from apps.blog.models import BlogCategory, BlogTag, BlogPost

def create_fixtures():
    """Создаём fixtures файлы с данными"""
    
    fixtures_dir = Path('fixtures')
    fixtures_dir.mkdir(exist_ok=True)
    
    print("🚀 Creating fixtures...")
    
    # 1. Core data (Profile, Experience)
    core_data = []
    
    # Создаём профиль если его нет
    profile, created = Profile.objects.get_or_create(
        id=1,
        defaults={
            'first_name': 'Vitaliy',
            'last_name': 'Voloshyn',
            'birth_date': '1990-01-01',
            'location': 'Ukraine',
            'email': 'vitalivo@gmail.com',
            'phone': '+380123456789',
            'linkedin_url': 'https://linkedin.com/in/vitaliy-voloshyn',
            'github_url': 'https://github.com/vitalivo',
            'current_title_en': 'Fullstack Junior Developer',
            'current_title_ru': 'Fullstack Junior Developer',
            'current_title_he': 'מפתח Fullstack Junior',
            'bio_en': 'Experienced manager transitioning to IT with over two years of intensive study and a diploma from SkillFactory. Ready to contribute to innovative web development projects.',
            'bio_ru': 'Опытный менеджер, переходящий в IT с более чем двухлетним интенсивным обучением и дипломом SkillFactory. Готов внести вклад в инновационные проекты веб-разработки.',
            'bio_he': 'מנהל מנוסה העובר לתחום ה-IT, עם למעלה משנתיים של לימוד אינטנסיבי ודיפלומה מ-SkillFactory. מוכן לתרום לפרויקטים חדשניים בפיתוח ווב.',
            'years_management': 10,
            'years_it': 2,
            'team_size_managed': 15,
            'is_active': True,
        }
    )
    
    # Создаём опыт работы
    exp1, created = Experience.objects.get_or_create(
        profile=profile,
        company='SkillFactory',
        start_date='2022-01-01',
        defaults={
            'title_en': 'Fullstack Developer Student',
            'title_ru': 'Студент Fullstack разработки',
            'title_he': 'סטודנט פיתוח Fullstack',
            'end_date': '2024-01-01',
            'is_current': False,
            'description_en': 'Intensive 2-year program covering Python, Django, JavaScript, React, and modern web development practices.',
            'description_ru': 'Интенсивная 2-летняя программа, охватывающая Python, Django, JavaScript, React и современные практики веб-разработки.',
            'description_he': 'תוכנית אינטנסיבית של שנתיים הכוללת Python, Django, JavaScript, React ופרקטיקות פיתוח ווב מודרניות.',
            'experience_type': 'education',
            'location': 'Online',
            'order': 1,
        }
    )
    
    exp2, created = Experience.objects.get_or_create(
        profile=profile,
        company='Personal Projects',
        start_date='2024-01-01',
        defaults={
            'title_en': 'Self-Learning Developer',
            'title_ru': 'Самообучающийся разработчик',
            'title_he': 'מפתח אוטודידקט',
            'end_date': None,
            'is_current': True,
            'description_en': 'Continuing education through personal projects, contributing to open source, and staying updated with latest technologies.',
            'description_ru': 'Продолжение образования через личные проекты, участие в open source и изучение новейших технологий.',
            'description_he': 'המשך חינוך באמצעות פרויקטים אישיים, תרומה לקוד פתוח ועדכון בטכנולוגיות חדשות.',
            'experience_type': 'it',
            'location': 'Remote',
            'order': 2,
        }
    )
    
    # Сериализуем core данные
    core_objects = [profile, exp1, exp2]
    core_json = serializers.serialize('json', core_objects, indent=2)
    
    with open(fixtures_dir / 'core_data.json', 'w', encoding='utf-8') as f:
        f.write(core_json)
    
    print("✅ Core data created")
    
    # 2. Contact Info
    contact_info, created = ContactInfo.objects.get_or_create(
        id=1,
        defaults={
            'email': 'vitalivo@gmail.com',
            'phone': '+380123456789',
            'address': 'Ukraine',
            'linkedin_url': 'https://linkedin.com/in/vitaliy-voloshyn',
            'github_url': 'https://github.com/vitalivo',
            'telegram_url': 'https://t.me/vitalivo',
            'twitter_url': '',
            'working_hours_en': 'Monday - Friday, 9:00 AM - 6:00 PM (EET)',
            'working_hours_ru': 'Понедельник - Пятница, 9:00 - 18:00 (EET)',
            'working_hours_he': 'יום שני - יום שישי, 9:00 - 18:00 (EET)',
            'is_available_for_work': True,
            'availability_note_en': 'Open to new opportunities and interesting projects',
            'availability_note_ru': 'Открыт для новых возможностей и интересных проектов',
            'availability_note_he': 'פתוח להזדמנויות חדשות ופרויקטים מעניינים',
        }
    )
    
    contacts_json = serializers.serialize('json', [contact_info], indent=2)
    with open(fixtures_dir / 'contacts_data.json', 'w', encoding='utf-8') as f:
        f.write(contacts_json)
    
    print("✅ Contacts data created")
    
    print("🎉 All fixtures created successfully!")
    print(f"📁 Files created in: {fixtures_dir.absolute()}")
    
    # Показываем созданные файлы
    for file in fixtures_dir.glob('*.json'):
        print(f"  - {file.name}")

if __name__ == '__main__':
    create_fixtures()
