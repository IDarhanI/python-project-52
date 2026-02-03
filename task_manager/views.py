from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label


def index(request):
    return render(request, "task_manager/index.html")


class LoginView(auth_views.LoginView):
    template_name = "registration/login.html"
    next_page = reverse_lazy("index")

    def form_valid(self, form):
        messages.success(self.request, _("Вы залогинены"))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            _("Пожалуйста, введите правильные имя пользователя и пароль."),
        )
        return super().form_invalid(form)


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy("index")

    def dispatch(self, request, *args, **kwargs):
        messages.info(self.request, _("Вы разлогинены"))
        return super().dispatch(request, *args, **kwargs)


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = "labels/list.html"
    context_object_name = "labels"


class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = "labels/create.html"
    success_url = reverse_lazy("labels_list")
    success_message = _("Метка успешно создана")

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = "labels/update.html"
    success_url = reverse_lazy("labels_list")
    success_message = _("Метка успешно изменена")

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = "labels/delete.html"
    success_url = reverse_lazy("labels_list")
    success_message = _("Метка успешно удалена")

    def post(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().post(request, *args, **kwargs)


def test_rollbar_error(request):
    raise Exception("Test Rollbar error")
