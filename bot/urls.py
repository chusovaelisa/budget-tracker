"""
URL configuration for budget_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from bot.views import telegram_start_view, setwebhook, telegram_bot

urlpatterns = [
    path("auth/start/", telegram_start_view, name="telegram_auth_start"),
    path("getpost/", telegram_bot, name="telegram_bot"),
    path("setwebhook/", setwebhook, name="setwebhook"),
]
