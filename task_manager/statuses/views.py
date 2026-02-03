from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.statuses.models import Status

from .forms import StatusForm


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = "task_manager/statuses/statuses.html"
    context_object_name = "statuses"
    login_url = reverse_lazy("login")


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = "task_manager/statuses/create.html"
    success_url = reverse_lazy("statuses_list")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Статус успешно создан")
        return response


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = "task_manager/statuses/update.html"
    success_url = reverse_lazy("statuses_list")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Статус успешно изменен")
        return response


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = "task_manager/statuses/delete.html"
    success_url = reverse_lazy("statuses_list")
    login_url = reverse_lazy("login")

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            messages.success(request, "Статус успешно удален")
            return response
        except ProtectedError:
            messages.error(
                request,
                "Невозможно удалить статус, потому что он используется",
            )
            return redirect("statuses_list")
