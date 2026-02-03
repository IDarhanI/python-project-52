from django import forms
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ["name"]
        labels = {
            "name": _("Имя"),
        }
