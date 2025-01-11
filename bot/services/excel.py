import os
import tempfile

import pandas as pd
from django.conf import settings

from app.models import Transaction, TransactionType


def get_transaction_data(transaction_type, chat_id):
    transactions = Transaction.objects.filter(
        type=transaction_type, user__telegram_id=chat_id
    )
    transaction_data = {
        "Тип": [
            "+" if transaction_type == TransactionType.INCOME else "-"
            for transaction in transactions
        ],
        "Сумма": [transaction.formatted_amount for transaction in transactions],
        "Категория": [transaction.category.name for transaction in transactions],
    }
    return pd.DataFrame(transaction_data)


def save_to_excel(df_income, df_expense, chat_id):
    temp_dir = tempfile.TemporaryDirectory(dir=settings.BASE_DIR)
    file_path = os.path.join(temp_dir.name, f"transactions_{chat_id}.xlsx")
    writer = pd.ExcelWriter(file_path, engine="xlsxwriter")
    df_income.to_excel(writer, index=False, sheet_name="Доход")
    df_expense.to_excel(writer, index=False, sheet_name="Расход")
    writer.close()
    return file_path
