import os
import tempfile

import matplotlib
import requests
import xlsxwriter
from django.contrib.auth.backends import ModelBackend
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from app.serializers import (
    UserSerializer,
    TransactionSerializer,
    TargetSerializer,
    LimitSerializer,
)
from bot.services.auth import generate_telegram_start_link

matplotlib.use("Agg")
from datetime import datetime, timedelta

from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404

from django.utils.timezone import make_aware

from rest_framework.views import APIView
from rest_framework.response import Response

from app.forms import (
    RegistrationForm,
    TransactionForm,
    TargetForm,
    LimitForm,
)

from app.models import Transaction, Target, Limit, TransactionType, Category, User
from rest_framework_simplejwt.tokens import RefreshToken


def welcome_view(request):
    return render(request, "app/welcome.html")


class MainView(APIView):
    def get(self, request):
        selected_date = request.GET.get("selected_date[formattedDate]")
        transactions = self.get_transactions(selected_date, request.user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def get_transactions(self, selected_date, current_user):
        if selected_date:
            selected_date = make_aware(datetime.strptime(selected_date, "%d.%m.%Y"))
            transactions = Transaction.objects.filter(
                date__date=selected_date.date(), user=current_user
            ).order_by("-date")
        else:
            transactions = Transaction.objects.filter(user=current_user).order_by(
                "-date"
            )[:5]

        return transactions


class RegistrationView(APIView):
    def post(self, request):
        form = RegistrationForm(request.data)

        if form.is_valid():
            user_data = {
                "email": form.cleaned_data["email"],
                "first_name": form.cleaned_data["first_name"],
                "last_name": form.cleaned_data["last_name"],
                "password": form.cleaned_data["password"],
                "password2": form.cleaned_data["password2"],
            }

            serializer = UserSerializer(data=user_data)

            if serializer.is_valid():
                user = serializer.save()
                next_url = request.GET.get("next")
                if next_url:
                    login(
                        request,
                        user,
                        backend="django.contrib.auth.backends.ModelBackend",
                    )
                    telegram_link = generate_telegram_start_link(user.id)
                    refresh = RefreshToken.for_user(user)
                    return Response(
                        {
                            "registration_link": telegram_link,
                            "refresh": str(refresh),
                            "access": str(refresh.access_token),
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response({"success": True}, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {"success": False, "errors": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"success": False, "errors": form.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class AuthView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddTransactionView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"error": "User is not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        form = TransactionForm(user=request.user, data=request.data)

        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()

            update_target_current_sum(transaction.target)

            return Response(
                {"message": "Transaction added successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


def update_target_current_sum(target):
    if target is None:
        return

    transactions = Transaction.objects.filter(target=target)
    current_sum = (
        transactions.aggregate(total_amount=Sum("amount"))["total_amount"] or 0
    ) / 100
    target.current_sum = current_sum

    if current_sum >= target.target_sum:
        target.reached = 100
    else:
        target.reached = round((current_sum / target.target_sum) * 100)

    target.save()


class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


@api_view(["PUT"])
def edit_transaction_view(request, transaction_id):
    categories = Category.objects.values("id", "name")
    targets = Target.objects.filter(user=request.user).values("id", "name")
    transaction = get_object_or_404(Transaction, id=transaction_id)

    form = TransactionForm(data=request.data, instance=transaction, user=request.user)

    if form.is_valid():
        updated_transaction = form.save()
        updated_transaction.save()
        return JsonResponse(
            {"success": True, "categories": list(categories), "targets": list(targets)}
        )

    return JsonResponse(
        {
            "error": "Invalid form data",
            "categories": list(categories),
            "targets": list(targets),
        },
        status=400,
    )


@api_view(["DELETE"])
def delete_transaction_view(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)

    if request.method == "DELETE":
        transaction.delete()
        return JsonResponse({"message": "Транзакции успешно удалены."})

    return JsonResponse({"error": "Метод не разрешен"}, status=405)


@api_view(["GET"])
def get_categories_targets(request):
    transaction_type = request.query_params.get("type")

    if transaction_type == "income":
        categories = Category.objects.filter(type="income").values("id", "name")
    elif transaction_type == "expense":
        categories = Category.objects.filter(type="expense").values("id", "name")
    else:
        categories = Category.objects.values("id", "name")

    targets = Target.objects.filter(user=request.user).values("id", "name")

    return Response(
        {"categories": list(categories), "targets": list(targets)},
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
def get_transaction_by_id_view(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    data = {
        "category": transaction.category_id,
        "type": transaction.type,
        "description": transaction.description,
        "amount": transaction.formatted_amount,
        "target": transaction.target_id,
    }
    return JsonResponse(data)


class CreateTargetView(APIView):
    def post(self, request):
        form = TargetForm(data=request.data)
        if form.is_valid():
            target = form.save(commit=False)
            target.user = request.user
            target.current_sum = 0
            target.save()
            return Response(
                {"message": "Target created successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class TargetListView(generics.ListAPIView):
    serializer_class = TargetSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        targets = Target.objects.filter(user=self.request.user)

        for target in targets:
            transactions = Transaction.objects.filter(target=target)
            current_sum = (
                transactions.aggregate(total_amount=Sum("amount"))["total_amount"] or 0
            ) / 100
            target.current_sum = current_sum

            if current_sum >= target.target_sum:
                target.reached = 100
            else:
                target.reached = round((current_sum / target.target_sum) * 100)

            target.save()

        return targets


@api_view(["PUT"])
def edit_target_view(request, target_id):
    target = get_object_or_404(Target, id=target_id)
    form = TargetForm(data=request.data, instance=target)
    if request.method == "PUT":
        if form.is_valid():
            updated_target = form.save(commit=False)
            updated_target.save()
            return JsonResponse({"success": True})
    return JsonResponse({"error": "Invalid request"}, status=400)


@api_view(["DELETE"])
def delete_target_view(request, target_id):
    target = get_object_or_404(Target, id=target_id)
    if request.method == "DELETE":
        target.delete()
        return JsonResponse({"message": "Цель успешно удалена"})

    return JsonResponse({"message": "Метод не разрешен"}, status=405)


@api_view(["GET"])
def get_target_by_id_view(request, target_id):
    target = get_object_or_404(Target, id=target_id)
    data = {"name": target.name, "target_sum": target.target_sum}
    return JsonResponse(data)


class LimitView(generics.RetrieveAPIView):
    serializer_class = LimitSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        limit = get_object_or_404(Limit, user=self.request.user)

        transactions = Transaction.objects.filter(
            user=self.request.user, type="expense", date__gte=limit.start_date
        )
        current_sum = (
            transactions.aggregate(total_amount=Sum("amount"))["total_amount"] or 0
        ) / 100
        limit.current_amount = current_sum
        limit.save()

        return limit


class CreateLimitView(APIView):
    def post(self, request):
        if Limit.objects.filter(user=request.user).exists():
            return Response(
                {"message": "Limit already exists for this user"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        form = LimitForm(data=request.data)
        if form.is_valid():
            limit = form.save(commit=False)
            limit.user = request.user
            limit.start_date = timezone.now()
            if "endDate" in request.data and request.data["endDate"]:
                end_date = datetime.strptime(request.data["endDate"], "%Y-%m-%d").date()
            else:
                end_date = limit.start_date + timedelta(days=30)

            limit.end_date = (
                timezone.make_aware(datetime.combine(end_date, datetime.min.time()))
                + timedelta(days=1)
                - timedelta(seconds=1)
            )

            limit.save()
            return Response(
                {"message": "Limit created successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def edit_limit_view(request, limit_id):
    limit = get_object_or_404(Limit, id=limit_id)
    form = LimitForm(data=request.data, instance=limit)

    if request.method == "PUT":
        if form.is_valid():
            edit_limit = form.save(commit=False)
            edit_limit.user = request.user

            if "start_date" not in request.data:
                edit_limit.start_date = limit.start_date

            if "endDate" in request.data and request.data["endDate"]:
                end_date = datetime.strptime(request.data["endDate"], "%Y-%m-%d").date()
            else:
                end_date = edit_limit.start_date + timedelta(days=30)

            edit_limit.end_date = (
                timezone.make_aware(datetime.combine(end_date, datetime.min.time()))
                + timedelta(days=1)
                - timedelta(seconds=1)
            )

            edit_limit.save()

            return JsonResponse({"success": True})
    return JsonResponse({"error": "Invalid request"}, status=400)


@api_view(["DELETE"])
def delete_limit_view(request, limit_id):
    limit = get_object_or_404(Limit, id=limit_id)

    if request.method == "DELETE":
        limit.delete()
        return JsonResponse({"message": "Лимит успешно удален"})

    return JsonResponse({"message": "Метод не разрешен"}, status=405)


class DownloadExcelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"error": "User is not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
            workbook = xlsxwriter.Workbook(temp_file.name)
            worksheet = workbook.add_worksheet()

            headers = ["Тип", "Сумма", "Категория", "Дата"]
            for col, header in enumerate(headers):
                worksheet.write(0, col, header)

            transactions = Transaction.objects.filter(user=request.user).order_by(
                "-date"
            )
            row = 1
            for transaction in transactions:
                sign = "+" if transaction.type == TransactionType.INCOME else "-"
                worksheet.write(row, 0, sign)
                worksheet.write(row, 1, f"{sign}{transaction.formatted_amount}")
                worksheet.write(row, 2, transaction.category.name)
                worksheet.write(row, 3, transaction.date.strftime("%d.%m.%Y"))
                row += 1

            workbook.close()

            with open(temp_file.name, "rb") as excel_file:
                response = HttpResponse(
                    excel_file.read(),
                    content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
                response[
                    "Content-Disposition"
                ] = 'attachment; filename="transactions.xlsx"'

        os.unlink(temp_file.name)

        return response


class GenerateChartData(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, transaction_type):
        transactions = Transaction.objects.filter(
            user=request.user, type=transaction_type
        )

        if not transactions.exists():
            return Response(
                {"labels": [], "data": [], "colors": []},
                status=status.HTTP_200_OK,
            )

        category_totals = transactions.values(
            "category__name", "category__color"
        ).annotate(total=Sum("amount"))

        data = {"labels": [], "data": [], "colors": []}

        for category_total in category_totals:
            data["labels"].append(category_total["category__name"])
            data["data"].append(category_total["total"] * 0.01)
            data["colors"].append(category_total["category__color"])

        return Response(data, status=status.HTTP_200_OK)


class GoogleBackend(ModelBackend):
    def authenticate(self, request, email=None):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None


class GoogleView(APIView):
    def post(self, request):
        token = request.data.get("token")

        if not token:
            return Response({"message": "Google token is missing"}, status=400)

        payload = {"access_token": token}
        r = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo", params=payload
        )
        data = r.json()

        if "error" in data:
            error_message = data.get("error_description", "Unknown error")
            return Response(
                {"message": f"Google token validation failed: {error_message}"},
                status=400,
            )

        user = GoogleBackend().authenticate(request, email=data["email"])
        if not user:
            user = User.objects.create_user(
                email=data["email"],
                first_name=data["given_name"],
                last_name=data["family_name"],
            )

        login(request, user, backend="django.contrib.auth.backends.ModelBackend")

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )


class TelegramAuthLinkView(APIView):
    def get(self, request):
        user_id = request.user.id
        telegram_link = generate_telegram_start_link(user_id)
        return Response(
            {"telegram_auth_link": telegram_link}, status=status.HTTP_200_OK
        )


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            token = RefreshToken(refresh_token)

            token.blacklist()

            logout(request)

            return Response(
                {"success": "Logged out successfully"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
