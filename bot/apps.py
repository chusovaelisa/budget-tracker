from django.apps import AppConfig
from django.conf import settings
from django.contrib.sites import requests


class BotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bot"

    def set_webhook(self):
        webhook_url = (
            f"https://d5dkmg1odlbnd9bcan2a.apigw.yandexcloud.net/telegram-webhook/"
        )
        telegram_url = (
            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/setWebhook"
        )
        response = requests.post(telegram_url, data={"url": webhook_url})
        print(response.json())
