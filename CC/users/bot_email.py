from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import CoffeeUsers
from .bot_telegram import generate_random_code

def save_email_code(email):
    try:
        user = CoffeeUsers.objects.get(email=email)
        code = generate_random_code()
        user.telegram_code = code
        user.code_creation_time = timezone.now()  # Записываем текущее время создания кода
        user.save(update_fields=['telegram_code', 'code_creation_time'])
        return code
    except CoffeeUsers.DoesNotExist:
        print(f"Ошибка: Пользователь с email={email} не найден")
        return None

def send_email_message(email, code):
    subject = 'Код подтверждения'
    message = f'Ваш код подтверждения: {code}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

def delete_email_code(email):
    try:
        user = CoffeeUsers.objects.get(email=email)
        user.telegram_code = None
        user.code_creation_time = None
        user.save(update_fields=['telegram_code', 'code_creation_time'])
    except CoffeeUsers.DoesNotExist:
        print(f"Ошибка: Пользователь с email={email} не найден")