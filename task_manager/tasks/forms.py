from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.tasks.models import Task

User = get_user_model()


class TaskForm(forms.ModelForm):
    executor = forms.ModelChoiceField(
        queryset=User.objects.none(),
        required=False,
        label=_("Исполнитель"),
        empty_label=_("---------"),
    )

    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.none(),
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["executor"].queryset = User.objects.all()
        self.fields["executor"].label_from_instance = (
            lambda user: user.get_full_name() or user.username
        )

        self.fields["labels"].queryset = Label.objects.all()
