from telegram import Bot
from .models import CoffeeUsers
import random
from django.utils import timezone
from django.conf import settings

def generate_random_code():
    return ''.join(random.choices('0123456789', k=6))

def save_telegram_code(username):
    try:
        user = CoffeeUsers.objects.get(username=username)
        code = generate_random_code()
        user.telegram_code = code
        user.code_creation_time = timezone.now()  # Записываем текущее время создания кода
        user.save(update_fields=['telegram_code', 'code_creation_time'])
        return code
    except CoffeeUsers.DoesNotExist:
        print(f"Ошибка: Пользователь с username={username} не найден")
        return None

def send_telegram_message(chat_id, code):
    bot = Bot(token=settings.TOKEN_TELEGRAM_BOT)
    bot.send_message(chat_id=chat_id, text=f'Ваш код подтверждения: {code}')

def save_telegram_code_and_send_message(username):
    code = save_telegram_code(username)
    if code:
        try:
            user = CoffeeUsers.objects.get(username=username)
            if user.chat_id:
                send_telegram_message(user.chat_id, code)
            else:
                print("Ошибка: Не указан chat_id для пользователя")
        except CoffeeUsers.DoesNotExist:
            print(f"Ошибка: Пользователь с username={username} не найден")


def delete_telegram_code(username):
    try:
        user = CoffeeUsers.objects.get(username=username)
        user.telegram_code = None
        user.code_creation_time = None
        user.save(update_fields=['telegram_code', 'code_creation_time'])
    except CoffeeUsers.DoesNotExist:
        print(f"Ошибка: Пользователь с username={username} не найден")