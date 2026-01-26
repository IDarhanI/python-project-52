from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Status, Task, Label


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")
        labels = {
            "first_name": _("First name"),
            "last_name": _("Last name"),
            "username": _("Username"),
        }


class UserUpdateForm(UserChangeForm):
    password = None  # Убираем поле смены пароля из формы редактирования

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")
        labels = {
            "first_name": _("First name"),
            "last_name": _("Last name"),
            "username": _("Username"),
        }


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ["name"]
        labels = {
            "name": _("Name"),
        }
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Status name")}
            )
        }


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ["name"]
        labels = {
            "name": _("Name"),
        }
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Label name")}
            )
        }


class TaskForm(forms.ModelForm):
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),
        required=False,
        label=_("Labels"),
    )

    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "labels"]
        labels = {
            "name": _("Name"),
            "description": _("Description"),
            "status": _("Status"),
            "executor": _("Executor"),
            "labels": _("Labels"),
        }
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Task name")}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": _("Task description"),
                }
            ),
            "status": forms.Select(attrs={"class": "form-control"}),
            "executor": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].queryset = Status.objects.all().order_by("name")
        self.fields["executor"].queryset = User.objects.all().order_by("username")
        self.fields["labels"].queryset = Label.objects.all().order_by("name")
        self.fields["executor"].required = False

        if self.instance.pk:
            self.fields["labels"].initial = self.instance.labels.all()

    def save(self, commit=True):
        task = super().save(commit=False)
        if commit:
            task.save()
            self.save_m2m()
        return task
