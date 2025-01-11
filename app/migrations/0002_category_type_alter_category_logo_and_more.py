# Generated by Django 5.0.2 on 2024-03-05 18:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="type",
            field=models.CharField(
                choices=[("income", "Доход"), ("expense", "Расход")],
                default=1,
                max_length=10,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="category",
            name="logo",
            field=models.ImageField(blank=True, null=True, upload_to="category/"),
        ),
        migrations.AlterField(
            model_name="limit",
            name="end_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 4, 4, 18, 49, 18, 703123, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
