import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from .models import Task, Status, Label


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=_("Статус"),
        empty_label="---------",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label=_("Исполнитель"),
        empty_label="---------",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    label = django_filters.ModelChoiceFilter(
        field_name="labels",
        queryset=Label.objects.all(),
        label=_("Метка"),
        empty_label="---------",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    self_tasks = django_filters.BooleanFilter(
        method="filter_self_tasks",
        label=_("Только свои задачи"),
        widget=forms.CheckboxInput(),
    )

    class Meta:
        model = Task
        fields = (
            "status",
            "executor",
            "label",
            "self_tasks",
        )

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.filters["status"].queryset = Status.objects.all().order_by("name")
        self.filters["executor"].queryset = User.objects.all().order_by("username")
        self.filters["label"].queryset = Label.objects.all().order_by("name")

        # ⭐ ВАЖНО: правильный способ задать отображение исполнителя
        self.form.fields["executor"].label_from_instance = (
            lambda user: user.get_full_name() or user.username
        )
