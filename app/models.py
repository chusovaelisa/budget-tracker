from datetime import timedelta

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import (
    PermissionsMixin,
    UserManager as DjangoUserManager,
)
from django.db import models


class UserManager(DjangoUserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField("First name", max_length=150, blank=True)
    last_name = models.CharField("Last name", max_length=150, blank=True)
    email = models.EmailField("Email address", unique=True)
    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    telegram_id = models.BigIntegerField(unique=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Limit(models.Model):
    amount = models.IntegerField()
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    current_amount = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=30)
        super().save(*args, **kwargs)


class Target(models.Model):
    name = models.CharField(max_length=100)
    target_sum = models.IntegerField()
    current_sum = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class TransactionType(models.TextChoices):
    INCOME = "income", "Доход"
    EXPENSE = "expense", "Расход"


class Category(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=TransactionType.choices)
    color = models.CharField(max_length=7, null=True)
    logo = models.ImageField(upload_to="category/", null=True, blank=True)


class Transaction(models.Model):
    type = models.CharField(max_length=10, choices=TransactionType.choices)
    amount = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    target = models.ForeignKey(Target, on_delete=models.CASCADE, null=True)

    @property
    def formatted_amount(self):
        formatted_amount = self.amount / 100
        if formatted_amount == int(formatted_amount):
            return int(formatted_amount)
        return formatted_amount

    @formatted_amount.setter
    def formatted_amount(self, value):
        self.amount = int(value * 100)
