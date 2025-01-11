from rest_framework import serializers

from app.models import User, Transaction, Target, Limit


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "password", "password2")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            password=validated_data["password"],
        )
        return user


class TransactionSerializer(serializers.ModelSerializer):
    formatted_amount = serializers.SerializerMethodField()
    category = serializers.CharField(source="category.name")
    logo = serializers.ImageField(source="category.logo")
    color = serializers.CharField(source="category.color")
    formatted_date = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = (
            "id",
            "type",
            "formatted_amount",
            "description",
            "date",
            "formatted_date",
            "category",
            "logo",
            "color",
            "target",
        )

    def get_formatted_amount(self, obj):
        return obj.formatted_amount

    def get_formatted_date(self, obj):
        return obj.date.strftime("%d.%m.%Y")


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ("id", "name", "target_sum", "current_sum")


class LimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Limit
        fields = ("id", "amount", "start_date", "end_date", "current_amount")
