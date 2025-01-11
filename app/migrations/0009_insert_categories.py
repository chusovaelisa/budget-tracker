# Generated by Django 5.0.2 on 2024-05-28 17:54

from django.db import migrations


def insert_categories(apps, schema_editor):
    Category = apps.get_model("app", "Category")
    categories = [
        (2, "Переводы", "#ABCDEF", "переводы.png", "income"),
        (3, "Зарплата", "#44944A", "зарплата.png", "income"),
        (4, "Кэшбек", "#FFAE42", "кешбэк.png", "income"),
        (5, "Инвестиции", "#DA7CBF", "инвестиции.png", "income"),
        (6, "Пенсия", "#911E42", "пенсия.png", "income"),
        (7, "Премия", "#DD7022", "премия.png", "income"),
        (8, "Стипендия", "#7851A9", "стипендия.png", "income"),
        (9, "Налоговые доходы", "#CFB92A", "налоговые_доходы.png", "income"),
        (10, "Пособия", "#1DACD6", "пособие.png", "income"),
        (11, "Подарки", "#FFF44F", "подарки.png", "income"),
        (
            12,
            "Дополнительный доход",
            "#7B917B",
            "дополнительный_доход.png",
            "income",
        ),
        (13, "Такси", "#FFCF40", "такси.png", "expense"),
        (14, "Путешествия", "#DD80CC", "путешествия.png", "expense"),
        (15, "Супермаркет", "#47A76A", "супермаркет.png", "expense"),
        (16, "Доставка", "#009B76", "доставка.png", "expense"),
        (17, "Транспорт", "#42AAFF", "транспорт.png", "expense"),
        (18, "Переводы", "#8CCB5E", "переводы_PkEDd4g.png", "expense"),
        (19, "Здоровье", "#E86969", "здоровье.png", "expense"),
        (20, "Ремонт", "#F34723", "ремонт.png", "expense"),
        (21, "Одежда и обувь", "#702963", "одежда.png", "expense"),
        (23, "Красота", "#DD4492", "красота.png", "expense"),
        (24, "Образование", "#2A8D9C", "образование.png", "expense"),
        (25, "Налоги, штрафы", "#7442C8", "налоги_штрафы.png", "expense"),
        (26, "Питомцы", "#57A639", "питомцы.png", "expense"),
        (27, "Развлечения", "#CFB53B", "развлечения.png", "expense"),
        (
            28,
            "Благотворительность",
            "#CA3767",
            "благотворительность.png",
            "expense",
        ),
        (29, "Спорт", "#3E5F8A", "спорт.png", "expense"),
        (30, "Автомобиль", "#D5713F", "автомобиль.png", "expense"),
        (31, "Детские товары", "#F19CBB", "детские_товары.png", "expense"),
        (32, "Онлайн-маркеты", "#30D5C8", "онлайн_маркеты.png", "expense"),
        (33, "Связь", "#CDA434", "связь.png", "expense"),
        (34, "Хобби", "#1CAC78", "хобби.png", "expense"),
        (
            35,
            "Техника и электроника",
            "#FF7F50",
            "техника_электроника.png",
            "expense",
        ),
        (22, "Рестораны и кафе", "#AC5254", "рестораны_кафе.png", "expense"),
    ]
    for id, name, color, logo, type in categories:
        Category.objects.create(id=id, name=name, color=color, logo=logo, type=type)


def remove_categories(apps, schema_editor):
    Category = apps.get_model("app", "Category")
    Category.objects.filter(id__in=range(2, 36)).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0008_limit_current_amount"),
    ]

    operations = [
        migrations.RunPython(insert_categories, remove_categories),
    ]