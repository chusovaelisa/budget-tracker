import json
import datetime
import tempfile

import pandas as pd
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telebot import types, TeleBot
from django.conf import settings

from bot.services.auth import (
    process_chat_join_request,
    connect_start_hash_with_telegram,
)
from app.models import User, TransactionType, Transaction
from bot.services.diagram import (
    create_pie_chart,
    get_category_colors,
    categorize_transactions,
)
from bot.services.excel import get_transaction_data
from bot.services.transaction_info import category_keyboards, choose_category

bot = TeleBot(settings.TELEGRAM_BOT_TOKEN, parse_mode=None)

bot.set_my_commands(
    [
        types.BotCommand("/start", "Начать использование бота"),
        types.BotCommand("/addexpense", "Добавить расход"),
        types.BotCommand("/addincome", "Добавить доход"),
        types.BotCommand("/getexcel", "Получить Excel файл"),
        types.BotCommand("/getdiagrams", "Получить диаграммы"),
        types.BotCommand("/checkbot", "Проверить статус бота"),
    ]
)


@bot.message_handler(commands=["start"])
def send_welcome(message: types.Message):
    message_lst = message.text.split(" ")
    if len(message_lst) > 1:
        auth_hash = message_lst[1]
        user_id = connect_start_hash_with_telegram(auth_hash, message.chat.id)
        if user_id:
            user = User.objects.get(id=user_id)
            bot.reply_to(message, f"Вы авторизованы как {user.email}.")
        return
    process_chat_join_request(message)


@bot.message_handler(commands=["addexpense", "addincome"])
def choose_transaction(message: types.Message):
    bot.reply_to(message, "Укажите сумму и описание транзакции")
    if message.text.split()[0] == "/addexpense":
        transaction_type = TransactionType.EXPENSE
    else:
        transaction_type = TransactionType.INCOME
    bot.register_next_step_handler(
        message, add_transaction, transaction_type=transaction_type
    )


def add_transaction(message: types.Message, transaction_type):
    time = datetime.datetime.now()
    message_lst = message.text.split()
    try:
        amount = float(message_lst[0].replace(",", "."))
        if amount <= 0:
            raise ValueError
        desc = " ".join(message_lst[1:])
        user = User.objects.get(telegram_id=message.chat.id)
        bot.send_message(
            message.chat.id,
            "Выберите категорию транзакции",
            reply_markup=category_keyboards(transaction_type),
        )
        bot.register_next_step_handler(
            message,
            choose_category,
            user=user,
            transaction_type=transaction_type,
            amount=amount,
            desc=desc,
            time=time,
        )
    except ValueError:
        bot.send_message(message.chat.id, "Введены некорректные данные!")
        return


@bot.message_handler(commands=["getexcel"])
def get_excel(message: types.Message):
    chat_id = message.chat.id
    df_income = get_transaction_data(TransactionType.INCOME, chat_id)
    df_expense = get_transaction_data(TransactionType.EXPENSE, chat_id)
    df_income["Тип"] = "+"
    df_expense["Тип"] = "-"
    df_combined = pd.concat([df_income, df_expense], ignore_index=True)
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as temp_file:
        file_path = temp_file.name
        with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
            df_combined.to_excel(writer, index=False, sheet_name="Транзакции")
    with open(file_path, "rb") as file:
        bot.send_document(chat_id, file)


@bot.message_handler(commands=["getdiagrams"])
def get_diagrams(message: types.Message):
    user_id = User.objects.get(telegram_id=message.chat.id).id
    today = timezone.now().date()
    first_day_of_month = today.replace(day=1)
    last_day_of_month = first_day_of_month.replace(
        day=1, month=first_day_of_month.month + 1
    ) - datetime.timedelta(days=1)
    transactions = Transaction.objects.filter(
        user_id=user_id,
        date__date__gte=first_day_of_month,
        date__date__lte=last_day_of_month,
    )
    expenses, incomes = categorize_transactions(transactions)
    category_colors = get_category_colors()
    expenses_img = create_pie_chart(
        expenses, category_colors, "expense", "Диаграмма расходов"
    )
    incomes_img = create_pie_chart(
        incomes, category_colors, "income", "Диаграмма доходов"
    )
    bot.send_photo(chat_id=message.chat.id, photo=expenses_img)
    bot.send_photo(chat_id=message.chat.id, photo=incomes_img)


@bot.message_handler(commands=["checkbot"])
def check_bot(message: types.Message):
    bot_info = bot.get_me()
    bot.reply_to(message, json.dumps(bot_info, indent=4))


@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        json_str = request.body.decode("UTF-8")
        update = types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return JsonResponse({"status": "ok"})
    return HttpResponse("Hello, world!")


bot.remove_webhook()
bot.set_webhook(
    url="https://d5dkmg1odlbnd9bcan2a.apigw.yandexcloud.net/api/bot/setwebhook/"
)
