from uuid import uuid4

import telebot
from django.conf import settings

from app.models import User
from bot.models import TelegramAuthHash

bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN, parse_mode=None)


def process_chat_join_request(message):
    existing_user = User.objects.filter(telegram_id=message.chat.id).first()
    if existing_user:
        bot.reply_to(message, "Вы уже авторизованы")
    else:
        url = f"{settings.FRONTEND_URL}login/?next=/bot/auth/start/"
        bot.reply_to(message, f"Зарегистрируйтесь на сайте: {url}")


def generate_telegram_start_link(user_id: int) -> str:
    hash = str(uuid4())
    TelegramAuthHash.objects.update_or_create(
        user_id=user_id,
        defaults=dict(hash=hash),
    )
    return f"https://t.me/{settings.TELEGRAM_BOT_LOGIN}?start={hash}"


def connect_start_hash_with_telegram(auth_hash: str, chat_id: int) -> User | None:
    hash_info = TelegramAuthHash.objects.filter(hash=auth_hash).first()
    if hash_info:
        existing_user = User.objects.filter(telegram_id=chat_id).first()
        if existing_user:
            return existing_user.id
        else:
            User.objects.update_or_create(
                id=hash_info.user.id, defaults=dict(telegram_id=chat_id)
            )
            hash_info.delete()
        return hash_info.user.id
