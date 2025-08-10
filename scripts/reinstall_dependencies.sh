# Шаг 1: Деактивируем текущее виртуальное окружение (если активно)
# Если ты в Windows PowerShell, используй 'deactivate'
# Если ты в Linux/macOS Bash, используй 'deactivate'
deactivate

# Шаг 2: Удаляем старое виртуальное окружение
# Будь осторожен! Убедись, что ты в папке 'backend'
# Если ты в Windows:
rmdir /s /q venv
# Если ты в Linux/macOS:
# rm -rf venv

# Шаг 3: Создаем новое виртуальное окружение
python -m venv venv

# Шаг 4: Активируем новое виртуальное окружение
# Если ты в Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Если ты в Linux/macOS Bash:
# source venv/bin/activate

# Шаг 5: Устанавливаем все необходимые зависимости
# Сначала убедимся, что pip обновлен
pip install --upgrade pip

# Устанавливаем зависимости из нашего requirements.txt
pip install -r requirements.txt

echo "Виртуальное окружение пересоздано и зависимости установлены."
echo "Теперь ты можешь запустить сервер Django: python manage.py runserver"
