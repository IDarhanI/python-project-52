from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import UserCreateForm, UserUpdateForm


class UsersListView(ListView):
    model = User
    template_name = "task_manager/users/users.html"
    context_object_name = "users"


class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm
    template_name = "task_manager/users/create.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            "Пользователь успешно зарегистрирован",
        )
        return response


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "task_manager/users/update.html"
    success_url = reverse_lazy("users_list")
    login_url = reverse_lazy("login")

    def test_func(self):
        return self.request.user == self.get_object()

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Пользователь успешно изменен")
        return response

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для изменения")
        return redirect("users_list")


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = "task_manager/users/delete.html"
    success_url = reverse_lazy("users_list")
    login_url = reverse_lazy("login")

    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для изменения")
        return redirect("users_list")

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            messages.success(request, "Пользователь успешно удален")
            return response
        except ProtectedError:
            messages.error(
                request,
                "Невозможно удалить пользователя, потому что он используется",
            )
            return redirect("users_list")
