from telebot import types, TeleBot

from django.conf import settings

from app.models import User, Transaction, Category, TransactionType

bot = TeleBot(settings.TELEGRAM_BOT_TOKEN, parse_mode=None)


def category_keyboards(transaction_type):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    categories = Category.objects.all()
    categories = [
        category.name for category in categories if category.type == transaction_type
    ]

    for category in categories:
        keyboard.add(types.KeyboardButton(category))

    return keyboard


def choose_category(message: types.Message, user, transaction_type, amount, desc, time):
    category_name = message.text
    category = Category.objects.get(name=category_name, type=transaction_type)
    if category is not None:
        Transaction.objects.create(
            type=transaction_type,
            formatted_amount=amount,
            description=desc,
            date=time,
            user=user,
            category=category,
            target=None,
        )
        if transaction_type == TransactionType.EXPENSE:
            transaction = "расход"
        else:
            transaction = "доход"
        bot.send_message(
            message.chat.id, f"Добавлена транзакция {transaction}а на сумму {amount} p."
        )
    else:
        bot.send_message(message.chat.id, "Категория не найдена")
