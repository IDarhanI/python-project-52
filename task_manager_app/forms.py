from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Status, Task, Label


# ================= USERS =================


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


# ================= STATUSES =================


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ["name"]
        labels = {
            "name": _("Имя"),
        }


# ================= LABELS =================


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ["name"]
        labels = {
            "name": _("Имя"),
        }


# ================= TASKS =================


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "labels"]
        labels = {
            "name": _("Имя"),
            "description": _("Описание"),
            "status": _("Статус"),
            "executor": _("Исполнитель"),
            "labels": _("Метки"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["executor"].required = False
