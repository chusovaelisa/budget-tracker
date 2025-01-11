from django.db import models
from app.models import User


class TelegramAuthHash(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hash = models.CharField(max_length=100)
