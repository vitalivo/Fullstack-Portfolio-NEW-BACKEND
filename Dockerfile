FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Копирование requirements и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . .

# Создание директорий
RUN mkdir -p staticfiles media logs

# Открытие порта
EXPOSE 8000

# ОБНОВЛЕННАЯ команда с ПРИНУДИТЕЛЬНЫМ созданием админа
CMD ["sh", "-c", "python manage.py migrate --settings=config.settings_production && python manage.py create_superuser_if_none_exists --settings=config.settings_production && python manage.py import_fixtures --settings=config.settings_production && python manage.py collectstatic --noinput --settings=config.settings_production && gunicorn --bind 0.0.0.0:8000 config.wsgi:application"]
