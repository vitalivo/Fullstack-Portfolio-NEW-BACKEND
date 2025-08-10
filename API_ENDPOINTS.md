# VITALY PORTFOLIO - API ENDPOINTS

## 🔗 BASE URL
- **Development**: `http://127.0.0.1:8000/api/v1/`
- **Production**: `https://your-domain.com/api/v1/`

## 📋 CORE ENDPOINTS

### Profiles
- `GET /api/v1/core/profiles/` - Список профилей
- `GET /api/v1/core/profiles/{id}/` - Детали профиля (с опытом работы)
- `GET /api/v1/core/profiles/{id}/experiences/` - Опыт работы профиля

### Experience
- `GET /api/v1/core/experiences/` - Список опыта работы
- `GET /api/v1/core/experiences/{id}/` - Детали опыта
- **Фильтры**: `?experience_type=it&is_current=true`
- **Поиск**: `?search=django`

## 🎨 PORTFOLIO ENDPOINTS

### Technologies
- `GET /api/v1/portfolio/technologies/` - Список технологий
- `GET /api/v1/portfolio/technologies/{id}/` - Детали технологии

### Project Categories
- `GET /api/v1/portfolio/categories/` - Категории проектов
- `GET /api/v1/portfolio/categories/{id}/` - Детали категории

### Projects
- `GET /api/v1/portfolio/projects/` - Список проектов
- `GET /api/v1/portfolio/projects/{id}/` - Детали проекта
- `GET /api/v1/portfolio/projects/featured/` - Рекомендуемые проекты
- `GET /api/v1/portfolio/projects/by_technology/?tech=django` - По технологии
- `GET /api/v1/portfolio/projects/{id}/images/` - Изображения проекта
- **Фильтры**: `?status=completed&project_type=fullstack&is_featured=true&year=2024`
- **Поиск**: `?search=django`

## 🎯 SKILLS ENDPOINTS

### Skill Categories
- `GET /api/v1/skills/categories/` - Категории навыков
- `GET /api/v1/skills/categories/with_skills/` - Категории с навыками

### Skills
- `GET /api/v1/skills/skills/` - Список навыков
- `GET /api/v1/skills/skills/{id}/` - Детали навыка
- `GET /api/v1/skills/skills/featured/` - Избранные навыки
- `GET /api/v1/skills/skills/by_category/?category=1` - По категории
- `GET /api/v1/skills/skills/recent/` - Недавно используемые
- **Фильтры**: `?proficiency_level=4&is_featured=true&skill_type=technical`

## 🏆 CERTIFICATES ENDPOINTS

### Certificates
- `GET /api/v1/certificates/certificates/` - Список сертификатов
- `GET /api/v1/certificates/certificates/{id}/` - Детали сертификата
- `GET /api/v1/certificates/certificates/featured/` - Избранные сертификаты
- `GET /api/v1/certificates/certificates/by_type/?type=diploma` - По типу
- `GET /api/v1/certificates/certificates/with_distinction/` - С отличием
- **Фильтры**: `?certificate_type=course&issuer=SkillFactory&is_featured=true`

## 📝 BLOG ENDPOINTS

### Blog Categories
- `GET /api/v1/blog/categories/` - Категории блога
- `GET /api/v1/blog/categories/{id}/` - Детали категории

### Blog Tags
- `GET /api/v1/blog/tags/` - Теги блога
- `GET /api/v1/blog/tags/{id}/` - Детали тега

### Blog Posts
- `GET /api/v1/blog/posts/` - Список постов (только опубликованные)
- `GET /api/v1/blog/posts/{id}/` - Детали поста (увеличивает счетчик)
- `GET /api/v1/blog/posts/featured/` - Избранные посты
- `GET /api/v1/blog/posts/by_category/?category=web-development` - По категории
- `GET /api/v1/blog/posts/by_tag/?tag=django` - По тегу
- **Фильтры**: `?is_featured=true&author=1`
- **Поиск**: `?search=python`

## 📞 CONTACTS ENDPOINTS

### Contact Messages
- `GET /api/v1/contacts/messages/` - Список сообщений (только админы)
- `POST /api/v1/contacts/messages/` - Отправить сообщение (публично)
- `GET /api/v1/contacts/messages/{id}/` - Детали сообщения
- **Фильтры**: `?status=new&priority=high`

### Contact Info
- `GET /api/v1/contacts/info/` - Контактная информация (публично)

## 🔧 ОБЩИЕ ПАРАМЕТРЫ

### Пагинация
- `?page=2` - Номер страницы
- `?page_size=10` - Размер страницы (по умолчанию 20)

### Сортировка
- `?ordering=created_at` - По возрастанию
- `?ordering=-created_at` - По убыванию

### Мультиязычность
Все поля возвращаются на всех языках:
\`\`\`json
{
  "title_en": "My Project",
  "title_ru": "Мой проект", 
  "title_he": "הפרויקט שלי"
}
\`\`\`

## 📚 ДОКУМЕНТАЦИЯ
- **Browsable API**: `http://127.0.0.1:8000/api/v1/`
- **API Docs**: `http://127.0.0.1:8000/api/docs/`
