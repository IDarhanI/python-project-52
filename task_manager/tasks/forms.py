from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from task_manager.models import Label, Task


class TaskForm(forms.ModelForm):
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label=_("Исполнитель"),
        empty_label=_("---------"),
    )

    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        required=False,
        label=_("Метки"),
    )

    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "labels"]
        labels = {
            "name": _("Имя"),
            "description": _("Описание"),
            "status": _("Статус"),
        }
