from django import forms
from matplotlib import pyplot as plt

from app.models import Transaction, TransactionType, Target, Category, Limit


class RegistrationForm(forms.Form):
    first_name = forms.CharField(
        label="Имя",
        widget=forms.TextInput(attrs={"placeholder": "Имя", "id": "first_name"}),
    )
    last_name = forms.CharField(
        label="Фамилия",
        widget=forms.TextInput(attrs={"placeholder": "Фамилия", "id": "last_name"}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "Email", "id": "email"}),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"placeholder": "Пароль", "id": "password"}),
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Подтверждение пароля", "id": "password2"}
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["password"] != cleaned_data["password2"]:
            self.add_error("password", "Пароли не совпадают")
        return cleaned_data


class AuthForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "Email", "id": "email"}),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"placeholder": "Пароль", "id": "password"}),
    )


class TransactionForm(forms.ModelForm):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, localize=True)

    class Meta:
        model = Transaction
        fields = ["type", "amount", "description", "category", "target"]
        widgets = {
            "type": forms.Select(choices=TransactionType.choices),
            "category": forms.Select(),
            "target": forms.Select(),
            "amount": forms.TextInput(attrs={"placeholder": "Сумма"}),
        }

    def __init__(self, user, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields["category"].required = False
        self.fields["target"].required = False
        self.fields["category"].widget.choices = [
            (category.id, category.name) for category in Category.objects.all()
        ]
        self.fields["target"].widget.choices = [(None, "------")] + [
            (target.id, target.name) for target in Target.objects.filter(user=user)
        ]

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        formatted_amount = amount * 100
        return formatted_amount


class TargetForm(forms.ModelForm):
    target_sum = forms.DecimalField(max_digits=10, decimal_places=2, localize=True)

    class Meta:
        model = Target
        fields = ["name", "target_sum"]

    def __init__(self, *args, **kwargs):
        super(TargetForm, self).__init__(*args, **kwargs)


class LimitForm(forms.ModelForm):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, localize=True)

    class Meta:
        model = Limit
        fields = ["amount", "end_date"]

    def __init__(self, *args, **kwargs):
        super(LimitForm, self).__init__(*args, **kwargs)


class ChartForm(forms.Form):
    transaction_types = forms.MultipleChoiceField(
        choices=TransactionType.choices,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
