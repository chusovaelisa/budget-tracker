import json

import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from bot.credentials import TELEGRAM_API_URL, URL
from bot.services.auth import generate_telegram_start_link


@login_required
def telegram_start_view(request):
    return redirect(generate_telegram_start_link(request.user.id))


@csrf_exempt
def telegram_bot(request):
    if request.method == "POST":
        message = json.loads(request.body.decode("utf-8"))
        chat_id = message["message"]["chat"]["id"]
        text = message["message"]["text"]
        send_message("sendMessage", {"chat_id": f"your message {text}"})
    return HttpResponse("ok")


def handle_update(update):
    chat_id = update["message"]["chat"]["id"]
    text = update["message"]["text"]
    send_message("sendMessage", {"chat_id": chat_id, "text": f"you said {text}"})


def send_message(method, data):
    return requests.post(TELEGRAM_API_URL + method, data)


def setwebhook(request):
    response = requests.post(TELEGRAM_API_URL + "setWebhook?url=" + URL).json()
    return HttpResponse(f"{response}")
