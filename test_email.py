import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from decouple import config
import os

# Загружаем переменные окружения из .env файла
# Убедись, что твой .env файл находится в корневой папке backend
# (там же, где manage.py и этот скрипт)
# Если decouple не может найти .env, укажи полный путь:
# config.search_path = os.path.dirname(os.path.abspath(__file__))

# Получаем данные из .env
SENDER_EMAIL = config('GMAIL_USER')
SENDER_PASSWORD = config('GMAIL_APP_PASSWORD') # Используй App Password!
RECEIVER_EMAIL = config('CONTACT_FORM_RECIPIENT_EMAIL', default=SENDER_EMAIL) # Отправляем себе же
SMTP_SERVER = config('EMAIL_HOST', default='smtp.gmail.com')
SMTP_PORT = config('EMAIL_PORT', default=587, cast=int)

print(f"DEBUG: SENDER_EMAIL: {SENDER_EMAIL}")
print(f"DEBUG: RECEIVER_EMAIL: {RECEIVER_EMAIL}")
print(f"DEBUG: SMTP_SERVER: {SMTP_SERVER}")
print(f"DEBUG: SMTP_PORT: {SMTP_PORT}")
print(f"DEBUG: SENDER_PASSWORD (first 3 chars): {SENDER_PASSWORD[:3]}...") # Не выводим весь пароль

# Создаем сообщение
message = MIMEMultipart("alternative")
message["Subject"] = "Тестовое письмо от Python smtplib"
message["From"] = SENDER_EMAIL
message["To"] = RECEIVER_EMAIL

text = """\
Привет,
Это тестовое письмо, отправленное напрямую из Python с использованием smtplib.
Если ты его получил, значит, проблема не в Django.
"""
html = """\
<html>
  <body>
    <p>Привет,<br>
       Это <b>тестовое письмо</b>, отправленное напрямую из Python с использованием smtplib.<br>
       Если ты его получил, значит, проблема не в Django.
    </p>
  </body>
</html>
"""

part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

message.attach(part1)
message.attach(part2)

# Создаем безопасный SSL контекст
# ВРЕМЕННОЕ РЕШЕНИЕ ДЛЯ ЛОКАЛЬНОЙ ОТЛАДКИ: Отключаем проверку сертификатов
# НЕ ИСПОЛЬЗУЙТЕ В ПРОДАКШЕНЕ!
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

try:
    print(f"Попытка подключения к SMTP-серверу {SMTP_SERVER}:{SMTP_PORT}...")
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls(context=context) # Запускаем TLS
        print("TLS соединение установлено. Попытка входа...")
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        print("Вход успешен. Отправка письма...")
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())
        print("Письмо успешно отправлено!")
except smtplib.SMTPAuthenticationError as e:
    print(f"Ошибка аутентификации SMTP: {e}")
    print("Проверьте GMAIL_USER и GMAIL_APP_PASSWORD в вашем .env файле.")
    print("Убедитесь, что для Gmail используется 'пароль приложения', а не обычный пароль.")
except smtplib.SMTPConnectError as e:
    print(f"Ошибка подключения SMTP: {e}")
    print("Возможно, проблема с сетью, брандмауэром или SMTP-сервер недоступен.")
except smtplib.SMTPException as e:
    print(f"Общая ошибка SMTP: {e}")
except Exception as e:
    print(f"Неизвестная ошибка: {e}")
