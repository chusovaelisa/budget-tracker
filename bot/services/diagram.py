from io import BytesIO

import matplotlib.pyplot as plt

from app.models import TransactionType, Category


def categorize_transactions(transactions):
    expenses = {}
    incomes = {}

    for transaction in transactions:
        if transaction.type == TransactionType.EXPENSE:
            if transaction.category.name not in expenses:
                expenses[transaction.category.name] = 0
            expenses[transaction.category.name] += transaction.amount
        elif transaction.type == TransactionType.INCOME:
            if transaction.category.name not in incomes:
                incomes[transaction.category.name] = 0
            incomes[transaction.category.name] += transaction.amount

    return expenses, incomes


def get_category_colors():
    category_colors = {}
    for category in Category.objects.all():
        category_colors[(category.name, category.type)] = category.color
    return category_colors


def create_pie_chart(data, category_colors, transaction_type, title):
    plt.figure(figsize=(8, 8))
    sorted_colors = [
        category_colors[(category_name, transaction_type)]
        for category_name in data.keys()
    ]
    plt.pie(data.values(), labels=data.keys(), autopct="%1.1f%%", colors=sorted_colors)
    plt.title(title)

    img_buffer = BytesIO()
    plt.savefig(img_buffer, format="png")
    img_buffer.seek(0)

    plt.close()

    return img_buffer
