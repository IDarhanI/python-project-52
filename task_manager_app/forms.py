from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Label, Status, Task


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
        )
        labels = {
            "first_name": _("Имя"),
            "last_name": _("Фамилия"),
            "username": _("Имя пользователя"),
            "password1": _("Пароль"),
            "password2": _("Подтверждение пароля"),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
        )
        labels = {
            "first_name": _("Имя"),
            "last_name": _("Фамилия"),
            "username": _("Имя пользователя"),
        }


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ["name"]
        labels = {
            "name": _("Имя"),
        }


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ["name"]
        labels = {
            "name": _("Имя"),
        }


class TaskForm(forms.ModelForm):
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label=_("Исполнитель"),
        empty_label=_("---------"),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        required=False,
        label=_("Метки"),
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "labels"]
        labels = {
            "name": _("Имя"),
            "description": _("Описание"),
            "status": _("Статус"),
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Имя задачи"),
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": _("Описание задачи"),
                }
            ),
            "status": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["status"].queryset = (
            Status.objects.all()
            .order_by("name")
        )
        self.fields["executor"].queryset = (
            User.objects.all()
            .order_by("username")
        )
        self.fields["labels"].queryset = (
            Label.objects.all()
            .order_by("name")
        )

        self.fields["executor"].label_from_instance = (
            lambda user: (
                f"{user.first_name} {user.last_name}".strip()
                if user.first_name or user.last_name
                else user.username
            )
        )

        if self.instance.pk:
            self.fields["labels"].initial = self.instance.labels.all()
